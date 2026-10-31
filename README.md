# From ML-Enabled Systems Concerns to Agile Data and Model Stories: An Exploratory Study

Replication package for the paper submitted to CAIN 2027 (anonymized for blind review).

The study evaluates **PerSpec2Story**, a mapping from the PerSpecML catalog of ML concerns to the
Data and Model Story classes of an agile backlog. Four teams of graduate students specified the
seven Data and Model Stories of a malicious URL classification project: two teams with the mapping
(treatment) and two teams ad hoc (control). The resulting specifications were paired
(mapping vs. ad hoc) and compared, story by story, on four quality characteristics
(completeness, clarity, correctness, consistency) by human experts and by four frontier LLMs
acting as judges.

This repository contains the materials of the **LLM-as-a-judge evaluation (RQ2)**: the exact
prompts and evaluation forms sent to the judges, the runner that calls the models and decodes
their answers, and the script that produces the preference figures.

## Repository layout

| Path | What it is |
|---|---|
| `prompts/` | The three prompt files sent to every LLM judge, in the order: system prompt, shared context, execution prompt (see below). |
| `contexts/` | The four evaluation forms, one per pair of specifications. Each is the participant-facing form rewritten as Markdown: project summary, the Team X and Team Y versions of the seven stories, and the 28 preference questions. |
| `judge_runner.py` | Runner for the whole LLM-as-a-judge protocol: configuration, prompt building, API calls, validation, status and analysis. |
| `make_figures.py` | Produces the Likert-style preference figures (PDF and PNG) from the decoded judge answers. |
| `run.sh` | Shell wrapper that loads `.env` and runs each step of the protocol with one command. |
| `config.json` | Study design and defaults: judges (model, provider, reasoning effort), prompt paths, orders, repetitions, and the private key that links Team X / Team Y to the teams and treatments of each form. |
| `.env.example` | Template of every runtime setting (API key, models, pilot, paths of the human response sheets). Copy to `.env` and fill in; `.env` is git-ignored because it holds the API key. |
| `README_protocol.md` | Detailed protocol: run rules, controls (position bias, repetitions, structured output, provider pinning, data policy), output files and the definitions used in the analysis. |
| `requirements.txt` | Python dependencies. Only `matplotlib` is needed, and only for the figures. The runner uses the standard library. |
| `.gitignore` | Keeps `.env`, `runs/` and virtual environments out of the repository. |

Folders that are created at run time and are **not** committed by default:

| Path | Content |
|---|---|
| `runs/<run>/` | Everything produced by a run: raw API responses, readable Markdown versions of each judgment, and the analysis CSVs and summary (see "Outputs" in `README_protocol.md`). |
| `human/` | The response sheets of the expert forms exported as CSV (`form_A.csv` … `form_D.csv`), used by the analysis to compare judges with experts. |

## Prompts (`prompts/`)

| File | Role |
|---|---|
| `01_System_Prompt_EN.md` | Defines the judge as a Requirements Engineering specialist, the four quality characteristics, the decision rules (judge each characteristic independently, do not prefer a version for its length, separate omissions from incorrect statements, etc.), the evidence rules and the JSON output contract. |
| `02_Project_Context_EN.md` | Shared context for every call: the objective, the questionnaire conventions, the three answer options and the question identifiers (`1.1.a` … `7.4.a`). |
| `03_Execution_Prompt_EN.md` | The task instruction sent last: answer all 28 preference questions with an explanation each and return only the JSON object. |

## Evaluation forms (`contexts/`)

Each file reproduces one expert form. Team X and Team Y are anonymous labels local to each form;
the key that maps them to teams and treatments lives only in `config.json` and is used only in the
analysis. The paper reports the two pairs of the Malicious URL Classification project (M1 and M2).

| File | Pair | Form | Project |
|---|---|---|---|
| `02_Context_M1_EN.md` | M1 | A | M: Malicious URL Classification |
| `02_Context_M2_EN.md` | M2 | B | M: Malicious URL Classification |
| `02_Context_N1_EN.md` | N1 | C | N: NYC Taxi Trip Duration Regression |
| `02_Context_N2_EN.md` | N2 | D | N: NYC Taxi Trip Duration Regression |

## Scripts

### `judge_runner.py`

Python 3.9+, standard library only. Settings come from `config.json`, overridden by `.env`.
Subcommands:

| Command | What it does |
|---|---|
| `config` | Prints the effective settings (API key shown only as set or missing). No API calls. |
| `build` | Writes the exact messages sent for every pair and order to `runs/<run>/prompts/` for inspection. No API calls. |
| `run` | Calls the judges through OpenRouter: judges × pairs × orders × repetitions. Validates every answer against the JSON schema, re-runs invalid outputs, stores raw responses, usage, cost and a SHA-256 of the messages. `--mock` runs the pipeline with a fake judge; `--force` redoes runs that are already valid. |
| `status` | Counts valid, invalid and missing runs and the cost per judge. |
| `analyze` | Decodes Team X/Y back to team and treatment (mapping / ad hoc), maps swapped-order answers back, builds the per-judge consensus labels, computes position consistency, repetition agreement, inter-judge agreement and, when the human CSVs exist, agreement with the experts (percent agreement and Cohen's kappa). Writes `decoded_long.csv`, `judge_consensus.csv`, `human_items.csv` and `summary.md`. |

Controls built into the runner: the `swapped` order shows the Team Y content under the Team X label
(position-bias control); every configuration runs `reps` times (default 3); the JSON schema is sent
as `response_format` and validated locally; the open-weight judge is pinned to one full-precision
provider; every request denies providers that store or train on prompts.

### `make_figures.py`

Reads `runs/<run>/analysis/decoded_long.csv` and writes to `runs/<run>/analysis/figures/`:
an overall figure (all criteria pooled and each criterion, per project), one figure per project with
one bar per story type, one figure per project with one panel per criterion, and `likert_shares.csv`
with the plotted shares. Each bar shows the share of judgments that preferred the ad hoc version,
had no preference, or preferred the mapping version.

### `run.sh`

One command per step of the protocol:

```sh
cp .env.example .env   # then set OPENROUTER_API_KEY
sh run.sh config       # effective settings
sh run.sh build        # write the prompts for inspection
sh run.sh smoke        # whole pipeline with a fake judge, no API calls
sh run.sh pilot        # one real call with the pilot judge
sh run.sh full         # full study: enabled judges x 4 pairs x 2 orders x 3 reps
sh run.sh status       # valid / invalid / missing runs and cost
sh run.sh analyze      # analysis (uses the human CSVs when present)
sh run.sh figures      # Likert figures (creates .venv with matplotlib)
```

## Judges

Configured in `config.json` and `.env.example`, all accessed through OpenRouter with reasoning
effort set to high and the same prompts:

| Judge id | Model | Weights |
|---|---|---|
| `sonnet-5.5` | Claude Sonnet 5.5 (Anthropic) | closed |
| `gpt-6.1-sol` | GPT-6.1 Sol (OpenAI) | closed |
| `qwen3.8-max` | Qwen3.8 Max (Alibaba) | closed |
| `deepseek-v4.1-flash` | DeepSeek V4.1 Flash, pinned to one provider | open |

A fifth entry, `nemotron-test`, is a free model used only for the pilot and never enters the study.

## Reproducing the LLM evaluation

1. Install Python 3.9+ and copy `.env.example` to `.env`; set `OPENROUTER_API_KEY`.
2. Run `sh run.sh smoke` to check the pipeline without API calls.
3. Run `sh run.sh full`, then `sh run.sh status` until every run is valid.
4. Place the expert response sheets in `human/` (or set the `HUMAN_FORM_*` paths in `.env`) and run
   `sh run.sh analyze`.
5. Run `sh run.sh figures` to generate the figures used in the paper.

See `README_protocol.md` for the full run protocol, controls, output formats and the definitions
of consensus, position consistency and agreement used in the analysis.
