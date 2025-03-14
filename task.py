
class Task():
    def __init__(self, task_number, target_info):
        self.task_number = task_number # needed to handle the specific task      
        self.target_info = target_info

    def show_info(self):
        print(f'Task no. {self.task_number}: {self.target_info}')
