"""
While models.py defines one task (like a single to-do item),
manager.py defines a TaskManager — something that holds and manages many tasks.

Think of:
Task = one sheet of paper with a to-do
TaskManager = the clipboard holding all the sheets
"""

from typing import List
from .models import Task

"""
List[Task] → says “this will be a list that contains Task objects”.
.models → means we’re importing from the models.py file in the same package.
"""

class TaskManager:
    """This is our clipboard"""
    
    def __init__(self):
        self.tasks: List[Task] = []
    """
    Runs when we create a TaskManager object.
    self.tasks starts as an empty list that will store Task objects.
    example:
        manager = TaskManager()
        print(manager.tasks)  # []
    """

    def add_task(self, title: str, description: str = "", due_date: str = None):
        task = Task(title, description, due_date)
        self.tasks.append(task)
        return task
    """
    Steps:
    Create a new Task using Task(...).
    Append it to self.tasks.
    Return the created task (useful if we want to see or print it immediately).
        manager.add_task("Buy milk", "Get 2 liters")
        print(manager.tasks)
        # [<Task Buy milk - Pending>]

    """
    
    def list_tasks(self):
        return self.tasks
    """Return the list of all tasks stored"""
    

    def mark_done(self, index: int):
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_done()
            return True
        return False
    """
    Takes an index (position in the list — starts from 0).
    Checks: is index valid? (0 <= index < len(self.tasks))
    If valid: calls the task’s .mark_done() method.
    Returns True if done, False if invalid index.
    """
    
    """
    Manager classes keep code organized — you don’t want task-adding logic scattered everywhere.
    This separation means tomorrow we could swap TaskManager to save to a database without touching CLI code.
    Index-based selection is simple but in real apps we might use IDs.
    """