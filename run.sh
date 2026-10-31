#!/usr/bin/env sh
# Usual sequence for the LLM-as-a-judge study. Run the steps one at a time:
#   sh run.sh config | build | smoke | pilot | full | status | analyze | figures
# All settings (API key, models, reps, pilot, paths...) live in .env.
set -e
cd "$(dirname "$0")"
ENV_FILE=${ENV_FILE:-.env}

# Load .env without overriding variables already set in the shell, so that
# "PILOT_JUDGE=deepseek-v4.1-flash sh run.sh pilot" wins over the value in .env.
load_env() {
  [ -f "$1" ] || return 0
  while IFS= read -r line || [ -n "$line" ]; do
    case "$line" in ''|\#*) continue ;; esac
    line=${line#export }
    key=${line%%=*}
    case "$key" in ''|*[!A-Za-z0-9_]*) continue ;; esac
    eval "already=\${$key+x}"
    [ -n "$already" ] || eval "export $line"
  done < "$1"
}
load_env "$ENV_FILE"
export ENV_FILE
PY=${PY:-python3}

case "$1" in
  config)  $PY judge_runner.py config ;;
  build)   $PY judge_runner.py build ;;
  smoke)   $PY judge_runner.py run --mock --run "${SMOKE_RUN_NAME:-smoke}" &&
           $PY judge_runner.py analyze --run "${SMOKE_RUN_NAME:-smoke}" ;;
  pilot)   $PY judge_runner.py run --run "${PILOT_RUN_NAME:-pilot}" --judges "${PILOT_JUDGE:-nemotron-test}" \
             --pairs "${PILOT_PAIRS:-M1}" --orders "${PILOT_ORDERS:-original}" --reps "${PILOT_REPS:-1}" ;;
  full)    $PY judge_runner.py run ;;
  status)  $PY judge_runner.py status ;;
  analyze) $PY judge_runner.py analyze ;;
  figures) [ -x .venv/bin/python ] || { python3 -m venv .venv && .venv/bin/pip install -q matplotlib; }
           .venv/bin/python make_figures.py --run "${RUN_NAME:-main}" ;;
  *) echo "Usage: sh run.sh config|build|smoke|pilot|full|status|analyze|figures"; exit 1 ;;
esac
