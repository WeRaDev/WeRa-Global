FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

WORKDIR /app

COPY src /app/src
COPY scripts /app/scripts
COPY config /app/config
COPY tests /app/tests
COPY README.md /app/README.md
COPY CONTRIBUTING.md /app/CONTRIBUTING.md
COPY WARP.md /app/WARP.md

RUN mkdir -p /app/runtime

EXPOSE 8765

CMD ["python3", "scripts/run_runtime_gui.py", "--host", "0.0.0.0", "--port", "8765", "--state-path", "/app/runtime/runtime_state.json", "--journal-path", "/app/runtime/runtime_journal.jsonl", "--control-state-path", "/app/runtime/operator_control_state.json", "--audit-path", "/app/runtime/operator_action_audit.jsonl"]
