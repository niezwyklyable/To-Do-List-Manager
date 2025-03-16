
import colorama
from colorama import Fore
colorama.init(autoreset=True)

class Task():
    def __init__(self, task_number, target_info):
        self.task_number = task_number # needed to handle the specific task, int type     
        self.target_info = target_info # str type
        self.state = 'to-do'

    def show_info(self):
        if self.state == 'to-do':
            color = Fore.CYAN
        elif self.state == 'completed':
            color = Fore.BLUE
        print(f'{color}Task #{self.task_number}: {self.target_info} | [{self.state}]')

    def mark_as_completed(self):
        self.state = 'completed'

    def mark_as_to_do(self):
        self.state = 'to-do'

    def change_target_info(self, new_target_info):
        self.target_info = new_target_info
