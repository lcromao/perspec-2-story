# LLM-as-a-judge protocol — Data and Model Stories expert evaluation

This folder runs four LLM judges on the same questionnaire answered by the human experts (forms A–D) and compares their answers.

## Contents

| Path | Purpose |
|---|---|
| `prompts/01_System_Prompt_EN.md` | Judge role, criteria, decision rules, JSON output contract |
| `prompts/02_Project_Context_EN.md` | Shared context sent to the judge (answer options, question IDs) |
| `prompts/03_Execution_Prompt_EN.md` | Task instruction, sent last |
| `contexts/02_Context_<pair>_EN.md` | One form per pair (M1, M2, N1, N2), same content as forms A–D |
| `.env.example` | Template with every setting: endpoint, file paths, run options, each judge (id, model, provider, schema, effort, tokens), pilot, smoke test, human CSV paths. Copy it to `.env` and fill it in |
| `.env` | Your settings (created from `.env.example`). Holds the API key: not to be shared or committed |
| `config.json` | Defaults, and the pairs with the private X/Y key (the only part not set in `.env`, because it defines the study design). Values in `.env` override the defaults |
| `judge_runner.py` | Runner: config, build, run, status, analyze (Python 3.9+, standard library only) |
| `run.sh` | The usual sequence of commands (loads `.env`) |
| `.gitignore` | Keeps `.env` and `runs/` out of git |

## Run protocol

These rules were previously inside the shared context. They are for whoever runs the study and are never sent to the judges.

- Each call evaluates exactly one pair in a fresh context. The messages are the system prompt, then one user message with the shared context, the selected pair context and the execution prompt, in that order.
- Team X and Team Y labels are local to each form. The key that links them to groups and conditions lives only in `config.json` and is used only in the analysis.
- Forms and pairs: A = M1, B = M2, C = N1, D = N2.

  | Pair | Form | Team X | Team Y | Mapping group |
  |---|---|---|---|---|
  | M1 | A | Group A (mapping) | Group B (ad hoc) | A |
  | M2 | B | Group D (ad hoc) | Group C (mapping) | C |
  | N1 | C | Group B (mapping) | Group A (ad hoc) | B |
  | N2 | D | Group C (ad hoc) | Group D (mapping) | D |

- Each run produces 28 preference answers. With 4 judges, 4 pairs, 2 orders and 3 repetitions there are 96 runs and 2,688 answers. These are repeated judgments by 4 judges, not independent participants.
- Question IDs repeat across forms, so the pair ID is always kept with the results.

## Controls added by the runner

| Control | How |
|---|---|
| Position bias | Each pair also runs in the `swapped` order: the original Team Y content is shown under the Team X label and vice versa, with labels, page order and questions unchanged. Answers are mapped back before analysis. |
| Repetitions | Every configuration runs `reps` times (default 3). Temperature is not set, because reasoning is enabled for all judges. |
| Output format | The judge returns one JSON object with one required key per question (`1.1.a` … `7.4.a`), so a question cannot be repeated or skipped. The runner sends this JSON schema as `response_format` (strict) and also validates locally: all 28 keys, allowed answers, explanations, coverage, input issues. Invalid outputs are re-run up to `max_invalid_retries` times; every attempt is stored. |
| Same conditions for all judges | Same prompts, same `reasoning.effort` and `max_tokens`. The returned model, provider, usage and cost are stored for each attempt. |
| Open-weight provider | DeepSeek is pinned to one full-precision provider (Together; `provider.order`, `allow_fallbacks: false`) so that quantization does not change between calls. DeepSeek's own endpoint is not used: it does not support the JSON schema and may train on prompts. |
| Data policy | Every request sends `provider.data_collection: deny` (only providers that do not store or train on prompts, since the stories were written by participants) and `require_parameters: true` (only providers that support the JSON schema and reasoning). |
| Traceability | Each record stores a SHA-256 of the exact messages, timestamps, the raw response and the reasoning text when the API returns it. |

## Before the first real run

1. Create `.env` from the template (`cp .env.example .env`) and fill it in:
   - `OPENROUTER_API_KEY`: a key used only for this study, with a credit limit. All calls then appear under that key in the OpenRouter activity log, named by `OPENROUTER_APP_TITLE`. Each attempt in `raw/` stores the OpenRouter `generation_id`, which matches the entry in the activity log.
   - Judges: `qwen/qwen3.8-max-0902` is served as an API-only model. If the study needs two open-weight judges, replace `JUDGE_QWEN_MODEL` with the open-weight Qwen3.8 variant listed on OpenRouter and set `JUDGE_QWEN_WEIGHTS=open`.
   - Confirm `JUDGE_DEEPSEEK_PROVIDER` on the model's Providers tab on OpenRouter. If the slug is wrong, the call fails and the error is stored in `raw/`; fix it and run again.
   - If a model rejects `response_format`, set its `..._STRUCTURED_OUTPUT=false`. The prompt still asks for JSON and the local validation still applies.
2. Check the effective settings: `sh run.sh config` (the key is shown only as set or missing).
3. Run the smoke test (fake judge, no API calls): `sh run.sh smoke`.
4. Run the pilot: `sh run.sh pilot`. By default it makes one call (pair M1, original order, 1 repetition; see `PILOT_*` in `.env`) with the test judge `nemotron-test` (`nvidia/nemotron-3-ultra-550b-a55b:free`), which is disabled for the study and never enters `run`, `status` or the analysis of `main`. Read the output in `runs/pilot/readable/`.
   - Free endpoints have daily call limits and may log or train on prompts. If OpenRouter answers that no endpoint matches your data policy, allow free endpoints in the OpenRouter privacy settings.
   - To check that a study judge accepts the JSON schema before the full run: `PILOT_JUDGE=deepseek-v4.1-flash sh run.sh pilot`.
5. Run the study: `sh run.sh full`, then `sh run.sh status`.

## Commands

```sh
sh run.sh config     # effective settings from config.json + .env
sh run.sh build      # writes runs/main/prompts/<pair>_<order>.txt for inspection
sh run.sh smoke      # whole pipeline with a fake judge, no API calls
sh run.sh pilot      # one real call with PILOT_JUDGE (default: nemotron-test)
sh run.sh full       # full study: enabled judges x 4 pairs x ORDERS x REPS
sh run.sh status     # valid / invalid / missing runs and cost per judge
sh run.sh analyze    # analysis; uses the human CSVs listed in .env when the files exist
sh run.sh figures    # Likert figures (PDF + PNG) in runs/<run>/analysis/figures (installs matplotlib in .venv)
```

The same commands are available directly, for example `python3 judge_runner.py run --judges sonnet-5.5 --pairs N2`. Running `run` again only redoes runs that are missing or invalid; `--force` redoes everything. The human CSVs are the response sheets of forms A–D downloaded as CSV (File > Download > CSV), saved at the paths in `HUMAN_FORM_A` to `HUMAN_FORM_D` (by default `human/form_A.csv` to `human/form_D.csv`).

## Outputs (`runs/<run>/`)

| Path | Content |
|---|---|
| `raw/<judge>/<pair>_<order>_r<rep>.json` | Request metadata, every attempt (raw response, usage, errors) and the validated JSON |
| `readable/<judge>/<pair>_<order>_r<rep>.md` | The answers as Markdown tables, labels as displayed to the judge |
| `analysis/decoded_long.csv` | One row per answer: displayed answer, original label, preferred group and condition, explanation |
| `analysis/judge_consensus.csv` | One row per judge x pair x question: majority per order, position consistency, consensus label |
| `analysis/human_items.csv` | Human answer counts and majority per question (when the human CSVs are available) |
| `analysis/summary.md` | Runs and cost, stability, preferences by condition, agreement between judges and with the experts |

Definitions used in `summary.md`:

- Consensus of a judge: the label chosen by more than half of its valid runs for that question, both orders and all repetitions. Otherwise "no majority".
- Position consistency: share of questions whose majority in the original order equals the majority in the swapped order.
- First-position share: share of Team X among the X/Y answers as displayed. Since the swapped order balances the content, values far from 50% indicate position bias.
- Human label: the answer chosen by more than half of the respondents of that form.
- Agreement: Cohen's kappa and percent agreement over questions where both sides have a label (mapping, ad hoc or no preference).

In swapped runs, the explanations refer to the labels as displayed. `decoded_long.csv` marks these rows in `labels_swapped_in_explanation`.

## Note for the paper: differences between the judges' and the experts' instrument

The judges and the experts answered the same questions on the same stories, but under different conditions. This should be reported:

> The LLM judges answered the same 28 preference questions per form as the experts, with the same answer options and quality definitions. Unlike the experts, the judges received operational decision rules (for example, not to prefer a version for its length or for requirement codes, and to separate omissions from incorrect statements), were required to justify every answer, and read the stories as text, whereas the experts saw them as table images. Each judge evaluated each form six times, three in the original Team X/Team Y order and three with the contents swapped, and we used the majority answer across these runs. The judges' answers therefore indicate how the stories are assessed under explicit guidance, and the agreement with the experts should be interpreted in this light.

## Where each of the six changes was made

| Change | Where |
|---|---|
| 1. Defects inside stories are judged, not reported as input issues | System prompt (Evidence and input handling) and execution prompt |
| 2. Position bias | Runner: `swapped` order and mapping back in `analyze` |
| 3. Different instrument for judges and experts | This README (note for the paper) |
| 4. Shared context without design details or operator instructions | Shared context trimmed; operator rules moved to this README |
| 5. Robust output format | System prompt (JSON contract), runner (schema, validation, retries, Markdown rendering) |
| 6. Repetitions | Runner: `reps` (default 3) and repetition agreement in `analyze` |
