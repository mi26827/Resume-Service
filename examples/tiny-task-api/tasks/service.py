class TaskService:
    def __init__(self):
        self._tasks = []

    def list_tasks(self):
        return [task.copy() for task in self._tasks]

    def create(self, title):
        if not isinstance(title, str) or not title.strip():
            raise ValueError("title must be a non-empty string")

        task = {"id": len(self._tasks) + 1, "title": title.strip()}
        self._tasks.append(task)
        return task.copy()
