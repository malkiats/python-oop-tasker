# python-oop-tasker

- dataclass Task: a simple OOP model for a task. Fields, defaults and a to_dict / from_dict for JSON serialization.
- Status enum: avoids magic strings for task states.
- load_tasks / save_tasks: persistent storage using tasks.json. Simple and fast for prototyping.
- Typer (app = typer.Typer()): creates CLI commands via @app.command(). Typer reads function signature & type hints to generate help and parse arguments automatically.
- rich.Table: pretty table output for list.


==================================

Run & try examples (in the terminal)

Create a task:
python tasker.py add "Fix login bug" -d "Investigate 500s in auth service" -a alice --due 2025-09-01 --tags bug,backend

List tasks:
python tasker.py list

Show details (use first 8 chars of id printed in list):
python tasker.py show 1a2b3c4d

Mark complete:
python tasker.py complete 1a2b3c4d

Remove (with confirmation):
python tasker.py remove 1a2b3c4d

# or skip confirm
python tasker.py remove 1a2b3c4d -y

Try python tasker.py --help and python tasker.py add --help to see auto-generated help — very useful.