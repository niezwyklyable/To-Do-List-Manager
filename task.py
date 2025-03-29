
import colorama
from colorama import Fore
colorama.init(autoreset=True)
import re

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
        # inactive task (periodic without time only)
        if not self.active:
            print(f'Task #{self.task_number}: {self.target_info} | [inactive]')
            return
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
    
    def last_day_of_february_is_valid(self, date):
        day, month, year = date.split('.')
        if day == '29' and month == '02':
            if int(year)%4 == 0 and int(year)%100 != 0 or int(year)%400 == 0:
                return True # February 29 is valid
            return False # February 29 is not valid
        return True # not concern February 29

    def change_parameters(self):
        date = input('Please set the date (dd.mm.yyyy): ').strip()
        # without date
        if len(date) == 0:
            assigned_day = input('Please assign day of the week (mon/tue/wed/thu/fri/sat/sun): ').strip().lower()
            # no assigned day
            if len(assigned_day) == 0:
                self.date=None
                self.assigned_day=None
                self.periodic = False
                self.time = None
                self.active = True
                print(f'{Fore.GREEN}The task has been modified properly.')
                return True
            # assigned day of the week
            if not re.fullmatch('mon|tue|wed|thu|fri|sat|sun', assigned_day):
                print(f'{Fore.RED}Wrong input.')
                return False
            periodic = input('Is it periodic? (y/n): ').strip().lower()
            # periodic
            if periodic == 'y':
                time = input('Please set the time (hh:mm): ').strip()
                # without time
                if len(time) == 0:
                    self.date=None
                    self.assigned_day=assigned_day
                    self.periodic = True
                    self.time = None
                    active = input('Is it active? (y/n): ').strip().lower()
                    # check if it is active
                    if active == 'y':
                        self.active = True
                    elif active == 'n':
                        self.active = False
                    else:
                        print(f'{Fore.RED}Wrong input.')
                        return False
                    print(f'{Fore.GREEN}The task has been modified properly.')
                    return True
                # set the time
                if not re.fullmatch('1?[0-9]:[0-5][0-9]|2[0-3]:[0-5][0-9]', time):
                    print(f'{Fore.RED}Wrong input.')
                    return False
                self.date=None
                self.assigned_day=assigned_day
                self.periodic = True
                self.time = time
                self.active = True
                print(f'{Fore.GREEN}The task has been modified properly.')
                return True
            # no periodic
            elif periodic == 'n':
                time = input('Please set the time (hh:mm): ').strip()
                # without time
                if len(time) == 0:
                    self.date=None
                    self.assigned_day=assigned_day
                    self.periodic = False
                    self.time = None
                    self.active = True
                    print(f'{Fore.GREEN}The task has been modified properly.')
                    return True
                # set the time
                if not re.fullmatch('1?[0-9]:[0-5][0-9]|2[0-3]:[0-5][0-9]', time):
                    print(f'{Fore.RED}Wrong input.')
                    return False
                self.date=None
                self.assigned_day=assigned_day
                self.periodic = False
                self.time = time
                self.active = True
                print(f'{Fore.GREEN}The task has been modified properly.')
                return True
            else:
                print(f'{Fore.RED}Wrong input.')
                return False
        else:
            # set the date
            if not re.fullmatch(r'''[0][1-9]\.[0][13578]\.2[01][0-9][0-9]| # 01-09.Jan,Mar,May,Jul,Aug.2000-2199
                                [12][0-9]\.[0][13578]\.2[01][0-9][0-9]| # 10-29.Jan,Mar,May,Jul,Aug.2000-2199
                                3[01]\.[0][13578]\.2[01][0-9][0-9]| # 30-31.Jan,Mar,May,Jul,Aug.2000-2199
                                [0][1-9]\.1[02]\.2[01][0-9][0-9]| # 01-09.Oct,Dec.2000-2199
                                [12][0-9]\.1[02]\.2[01][0-9][0-9]| # 10-29.Oct,Dec.2000-2199
                                3[01]\.1[02]\.2[01][0-9][0-9]| # 30-31.Oct,Dec.2000-2199
                                [0][1-9]\.[0][469]\.2[01][0-9][0-9]| # 01-09.Apr,Jun,Sep.2000-2199
                                [12][0-9]\.[0][469]\.2[01][0-9][0-9]| # 10-29.Apr,Jun,Sep.2000-2199
                                30\.[0][469]\.2[01][0-9][0-9]| # 30.Apr,Jun,Sep.2000-2199
                                [0][1-9]\.11\.2[01][0-9][0-9]| # 01-09.Nov.2000-2199
                                [12][0-9]\.11\.2[01][0-9][0-9]| # 10-29.Nov.2000-2199
                                30\.11\.2[01][0-9][0-9]| # 30.Nov.2000-2199
                                [0][1-9]\.02\.2[01][0-9][0-9]| # 01-09.Feb.2000-2199
                                [12][0-9]\.02\.2[01][0-9][0-9]''', date, re.X): # 10-29.Feb.2000-2199
                # re.X flag allows to correctly save the pattern str in a multiline mode ('''str''') and a raw str mode allows to comment between the lines
                print(f'{Fore.RED}Wrong input.')
                return False
            if not self.last_day_of_february_is_valid(date):
                print(f'{Fore.RED}Wrong input. February 29 does not exist in that year.')
                return False
            time = input('Please set the time (hh:mm): ').strip()
            # without time
            if len(time) == 0:
                # deadline or event type
                task_type = input('Please define the task typ (deadline/event): ').strip().lower()
                if task_type == 'deadline' or task_type == 'event':
                    self.date=date
                    self.assigned_day=None
                    self.periodic = False
                    self.time = None
                    self.active = True
                    self.task_type = task_type
                    print(f'{Fore.GREEN}The task has been modified properly.')
                    return True                   
                else:
                    print(f'{Fore.RED}Wrong input.')
                    return False
            # set the time
            if not re.fullmatch('1?[0-9]:[0-5][0-9]|2[0-3]:[0-5][0-9]', time):
                print(f'{Fore.RED}Wrong input.')
                return False
            # deadline or event type
            task_type = input('Please define the task typ (deadline/event): ').strip().lower()
            if task_type == 'deadline' or task_type == 'event':
                    self.date=date
                    self.assigned_day=None
                    self.periodic = False
                    self.time = time
                    self.active = True
                    self.task_type = task_type
                    print(f'{Fore.GREEN}The task has been modified properly.')
                    return True                   
            else:
                print(f'{Fore.RED}Wrong input.')
                return False
