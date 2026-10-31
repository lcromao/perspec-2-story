#!/usr/bin/env python3
"""
LLM-as-a-judge runner for the Data and Model Stories expert evaluation.

Commands
  config   Show the effective settings (config.json + .env) without calling the API.
  build    Write the exact messages sent for every pair and order (no API calls).
  run      Call the judges on OpenRouter: judges x pairs x orders x repetitions.
  status   Count valid, invalid and missing runs.
  analyze  Decode X/Y, build consensus labels and summaries; optionally compare with
           the human responses exported from the Google Forms.

What it adds to the prompts
  - Position-bias control: the "swapped" order shows the original Team Y content under
    the Team X label and vice versa; answers are mapped back before analysis.
  - Repetitions: --reps N runs every configuration N times.
  - Structured output: JSON schema sent as response_format, plus local validation and
    automatic re-runs when the output is invalid.
  - Decoding: X/Y -> group -> mapping / ad hoc, using the private key in config.json.

Only the Python standard library is used. Settings come from config.json and are
overridden by .env in this folder (variables already set in the shell win).
OPENROUTER_API_KEY must be set in .env or in the shell before "run".
Use --mock to test the whole pipeline without calling the API.
"""

import argparse
import concurrent.futures as cf
import csv
import datetime as dt
import hashlib
import json
import os
import random
import re
import sys
import threading
import time
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent

OPT_X = "Team X's version"
OPT_Y = "Team Y's version"
OPT_TIE = "No preference (both are equivalent)"
OPTIONS = [OPT_X, OPT_Y, OPT_TIE]
DISPLAY_CODE = {OPT_X: "X", OPT_Y: "Y", OPT_TIE: "TIE", "": "NA"}

STORIES = [
    "Data Collection",
    "Data Pre-processing",
    "Data Management",
    "Model Feature Preprocessing",
    "Model Training & Evaluation",
    "Model Deployment",
    "Model Integration",
]
CRITERIA = ["Completeness", "Clarity", "Correctness", "Consistency"]
QUESTIONS = [
    {"story": s + 1, "story_type": STORIES[s], "characteristic": CRITERIA[c],
     "preference_question": f"{s + 1}.{c + 1}.a", "comment_question": f"{s + 1}.{c + 1}.b"}
    for s in range(len(STORIES)) for c in range(len(CRITERIA))
]
QIDS = [q["preference_question"] for q in QUESTIONS]
QINFO = {q["preference_question"]: q for q in QUESTIONS}

ANSWER_ITEM = {
    "type": "object",
    "additionalProperties": False,
    "required": ["answer", "explanation"],
    "properties": {
        "answer": {"type": "string", "enum": OPTIONS + [""]},
        "explanation": {"type": "string"},
    },
}

SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["pair", "project", "answers", "coverage", "input_issues"],
    "properties": {
        "pair": {"type": "string"},
        "project": {"type": "string"},
        "answers": {
            "type": "object",
            "additionalProperties": False,
            "required": QIDS,
            "properties": {qid: ANSWER_ITEM for qid in QIDS},
        },
        "coverage": {
            "type": "object",
            "additionalProperties": False,
            "required": ["rows", "answered", "unanswered"],
            "properties": {
                "rows": {"type": "integer"},
                "answered": {"type": "integer"},
                "unanswered": {"type": "integer"},
            },
        },
        "input_issues": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["question_id", "missing_information", "effect"],
                "properties": {
                    "question_id": {"type": "string"},
                    "missing_information": {"type": "string"},
                    "effect": {"type": "string"},
                },
            },
        },
    },
}

PRINT_LOCK = threading.Lock()


def log(msg):
    with PRINT_LOCK:
        print(msg, flush=True)


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def sha256(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_dotenv(path):
    """Read KEY=VALUE lines from a .env file. Variables already set in the shell win."""
    path = Path(path)
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip().removeprefix("export ").strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        elif " #" in value:
            value = value.split(" #", 1)[0].strip()
        os.environ.setdefault(key, value)


def env(name, default=None):
    value = os.environ.get(name, "")
    return value.strip() if value.strip() else default


def env_bool(name, default):
    value = env(name)
    if value is None:
        return default
    return value.lower() in ("1", "true", "yes", "on")


def apply_env(cfg):
    """Override config.json with the values set in .env (or in the shell)."""
    cfg["app_title"] = env("OPENROUTER_APP_TITLE", cfg.get("app_title"))
    cfg["app_url"] = env("OPENROUTER_APP_URL", cfg.get("app_url", ""))
    cfg["openrouter_url"] = env("OPENROUTER_URL", cfg["openrouter_url"])
    cfg["prompts"]["system"] = env("PROMPT_SYSTEM", cfg["prompts"]["system"])
    cfg["prompts"]["shared_context"] = env("PROMPT_SHARED_CONTEXT", cfg["prompts"]["shared_context"])
    cfg["prompts"]["execution"] = env("PROMPT_EXECUTION", cfg["prompts"]["execution"])
    cfg["pair_context_pattern"] = env("PAIR_CONTEXT_PATTERN", cfg["pair_context_pattern"])
    cfg["runs_dir"] = env("RUNS_DIR", cfg["runs_dir"])
    pd = cfg.setdefault("provider_defaults", {})
    pd["data_collection"] = env("PROVIDER_DATA_COLLECTION", pd.get("data_collection", "deny"))
    pd["require_parameters"] = env_bool("PROVIDER_REQUIRE_PARAMETERS", pd.get("require_parameters", True))
    d = cfg["defaults"]
    d["reps"] = int(env("REPS", d["reps"]))
    d["workers"] = int(env("WORKERS", d["workers"]))
    d["max_invalid_retries"] = int(env("MAX_INVALID_RETRIES", d["max_invalid_retries"]))
    d["timeout_s"] = int(env("TIMEOUT_S", d.get("timeout_s", 1800)))
    d["http_retries"] = int(env("HTTP_RETRIES", d.get("http_retries", 5)))
    if env("ORDERS"):
        d["orders"] = [o.strip() for o in env("ORDERS").split(",") if o.strip()]
    for j in cfg["judges"]:
        if env("REASONING_EFFORT"):
            j["reasoning"] = {"effort": env("REASONING_EFFORT")}
        if env("MAX_TOKENS"):
            j["max_tokens"] = int(env("MAX_TOKENS"))
        k = j.get("env")
        if not k:
            continue
        j["id"] = env(f"JUDGE_{k}_ID", j["id"])
        j["enabled"] = env_bool(f"JUDGE_{k}_ENABLED", j.get("enabled", True))
        j["model"] = env(f"JUDGE_{k}_MODEL", j["model"])
        j["weights"] = env(f"JUDGE_{k}_WEIGHTS", j.get("weights"))
        j["structured_output"] = env_bool(f"JUDGE_{k}_STRUCTURED_OUTPUT", j.get("structured_output", True))
        if env(f"JUDGE_{k}_REASONING_EFFORT"):
            j["reasoning"] = {"effort": env(f"JUDGE_{k}_REASONING_EFFORT")}
        if env(f"JUDGE_{k}_MAX_TOKENS"):
            j["max_tokens"] = int(env(f"JUDGE_{k}_MAX_TOKENS"))
        if f"JUDGE_{k}_PROVIDER" in os.environ:
            prov = env(f"JUDGE_{k}_PROVIDER", "")
            if prov.lower() in ("", "auto", "none"):
                j["provider"] = None
            else:
                j["provider"] = {"order": [p.strip() for p in prov.split(",") if p.strip()],
                                 "allow_fallbacks": env_bool(f"JUDGE_{k}_ALLOW_FALLBACKS", False)}
    ids = [j["id"] for j in cfg["judges"]]
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        sys.exit(f"Judge ids must be unique; repeated: {', '.join(dup)}")
    return cfg


def load_config(path):
    cfg = json.loads(Path(path).read_text(encoding="utf-8"))
    cfg["_base"] = Path(path).resolve().parent
    return apply_env(cfg)


def enabled_judges(cfg):
    return [j for j in cfg["judges"] if j.get("enabled", True)]


def cfg_path(cfg, rel):
    return (cfg["_base"] / rel).resolve()


def read_text(path):
    return Path(path).read_text(encoding="utf-8").replace("\r\n", "\n")


def write_json_atomic(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(path)


# ---------------------------------------------------------------------------
# Prompt building
# ---------------------------------------------------------------------------

SWAP_RE = re.compile(
    r"(### Team X — (?P<name>[^\n]+?) Story\n)(?P<x>.*?)"
    r"(### Team Y — (?P=name) Story\n)(?P<y>.*?)"
    r"(?=\*\*\d\.1\.a — )",
    re.S,
)


def swap_teams(context_md):
    """Swap the Team X and Team Y story bodies, keeping labels and page order."""
    count = 0

    def repl(m):
        nonlocal count
        count += 1
        return m.group(1) + m.group("y") + m.group(4) + m.group("x")

    out = SWAP_RE.sub(repl, context_md)
    if count != len(STORIES):
        raise ValueError(f"Expected {len(STORIES)} story pairs to swap, found {count}.")
    return out


def pair_context(cfg, pair, order):
    text = read_text(cfg_path(cfg, cfg["pair_context_pattern"].format(pair=pair)))
    if order == "swapped":
        text = swap_teams(text)
    elif order != "original":
        raise ValueError(f"Unknown order: {order}")
    return text


def build_messages(cfg, pair, order):
    system = read_text(cfg_path(cfg, cfg["prompts"]["system"]))
    shared = read_text(cfg_path(cfg, cfg["prompts"]["shared_context"]))
    execution = read_text(cfg_path(cfg, cfg["prompts"]["execution"]))
    user = "\n\n---\n\n".join([shared.strip(), pair_context(cfg, pair, order).strip(), execution.strip()])
    return [{"role": "system", "content": system.strip()}, {"role": "user", "content": user}]


def project_label(cfg, pair):
    text = read_text(cfg_path(cfg, cfg["pair_context_pattern"].format(pair=pair)))
    pid = re.search(r"^Project ID:\s*(.+)$", text, re.M)
    name = re.search(r"^Project name:\s*(.+)$", text, re.M)
    return f"{pid.group(1).strip() if pid else '?'} — {name.group(1).strip() if name else '?'}"


# ---------------------------------------------------------------------------
# OpenRouter
# ---------------------------------------------------------------------------

class ApiError(Exception):
    pass


def provider_prefs(cfg, judge):
    """Provider routing for one judge: pinned order (if any) plus the study-wide data policy."""
    prefs = dict(judge.get("provider") or {})
    pd = cfg.get("provider_defaults", {})
    if pd.get("data_collection"):
        prefs["data_collection"] = pd["data_collection"]
    if pd.get("require_parameters"):
        prefs["require_parameters"] = True
    return prefs


def call_openrouter(cfg, judge, messages, api_key):
    body = {
        "model": judge["model"],
        "messages": messages,
        "max_tokens": judge.get("max_tokens", 32000),
        "usage": {"include": True},
    }
    if judge.get("reasoning"):
        body["reasoning"] = judge["reasoning"]
    provider = provider_prefs(cfg, judge)
    if provider:
        body["provider"] = provider
    if judge.get("structured_output", True):
        body["response_format"] = {
            "type": "json_schema",
            "json_schema": {"name": "expert_evaluation", "strict": True, "schema": SCHEMA},
        }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-Title": cfg.get("app_title", "LLM judge runner"),
    }
    if cfg.get("app_url"):
        headers["HTTP-Referer"] = cfg["app_url"]
    retries = cfg["defaults"].get("http_retries", 5)
    timeout = cfg["defaults"].get("timeout_s", 900)
    last = None
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(cfg["openrouter_url"], data=json.dumps(body).encode("utf-8"),
                                         headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            if "error" in data and not data.get("choices"):
                code = data["error"].get("code")
                last = f"API error {code}: {data['error'].get('message')}"
                if code in (408, 429, 500, 502, 503, 504):
                    raise urllib.error.URLError(last)
                raise ApiError(last)
            return data
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")[:500]
            last = f"HTTP {e.code}: {detail}"
            if e.code not in (408, 429, 500, 502, 503, 504):
                raise ApiError(last)
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            last = f"{type(e).__name__}: {e}"
        wait = min(60, 2 ** attempt) + random.random()
        log(f"    retry {attempt + 1}/{retries} in {wait:.0f}s ({last[:120]})")
        time.sleep(wait)
    raise ApiError(f"Giving up after {retries} retries: {last}")


def message_text(data):
    msg = data["choices"][0]["message"]
    content = msg.get("content")
    if isinstance(content, list):
        content = "".join(p.get("text", "") for p in content if isinstance(p, dict))
    return content or "", msg.get("reasoning")


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def extract_json(text):
    t = text.strip()
    t = re.sub(r"^```(?:json)?\s*", "", t)
    t = re.sub(r"\s*```$", "", t)
    start, end = t.find("{"), t.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("No JSON object found in the response.")
    return json.loads(t[start:end + 1])


def validate(obj, pair):
    errors = []
    if not isinstance(obj, dict):
        return ["Response is not a JSON object."]
    if obj.get("pair") != pair:
        errors.append(f"pair is {obj.get('pair')!r}, expected {pair!r}.")
    answers = obj.get("answers")
    if not isinstance(answers, dict):
        return errors + ["answers is not an object keyed by question ID."]
    extra = [k for k in answers if k not in QINFO]
    if extra:
        errors.append(f"answers has unknown keys: {', '.join(map(str, extra[:5]))}.")
    for qid in QIDS:
        item = answers.get(qid)
        if item is None:
            errors.append(f"{qid} is missing.")
            continue
        if not isinstance(item, dict):
            errors.append(f"{qid} is not an object.")
            continue
        if item.get("answer") not in OPTIONS + [""]:
            errors.append(f"{qid}: answer {item.get('answer')!r} is not an allowed option.")
        if not isinstance(item.get("explanation"), str) or not item["explanation"].strip():
            errors.append(f"{qid}: explanation is empty.")
    items = [answers.get(q) for q in QIDS if isinstance(answers.get(q), dict)]
    answered = sum(1 for i in items if i.get("answer") in OPTIONS)
    unanswered_ids = {q for q in QIDS if isinstance(answers.get(q), dict) and answers[q].get("answer") == ""}
    cov = obj.get("coverage") or {}
    if cov.get("answered") != answered or cov.get("unanswered") != len(unanswered_ids) or cov.get("rows") != len(QIDS):
        errors.append(f"coverage {cov} does not match {answered} answered / {len(unanswered_ids)} unanswered.")
    issues = obj.get("input_issues")
    if not isinstance(issues, list):
        errors.append("input_issues is not a list.")
    else:
        listed = {i.get("question_id") for i in issues if isinstance(i, dict)}
        for qid in sorted(unanswered_ids - listed):
            errors.append(f"{qid} is unanswered but not listed in input_issues.")
    return errors


def normalize(obj):
    """Validated judge output -> one row per question, with story and characteristic."""
    responses = [dict(QINFO[q], answer=obj["answers"][q]["answer"],
                      explanation=obj["answers"][q]["explanation"].strip()) for q in QIDS]
    return {"pair": obj["pair"], "project": obj.get("project"), "responses": responses,
            "coverage": obj["coverage"], "input_issues": obj["input_issues"]}


# ---------------------------------------------------------------------------
# Mock judge (pipeline tests only)
# ---------------------------------------------------------------------------

def mock_response(cfg, judge, pair, order, rep, attempt):
    """Deterministic fake judge with some noise and a small preference for the first position."""
    rng = random.Random(f"{judge['id']}|{pair}|{order}|{rep}|{attempt}")
    answers = {}
    for q in QUESTIONS:
        qid = q["preference_question"]
        truth = random.Random(f"truth|{pair}|{qid}").choices(["X", "Y", "TIE"], [0.45, 0.4, 0.15])[0]
        label = truth
        if rng.random() < 0.2:
            label = rng.choice(["X", "Y", "TIE"])
        if order == "swapped" and label in ("X", "Y"):
            label = "Y" if label == "X" else "X"
        if rng.random() < 0.12:
            label = "X"
        answer = {"X": OPT_X, "Y": OPT_Y, "TIE": OPT_TIE}[label]
        answers[qid] = {"answer": answer, "explanation": f"Mock explanation for {qid} ({pair} / Story {q['story']})."}
    obj = {"pair": pair, "project": project_label(cfg, pair), "answers": answers,
           "coverage": {"rows": 28, "answered": 28, "unanswered": 0}, "input_issues": []}
    if attempt == 1 and rng.random() < 0.15:
        del obj["answers"]["7.4.a"]
    content = json.dumps(obj, ensure_ascii=False)
    return {"model": judge["model"] + " (mock)", "provider": "mock",
            "choices": [{"message": {"content": content}, "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 0, "completion_tokens": 0, "cost": 0}}


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

def run_dir(cfg, name):
    return cfg_path(cfg, cfg["runs_dir"]) / name


def raw_path(rdir, judge_id, pair, order, rep):
    return rdir / "raw" / judge_id / f"{pair}_{order}_r{rep}.json"


def render_markdown(obj, meta):
    lines = [f"# {meta['judge']} — Pair {meta['pair']} — {meta['order']} — rep {meta['rep']}", ""]
    if meta["order"] == "swapped":
        lines += ["> Swapped order: the content shown as Team X was the original Team Y, and vice versa. "
                  "Answers and explanations below use the labels as displayed to the judge.", ""]
    lines += [f"Pair: {obj.get('pair')}", f"Project: {obj.get('project')}", ""]
    by_story = defaultdict(list)
    for r in obj["responses"]:
        by_story[r["story"]].append(r)
    for s in sorted(by_story):
        lines += [f"## {s}. {STORIES[s - 1]}", "",
                  "| Preference question | Characteristic | Answer | Comment question | Explanation |",
                  "|---|---|---|---|---|"]
        for r in sorted(by_story[s], key=lambda r: r["preference_question"]):
            expl = r["explanation"].replace("|", "\\|").replace("\n", " ")
            lines.append(f"| {r['preference_question']} | {r['characteristic']} | {r['answer']} | {r['comment_question']} | {expl} |")
        lines.append("")
    cov = obj.get("coverage", {})
    lines.append(f"Coverage: {cov.get('rows')} preference rows; {cov.get('answered')} answered; {cov.get('unanswered')} unanswered.")
    issues = obj.get("input_issues") or []
    lines.append("Input issues: None." if not issues else "Input issues:")
    for i in issues:
        lines.append(f"- {i.get('question_id')}: {i.get('missing_information')} ({i.get('effect')})")
    return "\n".join(lines) + "\n"


def run_one(cfg, rdir, judge, pair, order, rep, api_key, mock, force):
    path = raw_path(rdir, judge["id"], pair, order, rep)
    if path.exists() and not force:
        try:
            if json.loads(path.read_text(encoding="utf-8")).get("valid"):
                return "skipped"
        except json.JSONDecodeError:
            pass
    messages = build_messages(cfg, pair, order)
    meta = {
        "judge": judge["id"], "model_requested": judge["model"], "weights": judge.get("weights"),
        "reasoning": judge.get("reasoning"), "provider_requested": provider_prefs(cfg, judge),
        "structured_output": judge.get("structured_output", True), "max_tokens": judge.get("max_tokens"),
        "pair": pair, "form": cfg["pairs"][pair]["form"], "order": order, "rep": rep,
        "prompt_sha256": sha256(json.dumps(messages, ensure_ascii=False)), "mock": mock, "started": now(),
    }
    record = {"meta": meta, "attempts": [], "valid": False, "final": None, "errors": []}
    max_tries = 1 + cfg["defaults"].get("max_invalid_retries", 2)
    for attempt in range(1, max_tries + 1):
        entry = {"attempt": attempt, "time": now()}
        try:
            data = mock_response(cfg, judge, pair, order, rep, attempt) if mock else call_openrouter(cfg, judge, messages, api_key)
            content, reasoning = message_text(data)
            entry.update({"generation_id": data.get("id"), "model_returned": data.get("model"), "provider_returned": data.get("provider"),
                          "finish_reason": data["choices"][0].get("finish_reason"), "usage": data.get("usage"),
                          "content": content})
            if reasoning:
                entry["reasoning"] = reasoning
            obj = extract_json(content)
            errors = validate(obj, pair)
            if entry["finish_reason"] == "length":
                errors.append("Output truncated (finish_reason=length); raise max_tokens.")
        except ApiError as e:
            entry["api_error"] = str(e)
            record["attempts"].append(entry)
            record["errors"] = [str(e)]
            break
        except (ValueError, KeyError, IndexError, json.JSONDecodeError) as e:
            obj, errors = None, [f"Could not parse response: {e}"]
        entry["errors"] = errors
        record["attempts"].append(entry)
        record["errors"] = errors
        if not errors:
            record["valid"], record["final"] = True, normalize(obj)
            break
        log(f"    {judge['id']} {pair} {order} r{rep}: invalid output (attempt {attempt}): {errors[0][:120]}")
    meta["finished"] = now()
    write_json_atomic(path, record)
    if record["valid"]:
        md = rdir / "readable" / judge["id"] / f"{pair}_{order}_r{rep}.md"
        md.parent.mkdir(parents=True, exist_ok=True)
        md.write_text(render_markdown(record["final"], meta), encoding="utf-8")
    return "valid" if record["valid"] else "invalid"


def select(items, wanted, label):
    if not wanted or wanted == "all":
        return items
    keys = [w.strip() for w in wanted.split(",") if w.strip()]
    unknown = [k for k in keys if k not in items]
    if unknown:
        sys.exit(f"Unknown {label}: {', '.join(unknown)}. Available: {', '.join(items)}")
    return keys


def cmd_build(cfg, args):
    rdir = run_dir(cfg, args.run)
    for pair in cfg["pairs"]:
        for order in cfg["defaults"]["orders"]:
            messages = build_messages(cfg, pair, order)
            out = rdir / "prompts" / f"{pair}_{order}"
            write_json_atomic(out.with_suffix(".json"), messages)
            out.with_suffix(".txt").write_text(
                f"=== SYSTEM ===\n{messages[0]['content']}\n\n=== USER ===\n{messages[1]['content']}\n", encoding="utf-8")
            print(f"{pair} {order}: {len(messages[0]['content']) + len(messages[1]['content'])} chars -> {out}.txt")


def judge_line(j):
    prov = j.get("provider") or {}
    prov_txt = ",".join(prov.get("order", [])) + ("" if prov.get("allow_fallbacks", True) else " (pinned)") if prov else "auto"
    return (f"{j['id']:<22} {j['model']:<36} weights={j.get('weights')}, provider={prov_txt}, "
            f"effort={(j.get('reasoning') or {}).get('effort')}, max_tokens={j.get('max_tokens')}, "
            f"json_schema={j.get('structured_output', True)}")


def human_specs_from_env(cfg):
    specs, notes = [], []
    for form in sorted({v["form"] for v in cfg["pairs"].values()}):
        path = env(f"HUMAN_FORM_{form}")
        if not path:
            continue
        full = Path(path) if Path(path).is_absolute() else cfg["_base"] / path
        if full.exists():
            specs.append(f"{form}={full}")
        else:
            notes.append(f"HUMAN_FORM_{form}: {full} not found (skipped)")
    return specs, notes


def cmd_config(cfg, args):
    if not (HERE / ".env").exists() and not os.environ.get("ENV_FILE"):
        print("No .env found. Create it with: cp .env.example .env  (then fill in OPENROUTER_API_KEY)")
    key = env("OPENROUTER_API_KEY", "")
    print(f"OPENROUTER_API_KEY: {'set' if key else 'MISSING'}")
    print(f"Endpoint: {cfg['openrouter_url']}")
    print(f"App title: {cfg.get('app_title')} | App URL: {cfg.get('app_url') or '-'}")
    d = cfg["defaults"]
    print(f"Run name: {args.run} | pairs: {env('PAIRS') or 'all'} | orders: {','.join(d['orders'])} | reps: {d['reps']} "
          f"| workers: {d['workers']} | max invalid retries: {d['max_invalid_retries']} "
          f"| timeout: {d['timeout_s']}s | HTTP retries: {d['http_retries']}")
    print("Prompts: " + ", ".join(f"{k}={cfg['prompts'][k]}" for k in ("system", "shared_context", "execution")))
    print(f"Pair contexts: {cfg['pair_context_pattern']} | runs dir: {cfg['runs_dir']}")
    pd = cfg["provider_defaults"]
    print(f"Provider policy: data_collection={pd['data_collection']} | require_parameters={pd['require_parameters']}")
    missing = [str(cfg_path(cfg, v)) for v in cfg["prompts"].values() if not cfg_path(cfg, v).exists()]
    missing += [str(cfg_path(cfg, cfg["pair_context_pattern"].format(pair=p))) for p in cfg["pairs"]
                if not cfg_path(cfg, cfg["pair_context_pattern"].format(pair=p)).exists()]
    for m in missing:
        print(f"  MISSING FILE: {m}")
    print("Judges:")
    for j in cfg["judges"]:
        print(("  " if j.get("enabled", True) else "  [disabled] ") + judge_line(j))
    weights = Counter(j.get("weights") for j in enabled_judges(cfg))
    print("Weights among enabled judges: " + ", ".join(f"{k}={v}" for k, v in weights.items()))
    specs, notes = human_specs_from_env(cfg)
    print("Human CSVs: " + (", ".join(s.split("=", 1)[0] for s in specs) if specs else "none found"))
    for n in notes:
        print("  " + n)


def cmd_run(cfg, args):
    api_key = env("OPENROUTER_API_KEY", "")
    if not args.mock and not api_key:
        sys.exit("Set OPENROUTER_API_KEY in .env (cp .env.example .env), or in the shell, or use --mock.")
    judges = {j["id"]: j for j in cfg["judges"]}
    judge_ids = select([j["id"] for j in enabled_judges(cfg)], None, "judges") if not args.judges else \
        select(list(judges), args.judges, "judges")
    pairs = select(list(cfg["pairs"]), args.pairs or env("PAIRS"), "pairs")
    orders = select(["original", "swapped"], args.orders or ",".join(cfg["defaults"]["orders"]), "orders")
    reps = args.reps or cfg["defaults"]["reps"]
    workers = args.workers or cfg["defaults"]["workers"]
    rdir = run_dir(cfg, args.run)
    for pair in pairs:
        for order in orders:
            build_messages(cfg, pair, order)
    tasks = [(judges[j], p, o, r) for j in judge_ids for p in pairs for o in orders for r in range(1, reps + 1)]
    log(f"Run '{args.run}': {len(tasks)} tasks ({len(judge_ids)} judges x {len(pairs)} pairs x {len(orders)} orders x {reps} reps)"
        + (" [MOCK]" if args.mock else ""))
    for jid in judge_ids:
        log("  " + judge_line(judges[jid]))
    results = Counter()
    with cf.ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(run_one, cfg, rdir, j, p, o, r, api_key, args.mock, args.force): (j["id"], p, o, r)
                   for j, p, o, r in tasks}
        for fut in cf.as_completed(futures):
            jid, p, o, r = futures[fut]
            try:
                status = fut.result()
            except Exception as e:
                status = "error"
                log(f"  {jid} {p} {o} r{r}: {type(e).__name__}: {e}")
            results[status] += 1
            if status != "skipped":
                log(f"  {jid:<22} {p} {o:<8} r{r}: {status}")
    log("Done: " + ", ".join(f"{k}={v}" for k, v in sorted(results.items())))
    if results["invalid"] or results["error"]:
        log("Some runs are not valid. Check raw/*.json ('errors') and run the same command again to retry them.")


def cmd_status(cfg, args):
    rdir = run_dir(cfg, args.run)
    reps = args.reps or cfg["defaults"]["reps"]
    print(f"{'judge':<22} {'valid':>5} {'invalid':>7} {'missing':>7} {'cost $':>8}")
    for j in enabled_judges(cfg):
        c, cost = Counter(), 0.0
        for p in cfg["pairs"]:
            for o in cfg["defaults"]["orders"]:
                for r in range(1, reps + 1):
                    path = raw_path(rdir, j["id"], p, o, r)
                    if not path.exists():
                        c["missing"] += 1
                        continue
                    rec = json.loads(path.read_text(encoding="utf-8"))
                    c["valid" if rec.get("valid") else "invalid"] += 1
                    for a in rec.get("attempts", []):
                        cost += float((a.get("usage") or {}).get("cost") or 0)
        print(f"{j['id']:<22} {c['valid']:>5} {c['invalid']:>7} {c['missing']:>7} {cost:>8.2f}")


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

def to_original(code, order):
    if order == "swapped" and code in ("X", "Y"):
        return "Y" if code == "X" else "X"
    return code


def condition_of(code, pinfo):
    if code in ("X", "Y"):
        group = pinfo["x"] if code == "X" else pinfo["y"]
        return group, ("mapping" if group == pinfo["mapping"] else "ad hoc")
    if code == "TIE":
        return "", "no preference"
    if code == "NO_MAJORITY":
        return "", "no majority"
    return "", "unanswered"


def majority(labels):
    labels = [l for l in labels if l in ("X", "Y", "TIE")]
    if not labels:
        return "NONE"
    top, n = Counter(labels).most_common(1)[0]
    return top if n > len(labels) / 2 else "NO_MAJORITY"


def cohen_kappa(a, b):
    n = len(a)
    if n == 0:
        return float("nan")
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(a) | set(b)) / (n * n)
    if pe == 1:
        return 1.0 if po == 1 else float("nan")
    return (po - pe) / (1 - pe)


def fmt(x, pct=False):
    if x is None or x != x:
        return "–"
    return f"{100 * x:.0f}%" if pct else f"{x:.2f}"


def load_human(cfg, specs):
    """specs: ['A=path.csv', ...] -> {(pair, qid): [codes]}, respondents per form."""
    form_to_pair = {v["form"]: k for k, v in cfg["pairs"].items()}
    votes, counts = defaultdict(list), {}
    for spec in specs or []:
        form, _, path = spec.partition("=")
        form = form.strip().upper()
        if form not in form_to_pair or not path:
            sys.exit(f"Bad --human value {spec!r}; use FORM=path.csv with FORM in {', '.join(form_to_pair)}.")
        pair = form_to_pair[form]
        with open(path, newline="", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            header = next(reader)
            cols = {}
            for i, h in enumerate(header):
                m = re.match(r"^\s*(\d\.\d\.a)\b", h)
                if m:
                    cols[m.group(1)] = i
            if len(cols) != len(QIDS):
                sys.exit(f"{path}: found {len(cols)} preference columns, expected {len(QIDS)}.")
            n = 0
            for row in reader:
                answers = {qid: (row[i].strip() if i < len(row) else "") for qid, i in cols.items()}
                if not any(answers.values()):
                    continue
                n += 1
                for qid, ans in answers.items():
                    votes[(pair, qid)].append(DISPLAY_CODE.get(ans, "NA"))
            counts[form] = n
    return votes, counts


def cmd_analyze(cfg, args):
    rdir = run_dir(cfg, args.run)
    out = rdir / "analysis"
    out.mkdir(parents=True, exist_ok=True)
    judges = {j["id"]: j for j in cfg["judges"]}
    long_rows, run_stats = [], defaultdict(Counter)
    cell = defaultdict(list)
    for path in sorted((rdir / "raw").glob("*/*.json")):
        rec = json.loads(path.read_text(encoding="utf-8"))
        m = rec["meta"]
        run_stats[m["judge"]]["valid" if rec.get("valid") else "invalid"] += 1
        for a in rec.get("attempts", []):
            u = a.get("usage") or {}
            run_stats[m["judge"]]["cost_micro"] += int(float(u.get("cost") or 0) * 1e6)
        if not rec.get("valid"):
            continue
        pinfo = cfg["pairs"][m["pair"]]
        model_returned = (rec["attempts"][-1].get("model_returned") or "")
        for r in rec["final"]["responses"]:
            shown = DISPLAY_CODE[r["answer"]]
            orig = to_original(shown, m["order"])
            group, cond = condition_of(orig, pinfo)
            qid = r["preference_question"]
            long_rows.append({
                "judge": m["judge"], "weights": m.get("weights"), "model_returned": model_returned,
                "pair": m["pair"], "form": pinfo["form"], "project": pinfo["project"], "order": m["order"],
                "rep": m["rep"], "question_id": qid, "story": r["story"], "story_type": r["story_type"],
                "characteristic": r["characteristic"], "displayed_answer": r["answer"], "displayed_code": shown,
                "original_code": orig, "preferred_group": group, "preferred_condition": cond,
                "labels_swapped_in_explanation": m["order"] == "swapped", "explanation": r["explanation"],
            })
            cell[(m["judge"], m["pair"], qid)].append((m["order"], m["rep"], orig, shown))

    if not long_rows:
        sys.exit("No valid runs to analyze.")
    with open(out / "decoded_long.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(long_rows[0]))
        w.writeheader()
        w.writerows(long_rows)

    # Consensus per judge x pair x question
    consensus, cons_rows = {}, []
    pos_bias = defaultdict(Counter)
    stability = defaultdict(list)
    for (jid, pair, qid), runs in sorted(cell.items()):
        pinfo = cfg["pairs"][pair]
        by_order = defaultdict(list)
        for order, rep, orig, shown in runs:
            by_order[order].append(orig)
            if shown in ("X", "Y"):
                pos_bias[jid][shown] += 1
        for order, labels in by_order.items():
            if len(labels) >= 2:
                stability[jid].append(Counter(labels).most_common(1)[0][1] / len(labels))
        all_labels = [o for _, _, o, _ in runs]
        maj_all = majority(all_labels)
        maj_o, maj_s = majority(by_order.get("original", [])), majority(by_order.get("swapped", []))
        definite = ("X", "Y", "TIE")
        pos_cons = (maj_o == maj_s) if (maj_o in definite and maj_s in definite) else None
        group, cond = condition_of(maj_all, pinfo)
        consensus[(jid, pair, qid)] = cond
        cons_rows.append({
            "judge": jid, "pair": pair, "form": pinfo["form"], "project": pinfo["project"], "question_id": qid,
            "story_type": QINFO[qid]["story_type"], "characteristic": QINFO[qid]["characteristic"],
            "n_runs": len(all_labels), "majority_original_order": maj_o, "majority_swapped_order": maj_s,
            "position_consistent": "" if pos_cons is None else pos_cons,
            "consensus_code": maj_all, "consensus_group": group, "consensus_condition": cond,
            "share_agreeing": round(Counter(all_labels)[maj_all] / len(all_labels), 3) if maj_all in definite else "",
        })
    with open(out / "judge_consensus.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(cons_rows[0]))
        w.writeheader()
        w.writerows(cons_rows)

    jids = [j for j in judges if j in run_stats]
    L = [f"# LLM-as-a-judge summary — run '{args.run}'", "", f"Generated {now()}.", ""]

    L += ["## Runs", "", "| Judge | Weights | Valid runs | Invalid runs | Cost (USD) |", "|---|---|---|---|---|"]
    for j in jids:
        s = run_stats[j]
        L.append(f"| {j} | {judges[j].get('weights')} | {s['valid']} | {s['invalid']} | {s['cost_micro'] / 1e6:.2f} |")

    L += ["", "## Stability", "",
          "Position consistency: share of items whose majority in the original order equals the majority in the swapped order.",
          "First-position share: share of Team X among X/Y answers as displayed (50% means no position preference across both orders).",
          "Repetition agreement: mean share of repetitions that match the modal answer within the same order.", "",
          "| Judge | Position consistency | Items compared | First-position share | Repetition agreement |", "|---|---|---|---|---|"]
    for j in jids:
        rows = [r for r in cons_rows if r["judge"] == j and r["position_consistent"] != ""]
        pc = sum(1 for r in rows if r["position_consistent"]) / len(rows) if rows else None
        pb = pos_bias[j]
        fp = pb["X"] / (pb["X"] + pb["Y"]) if (pb["X"] + pb["Y"]) else None
        st = sum(stability[j]) / len(stability[j]) if stability[j] else None
        L.append(f"| {j} | {fmt(pc, True)} | {len(rows)} | {fmt(fp, True)} | {fmt(st, True)} |")

    conds = ["mapping", "ad hoc", "no preference", "no majority", "unanswered"]
    L += ["", "## Consensus preferences by condition", "",
          "Consensus = label chosen by more than half of all valid runs of a judge (both orders, all repetitions).", "",
          "| Judge | " + " | ".join(conds) + " | Items |", "|---|" + "---|" * (len(conds) + 1)]
    for j in jids:
        c = Counter(r["consensus_condition"] for r in cons_rows if r["judge"] == j)
        L.append(f"| {j} | " + " | ".join(str(c[k]) for k in conds) + f" | {sum(c.values())} |")

    L += ["", "### By characteristic (mapping / ad hoc / no preference)", "",
          "| Judge | " + " | ".join(CRITERIA) + " |", "|---|" + "---|" * len(CRITERIA)]
    for j in jids:
        cells = []
        for crit in CRITERIA:
            c = Counter(r["consensus_condition"] for r in cons_rows if r["judge"] == j and r["characteristic"] == crit)
            cells.append(f"{c['mapping']} / {c['ad hoc']} / {c['no preference']}")
        L.append(f"| {j} | " + " | ".join(cells) + " |")

    L += ["", "### By pair (mapping / ad hoc / no preference)", "",
          "| Judge | " + " | ".join(f"{p} (form {cfg['pairs'][p]['form']})" for p in cfg["pairs"]) + " |",
          "|---|" + "---|" * len(cfg["pairs"])]
    for j in jids:
        cells = []
        for p in cfg["pairs"]:
            c = Counter(r["consensus_condition"] for r in cons_rows if r["judge"] == j and r["pair"] == p)
            cells.append(f"{c['mapping']} / {c['ad hoc']} / {c['no preference']}")
        L.append(f"| {j} | " + " | ".join(cells) + " |")

    definite_c = ("mapping", "ad hoc", "no preference")
    items = sorted({(p, q) for (_, p, q) in consensus})
    L += ["", "## Agreement between judges (consensus labels)", "",
          "Cohen's kappa over items where both judges have a consensus label; percent agreement in parentheses.", "",
          "| | " + " | ".join(jids) + " |", "|---|" + "---|" * len(jids)]
    for a in jids:
        cells = []
        for b in jids:
            if a == b:
                cells.append("–")
                continue
            pairs_ab = [(consensus.get((a, p, q)), consensus.get((b, p, q))) for p, q in items]
            pairs_ab = [(x, y) for x, y in pairs_ab if x in definite_c and y in definite_c]
            if not pairs_ab:
                cells.append("–")
                continue
            xa, xb = zip(*pairs_ab)
            agree = sum(x == y for x, y in pairs_ab) / len(pairs_ab)
            cells.append(f"{fmt(cohen_kappa(xa, xb))} ({fmt(agree, True)}, n={len(pairs_ab)})")
        L.append(f"| {a} | " + " | ".join(cells) + " |")

    if not args.human:
        args.human, notes = human_specs_from_env(cfg)
        for n in notes:
            print(n)
    if args.human:
        votes, counts = load_human(cfg, args.human)
        h_rows, human_cons = [], {}
        for (pair, qid), codes in sorted(votes.items()):
            pinfo = cfg["pairs"][pair]
            maj = majority(codes)
            _, cond = condition_of(maj, pinfo)
            human_cons[(pair, qid)] = cond
            c = Counter(codes)
            h_rows.append({"pair": pair, "form": pinfo["form"], "question_id": qid,
                           "characteristic": QINFO[qid]["characteristic"], "story_type": QINFO[qid]["story_type"],
                           "n_answers": c["X"] + c["Y"] + c["TIE"], "X": c["X"], "Y": c["Y"], "TIE": c["TIE"],
                           "majority_code": maj, "majority_condition": cond})
        with open(out / "human_items.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(h_rows[0]))
            w.writeheader()
            w.writerows(h_rows)
        L += ["", "## Agreement with human experts", "",
              "Respondents per form: " + ", ".join(f"{k}={v}" for k, v in sorted(counts.items())) + ".",
              "Human label per item = answer chosen by more than half of the respondents of that form.", "",
              "| Judge | Cohen's kappa | Percent agreement | Items compared |", "|---|---|---|---|"]
        for j in jids:
            pr = [(consensus.get((j, p, q)), human_cons.get((p, q))) for p, q in items]
            pr = [(x, y) for x, y in pr if x in definite_c and y in definite_c]
            if pr:
                xa, xb = zip(*pr)
                agree = sum(x == y for x, y in pr) / len(pr)
                L.append(f"| {j} | {fmt(cohen_kappa(xa, xb))} | {fmt(agree, True)} | {len(pr)} |")
            else:
                L.append(f"| {j} | – | – | 0 |")
        hc = Counter(v for v in human_cons.values())
        L += ["", "Human majority by condition: " + ", ".join(f"{k}={hc[k]}" for k in conds if hc[k]) + "."]

    (out / "summary.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"Wrote {out / 'decoded_long.csv'}, {out / 'judge_consensus.csv'} and {out / 'summary.md'}")
    if args.human:
        print(f"Wrote {out / 'human_items.csv'}")


def main():
    load_dotenv(os.environ.get("ENV_FILE") or HERE / ".env")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", default=str(HERE / "config.json"))
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("config", "build", "run", "status", "analyze"):
        p = sub.add_parser(name)
        p.add_argument("--run", default=env("RUN_NAME", "main"), help="Run name (folder under runs/). Default: RUN_NAME or main.")
        if name in ("run", "status"):
            p.add_argument("--reps", type=int, help="Repetitions per configuration (default from config).")
        if name == "run":
            p.add_argument("--judges", help="Comma-separated judge ids, or 'all'.")
            p.add_argument("--pairs", help="Comma-separated pairs (M1,M2,N1,N2), or 'all'.")
            p.add_argument("--orders", help="original, swapped, or both (comma-separated).")
            p.add_argument("--workers", type=int, help="Parallel requests.")
            p.add_argument("--mock", action="store_true", help="Fake judge; no API calls.")
            p.add_argument("--force", action="store_true", help="Redo runs that are already valid.")
        if name == "analyze":
            p.add_argument("--human", nargs="*", help="Human responses: FORM=path.csv (e.g. A=form_A.csv).")
    args = ap.parse_args()
    cfg = load_config(args.config)
    {"config": cmd_config, "build": cmd_build, "run": cmd_run, "status": cmd_status,
     "analyze": cmd_analyze}[args.cmd](cfg, args)


if __name__ == "__main__":
    main()
