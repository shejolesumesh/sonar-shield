# SONAR-SHIELD Backend

FastAPI service implementing sonar image ingestion, preprocessing, AI detection
(demo or PyTorch), evidence/risk/priority engines, expert feedback, and reporting.

## Requirements

**Use Python 3.11 or 3.12.** These are the versions this project is tested against.
Very new Python releases (e.g. 3.13/3.14) can force `pip` to build `numpy`/`Pillow`
from source instead of installing a prebuilt wheel, which commonly fails on Windows
without a modern C/C++ toolchain installed. If `python --version` shows something
newer than 3.12 and you hit build errors, install Python 3.12 from
https://www.python.org/downloads/ and create your virtual environment with it
specifically, e.g. on Windows: `py -3.12 -m venv venv`.

## Run

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux
pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Test

```bash
pytest -q
```

Interactive API docs: http://localhost:8000/docs
