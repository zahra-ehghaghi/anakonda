from anakonda.model import Task 
from anakonda.util import jsonify
from anakonda.schema.apiv1 import TaskSchema
from anakonda.anakonda import db


class TaskController:
    def get_tasks():
        tasks_schema = TaskSchema(many= True)
        tasks = Task.query.all()
        return jsonify(state=tasks_schema.dump(tasks))

    def get_task(task_id):
        return jsonify(status=501, code=101)

    def create_task():
        return jsonify(status=501, code=101)

    def update_task(task_id):
        return jsonify(status=501, code=101)

    def delete_task(task_id):
        return jsonify(status=501, code=101)
