from team_tasker.manager import TaskManager

def test_add_task():
    manager = TaskManager()
    manager.add_task("Test Task")
    assert len(manager.tasks) == 1
    assert manager.tasks[0].title == "Test Task"
