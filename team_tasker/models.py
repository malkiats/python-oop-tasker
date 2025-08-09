"""
contains our Task class — basically the “blueprint” for making a task.
"""
from datetime import datetime       # lets us store the exact time the task was created.
from typing import Optional         # means the value can be something or None (like “no value”).

"""
from typing import Optional

x: Optional[str] = "Hello"  # OK
x = None                    # also OK
"""

class Task:
    """method (constructor)"""
    def __init__(self, title: str, description: str = "", due_date: Optional[str] = None):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.created_at = datetime.now()
        self.completed = False

    """
    __init__ runs automatically when we make a new task.
    self → represents this specific task object.
    Parameters:
        title: str → required (e.g., "Buy milk")
        description: str = "" → optional, default is empty string.
        due_date: Optional[str] = None → optional, default is None.
    """

    def mark_done(self):
        self.completed = True
    """When called, this flips the completed flag to True."""
        
    def __repr__(self):
        return f"<Task {self.title} - {'Done' if self.completed else 'Pending'}"
    """Controls what Python shows if we print(task) or look at it in the debugger.
        Uses a ternary expression:
        'Done' if self.completed else 'Pending'
    """

    """
    Tips for OOP in Python
    __init__ is your object setup code.
    self is like saying “this object’s data”.
    Use __repr__ for a developer-friendly display.
    Make methods (mark_done) for actions that belong to the object.
    """
    
        
        

