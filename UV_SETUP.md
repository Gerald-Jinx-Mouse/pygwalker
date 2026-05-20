# UV setup for this repo

This repo uses [uv](https://docs.astral.sh/uv/) to manage its Python environment. The virtualenv lives at `.venv/` and the interpreter at:

```
C:\Users\jacob\source\repos\Gerald-Jinx-Mouse\pygwalker\.venv\Scripts\python.exe
```

## 1. Install uv

```powershell
winget install --id=astral-sh.uv -e
```

Or via the standalone installer:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Verify:

```powershell
uv --version
```

## 2. Create the venv

From the repo root:

```powershell
uv venv
```

This creates `.venv/` using a Python interpreter that satisfies `requires-python = ">=3.7"` from `pyproject.toml`. To pin a specific version:

```powershell
uv venv --python 3.12
```

## 3. Install pygwalker + every example's dependencies

The recommended install for working with the examples in this repo:

```powershell
uv pip install "pygwalker[all]" gradio marimo fastapi "uvicorn[standard]"
```

Breakdown:

| Group | Packages | Reason |
| --- | --- | --- |
| `pygwalker[all]` | `pygwalker` + `polars`, `streamlit`, `reflex`, `mini-racer` | Core lib plus declared optional extras |
| `gradio` | `gradio` | Needed by `examples/gradio_demo.py` |
| `marimo` | `marimo` | Needed by `examples/marimo_demo.py` |
| `fastapi`, `uvicorn[standard]` | FastAPI + ASGI server | Needed by `examples/web_server_demo.py` |
| `dash` | (already pulled in transitively, but pin it if you want) | Needed by `examples/dash_demo.py` |

If you only want the core library (no extras, no examples):

```powershell
uv pip install pygwalker
```

## 4. Day-to-day commands

| Task | Command |
| --- | --- |
| List installed packages | `uv pip list` |
| Add a new package | `uv pip install <pkg>` |
| Remove a package | `uv pip uninstall <pkg>` |
| Show the interpreter path | `uv python find` |
| Run a script with the venv | `uv run python path/to/script.py` |
| Run a script directly | `& .\.venv\Scripts\python.exe path\to\script.py` |

## 5. Running the examples

All example scripts live in `examples/`. Launch them with the venv interpreter:

```powershell
& .\.venv\Scripts\python.exe .\examples\dash_demo.py
```

Each web demo binds to a local port — watch the terminal output for the URL (e.g. Dash prints `Dash is running on http://127.0.0.1:8050/`). Stop the server with `Ctrl+C`.

## 6. Gotcha — do not run `python -c "import pygwalker"` from the repo root

Because the repo root contains a `pygwalker/` source directory, Python's default `sys.path` will pick up the **source tree** instead of the installed package when you run an interactive command from the repo root. The source tree is missing the built JS bundle (`pygwalker/templates/dist/pygwalker-app.iife.js`), which causes:

```
FileNotFoundError: ...pygwalker\templates\dist\pygwalker-app.iife.js
```

Two safe ways to avoid it:

- Run scripts from anywhere outside the repo root (the `examples/` folder is fine — `sys.path[0]` becomes the script's directory).
- Or run via `uv run`, which sets the working directory appropriately:

  ```powershell
  uv run python -c "import pygwalker; print(pygwalker.__version__)"
  ```

If you actually want to develop against the local source, you'll need to build the JS bundle first (`cd app; npm install; npm run build`) before doing `uv pip install -e .`.

## 7. VS Code interpreter

Point VS Code at the venv so the Python extension uses the same interpreter:

1. `Ctrl+Shift+P` → **Python: Select Interpreter**
2. Choose `.\.venv\Scripts\python.exe`
