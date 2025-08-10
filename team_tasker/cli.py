"""
typer → library that turns Python functions into terminal commands.
TaskManager → our OOP class from manager.py that stores and manages tasks.
"""
import typer
from .manager import TaskManager

"""
app → the Typer “application” object. This will collect all commands.
manager → one TaskManager instance that holds tasks in memory.
"""
app = typer.Typer()
manager = TaskManager()

@app.command()      # @app.command() → tells Typer: “Make this function a CLI command.”
def add(title: str, description: str = "", due_date: str = None):
    """Add a new task."""
    task = manager.add_task(title, description, due_date)
    typer.echo(f"✅ Task added: {task}")

@app.command()
def list():
    """List all tasks."""
    tasks = manager.list_tasks()
    if not tasks:
        typer.echo("No tasks found.")
        return
    for i, task in enumerate(tasks):
        typer.echo(f"{i}. {task}")

@app.command()
def done(index: int):
    """Mark a task as done by index."""
    if manager.mark_done(index):
        typer.echo(f"✅ Task {index} marked as done.")
    else:
        typer.echo("❌ Invalid index.")

if __name__ == "__main__":
    app()
"""
This means: “If you run this file directly, start the Typer CLI.”
Typer will read all @app.command() functions and make them usable from the terminal.
"""

"""
# python -m team_tasker.cli add "Buy milk"
Python runs cli.py.
app() is called.
Typer sees you used add → runs the add() function.
The function calls manager.add_task(...).
The TaskManager creates a Task object and stores it.
typer.echo() prints confirmation to terminal.
"""