from ..controller import db , mapper

Task = mapper.classes.tasks

class TaskJobController:
     def run_task1():
              pass
     def run_task(task_id):
          pass
          print(task_id)
          task = db.query(Task).get(task_id)
          if task is not None:
              print(task)