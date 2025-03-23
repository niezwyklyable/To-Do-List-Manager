
import colorama
from colorama import Fore
colorama.init(autoreset=True)

class Task():
    def __init__(self, task_number, target_info, date=None, assigned_day=None, \
                 periodic=False, time=None, task_type=None, active=True):
        self.task_number = task_number # needed to handle the specific task, int type     
        self.target_info = target_info # str type
        self.state = 'to-do' # str type
        self.date = date # str type or None
        self.assigned_day = assigned_day # str type or None
        self.periodic = periodic # boolean type
        self.time = time # str type or None
        self.task_type = task_type # str type or None
        self.active = active # boolean type

    def show_info(self):
        if self.state == 'to-do':
            color = Fore.CYAN
        elif self.state == 'completed':
            color = Fore.BLUE
        # with date
        if self.date:
            # with time
            if self.time:
                if self.task_type:
                    print(f'{color}Task #{self.task_number}: {self.date} - {self.time} - {self.target_info} | [{self.state}] | [{self.task_type}]')
                else:
                    print(f'{color}Task #{self.task_number}: {self.date} - {self.time} - {self.target_info} | [{self.state}]')
            # without time
            else:
                if self.task_type:
                    print(f'{color}Task #{self.task_number}: {self.date} - {self.target_info} | [{self.state}] | [{self.task_type}]')
                else:
                    print(f'{color}Task #{self.task_number}: {self.date} - {self.target_info} | [{self.state}]')
        # without date
        else:
            # with time
            if self.time:
                if self.task_type:
                    print(f'{color}Task #{self.task_number}: {self.time} - {self.target_info} | [{self.state}] | [{self.task_type}]')
                else:
                    print(f'{color}Task #{self.task_number}: {self.time} - {self.target_info} | [{self.state}]')
            # without time
            else:
                if self.task_type:
                    print(f'{color}Task #{self.task_number}: {self.target_info} | [{self.state}] | [{self.task_type}]')
                else:
                    print(f'{color}Task #{self.task_number}: {self.target_info} | [{self.state}]')

    def mark_as_completed(self):
        self.state = 'completed'

    def mark_as_to_do(self):
        self.state = 'to-do'

    def change_target_info(self, new_target_info):
        self.target_info = new_target_info

    def get_date(self):
        day, month, year = self.date.split('.')
        return int(day), int(month), int(year)
    
    def get_time(self):
        hours, minutes = self.time.split(':')
        return int(hours), int(minutes)
    