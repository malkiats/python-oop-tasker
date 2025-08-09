#!/usr/bin/env python3
"""
tasker.py — minimal task manager CLI using Typer + dataclasses + JSON storage.
Commands: add, list, show, complete, remove
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
from pathlib import Path
import json, uuid, datetime
import typer
from rich.table import Table
from rich.console import Console

app = typer.Typer()
console = Console()
DATA_FILE = Path("tasks.json")  # simple storage in project folder

class Status(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"

@dataclass
class Task:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    description: str = ""
    assignee: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())
    due_date: Optional[str] = None
    status: Status = Status.TODO
    tags: List[str] = field(default_factory=list)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "assignee": self.assignee,
            "created_at": self.created_at,
            "due_date": self.due_date,
            "status": self.status.value,
            "tags": self.tags,
        }

    @staticmethod
    def from_dict(d):
        return Task(
            id=d["id"],
            title=d["title"],
            description=d.get("description", ""),
            assignee=d.get("assignee"),
            created_at=d.get("created_at", datetime.datetime.utcnow().isoformat()),
            due_date=d.get("due_date"),
            status=Status(d.get("status", "TODO")),
            tags=d.get("tags", []),
        )

def load_tasks() -> List[Task]:
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return [Task.from_dict(d) for d in data]

def save_tasks(tasks: List[Task]):
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump([t.to_dict() for t in tasks], f, indent=2)

@app.command()
def add(
    title: str = typer.Argument(...),
    description: str = typer.Option("", "-d", "--description"),
    assignee: Optional[str] = typer.Option(None, "-a", "--assignee"),
    due: Optional[str] = typer.Option(None, "--due"),
    tags: str = typer.Option("", "--tags", help="comma separated tags"),
):
    """Add a new task."""
    tasks = load_tasks()
    tags_list = [t.strip() for t in tags.split(",") if t.strip()]
    task = Task(title=title, description=description, assignee=assignee, due_date=due, tags=tags_list)
    tasks.append(task)
    save_tasks(tasks)
    console.print(f"[green]Created[/green] task [bold]{task.title}[/bold] id: {task.id}")

@app.command("list")
def list_tasks(
    status: Optional[Status] = typer.Option(None, "--status", help="Filter by status"),
    assignee: Optional[str] = typer.Option(None, "--assignee", help="Filter by assignee"),
):
    """List tasks (optional filters)."""
    tasks = load_tasks()
    if status:
        tasks = [t for t in tasks if t.status == status]
    if assignee:
        tasks = [t for t in tasks if t.assignee == assignee]

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("id", style="dim", width=8)
    table.add_column("title")
    table.add_column("status")
    table.add_column("assignee")
    table.add_column("due")
    table.add_column("tags")

    for t in tasks:
        table.add_row(t.id[:8], t.title, t.status.value, t.assignee or "-", t.due_date or "-", ", ".join(t.tags))

    console.print(table)

@app.command()
def show(task_id: str = typer.Argument(...)):
    """Show task details (task id or first 8 chars)."""
    tasks = load_tasks()
    t = next((x for x in tasks if x.id.startswith(task_id) or x.id == task_id), None)
    if not t:
        typer.echo("Task not found.")
        raise typer.Exit(code=1)
    console.print(f"[bold]{t.title}[/bold] (id: {t.id})")
    console.print(f"Status: {t.status.value}")
    console.print(f"Assignee: {t.assignee or '-'}")
    console.print(f"Due: {t.due_date or '-'}")
    console.print(f"Tags: {', '.join(t.tags) or '-'}")
    console.print("\nDescription:")
    console.print(t.description or "-")

@app.command()
def complete(task_id: str = typer.Argument(...)):
    """Mark a task DONE."""
    tasks = load_tasks()
    t = next((x for x in tasks if x.id.startswith(task_id) or x.id == task_id), None)
    if not t:
        typer.echo("Task not found.")
        raise typer.Exit(code=1)
    t.status = Status.DONE
    save_tasks(tasks)
    console.print(f"[green]Completed[/green] {t.title}")

@app.command()
def remove(task_id: str = typer.Argument(...), yes: bool = typer.Option(False, "--yes", "-y")):
    """Remove a task (use --yes to skip confirmation)."""
    tasks = load_tasks()
    t = next((x for x in tasks if x.id.startswith(task_id) or x.id == task_id), None)
    if not t:
        typer.echo("Task not found.")
        raise typer.Exit(code=1)
    if not yes and not typer.confirm(f"Delete '{t.title}'?"):
        typer.echo("Aborted.")
        raise typer.Exit()
    tasks = [x for x in tasks if x.id != t.id]
    save_tasks(tasks)
    console.print(f"[red]Removed[/red] {t.title}")

if __name__ == "__main__":
    app()
