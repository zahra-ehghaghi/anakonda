from ..controller import db , mapper, docker
from controller.config import Config
from controller.util import now
from  time import sleep


Task = mapper.classes.tasks

class TaskJobController:
   
     def run_task(task_id):          
          print(task_id)
          task = db.query(Task).get(task_id)
          if task is not None:
              if task.status != "new":
                  pass
              task.status = "processing"
              task.last_update_at = now()
              db.commit()
              if task.runtime not in Config.AVAILABLE_RUNTIMES:
                   task.status = "failed"
                   task.last_update_at = now()
                   db.commit()
              if task.runtime == "docker" :
                   container= docker.containers.run(
                        image=task.image,
                        command=task.script,
                        detach = True,
                        tty=False
                   )
                   container_status = docker.containers.get(container.id).attrs["State"]["Running"]
                   while container_status:
                        sleep(1)
                        container_status = docker.containers.get(container.id).attrs["State"]["Running"]
                   container_exit_code =docker.containers.get(container.id).attrs["State"]["ExitCode"]
                   container_result =docker.containers.get(container.id).logs().decode("utf-8")
                   container.remove()
                   if container_exit_code == 0:
                        task.status = "success"
                   else:
                        task.status = "failed"
                   task.last_update_at = now()
                   task.result = container_result
                   db.commit()
              if task.runtime == "kubernetes" :
                   pass
