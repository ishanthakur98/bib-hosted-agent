# DEMO-ONLY: intentional finding - old Python base, unlike Python 3.11 CI.
FROM python:3.9-slim

WORKDIR /app

# DEMO-ONLY: intentional finding - copies the entire build context.
COPY . .

# Legacy PyYAML needs compatible build tooling and no build isolation.
RUN python -m pip install --no-cache-dir setuptools==75.8.0 wheel==0.45.1 Cython==0.29.37 \
    && python -m pip install --no-cache-dir --no-build-isolation -r agent/requirements.txt

# DEMO-ONLY: intentional finding - no USER directive; runs as root.
# DEMO-ONLY: intentional finding - no HEALTHCHECK directive.
EXPOSE 8088

CMD ["python", "-m", "uvicorn", "agent.main:app", "--host", "0.0.0.0", "--port", "8088"]