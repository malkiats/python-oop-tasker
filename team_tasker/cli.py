import typer
from .manager import TaskManager

app = typer.Typer()
manager = TaskManager()

@app.command()
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
