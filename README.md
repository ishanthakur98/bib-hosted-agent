# Dummy Hosted Agent Security Demo

A deliberately insecure, local-only FastAPI application for demonstrating
Microsoft Defender for DevOps scanning of a GitHub repository. It is not a real
AI agent: `/chat` echoes input with a prefix and never calls an LLM or Azure.

**Nothing is deployed. All secrets are fake. Do not deploy this repository or
use its code, dependencies, Dockerfile, or infrastructure in production.**
The unsafe tools are scanning fixtures only; neither endpoint calls them.

## Repository

```text
.
|-- .github/workflows/ci.yml
|-- agent/
|   |-- main.py
|   |-- tools.py
|   |-- config.py
|   `-- requirements.txt
|-- tests/test_agent.py
|-- infra/main.bicep
|-- Dockerfile
|-- .gitignore
`-- README.md
```

## Intentional Findings

Each fixture is labelled `# DEMO-ONLY: intentional finding`. Bicep uses
`// # DEMO-ONLY: intentional finding` to keep valid Bicep syntax.

| Fixture                  | Finding                                                                         | Expected scanner                                                                             |
| ------------------------ | ------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| `agent/config.py`        | Fake hardcoded API key and connection string                                    | GitHub secret scanning / Defender secret detection, subject to supported patterns            |
| `agent/tools.py`         | User input passed to `subprocess.run(..., shell=True)`                          | Bandit B602 (also B404 for subprocess import)                                                |
| `agent/tools.py`         | `eval()` on user input                                                          | Bandit B307                                                                                  |
| `agent/requirements.txt` | Requests 2.25.1: CVE-2023-32681                                                 | Trivy dependency scanning; Dependabot alerts if enabled                                      |
| `agent/requirements.txt` | PyYAML 5.3.1: CVE-2020-14343                                                    | Trivy dependency scanning; Dependabot alerts if enabled                                      |
| `agent/requirements.txt` | Jinja2 2.11.3: CVE-2020-28493                                                   | Trivy dependency scanning; Dependabot alerts if enabled                                      |
| `Dockerfile`             | Old `python:3.9-slim` base (Python 3.9 is end-of-life)                          | Trivy image scanning, when the image is explicitly scanned; findings depend on base contents |
| `Dockerfile`             | Runs as root; missing health check                                              | Checkov / supported Dockerfile policy scanners                                               |
| `Dockerfile`             | Broad `COPY . .`, dependency installation in image                              | Dockerfile policy review; exact detection depends on scanner rules                           |
| `infra/main.bicep`       | Storage public network access enabled; public blobs allowed; HTTPS not required | Template Analyzer / Checkov                                                                  |
| `infra/main.bicep`       | Container registry admin credentials enabled                                    | Template Analyzer / Checkov                                                                  |

These are detection candidates, not a guarantee that every scanner flags every
fixture. The fake credentials are deliberately invalid and may be ignored by
pattern-based secret scanners. MSDO's CredScan secret scanner was retired;
`categories: 'code,secrets,IaC,containers'` does not itself enable GitHub secret
scanning. Enable supported secret scanning separately in repository settings.
Tool availability and vulnerability databases change over time.

## CI Pipeline

Pushes and pull requests targeting `main`, plus manual `workflow_dispatch`, run:

1. **build-and-test** (Ubuntu): Python 3.11, pip cache, install, flake8, pytest.
2. **docker-build** (Ubuntu): build `dummy-agent:<commit SHA>` locally, save a
   tarball, upload `dummy-agent-image`. The image is never run or pushed in CI.
3. **security-scan** (Windows): Microsoft Security DevOps (MSDO), upload SARIF
   to GitHub Security and `.gdn/` as `msdo-results`, including hidden files.
4. **summary** (Ubuntu): report all job statuses, even if a preceding job fails.

Build, lint, tests, and image creation are blocking. Scanning and result uploads
are non-blocking so intentional findings or restricted SARIF permissions do not
break the demo. Review the raw scan outcome, logs, and artifacts: a green security
job does not prove scanners succeeded or uploads were accepted.

Jobs use separate runners. The Windows scan inspects repository sources and
Dockerfile, not the Ubuntu runner's built image. Container categories do not
guarantee an image vulnerability scan; the image tarball is provided for separate
offline inspection. This pipeline does not add another image-scanning job.

Actions are pinned to major versions except the explicitly requested
`microsoft/security-devops-action@latest`. All jobs have the requested
`contents: read`, `security-events: write`, `id-token: write`, and `actions: read`
permissions. The OIDC permission is unused; no login or token exchange occurs.
There are no Azure logins, Azure CLI commands, registry pushes, deployments,
environment protection rules, or workflow secret references.

For the Defender view, this repository must already be connected to Defender for
Cloud's DevOps security integration. GitHub code scanning must be available and
enabled to accept SARIF (private repositories may require GitHub Code Security).
Fork pull requests can have restricted write permissions; inspect the upload
logs. Connecting Defender or changing GitHub settings is outside this repository
and is not performed by CI.

## Local Verification

Use an isolated Python 3.11 virtual environment. The legacy PyYAML release needs
compatible build tools installed first and disabled build isolation. Optional
native extensions may need a compiler; pure-Python fallback is supported.

```sh
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows PowerShell instead:
# .\.venv\Scripts\Activate.ps1
python -m pip install setuptools==75.8.0 wheel==0.45.1 Cython==0.29.37
python -m pip install --no-build-isolation -r agent/requirements.txt
python -m flake8 agent tests
python -m pytest tests -q
```

Optional local-only server, bound to loopback on port 8088:

```sh
python -m agent.main
```

`GET http://127.0.0.1:8088/health` returns `{"status": "ok"}`.
`POST http://127.0.0.1:8088/chat` with `{"message": "Hello"}` returns
`{"reply": "Demo agent: Hello"}`. Invalid message payloads return HTTP 422.
`AGENT_HOST`, `AGENT_PORT`, and `AGENT_REPLY_PREFIX` override app defaults.
The fake credential constants are unused and contact no service.

Build only, without running or publishing the intentionally insecure image:

```sh
docker build --tag dummy-agent:demo .
docker save --output dummy-agent.tar dummy-agent:demo
```

The Dockerfile intentionally uses Python 3.9 while application CI uses 3.11.
No `USER`, `HEALTHCHECK`, or `.dockerignore` is provided, intentionally. Because
`COPY . .` includes the entire context, build from a clean checkout without real
credentials, virtual environments, or local image tarballs in the build context.
Never deploy the Bicep template: it is a static scan fixture only.
