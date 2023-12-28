from ..controller import db , mapper, docker
from controller.config import Config
from controller.util import now
from  time import sleep
from kubernetes import client


Task = mapper.classes.tasks
core_v1_client = client.CoreV1Api()                 
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
                        command=f"sh -c '{task.script}'" ,
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
                    pod = core_v1_client.create_namespaced_pod(
                        namespace=task.namespace,
                        body=client.V1Pod(
                             metadata=client.V1ObjectMeta(
                                  generate_name=task.name+"-",
                                  labels={"controller":"anakonda"}
                                  ),                             
                                     spec=client.V1PodSpec(
                                               restart_policy="Never",
                                               containers=[client.V1Container(
                                                    name=task.name,
                                                    command=["sh","-c",task.script],
                                                    image=task.image)])
                        )
                    )
                    while pod.status.phase not in ["Succeeded","Failed"]:
                        pod= core_v1_client.read_namespaced_pod(name=pod.metadata.name, namespace=task.namespace)
                        sleep(3)
                    pod_log=core_v1_client.read_namespaced_pod_log(name=pod.metadata.name, namespace=task.namespace)
                    core_v1_client.delete_namespaced_pod(name=pod.metadata.name, namespace=task.namespace)
                    if pod.status.phase ==   "Succeeded":
                        task.status = "success"                        
                    else :
                        task.status = "failed"
                    task.result=pod_log
                    task.last_update_at = now()
                    db.commit()

