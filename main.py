
from task import Task
import colorama
from colorama import Fore
colorama.init(autoreset=True)
import pickle
import re
from datetime import datetime
import pygame
from my_calendar import Calendar
from constants import FPS, WIDTH, HEIGHT, UP_ARROW_LEFT_VERTEX, UP_ARROW_MIDDLE_VERTEX, \
      UP_ARROW_RIGHT_VERTEX, DOWN_ARROW_LEFT_VERTEX, DOWN_ARROW_MIDDLE_VERTEX, \
        DOWN_ARROW_RIGHT_VERTEX, MARGIN, GAP, BIG_TILE_SIZE

def main():
    run = True
    print()
    print('Hello, welcome at the To-Do List Manager :)')
    
    """
    loading or creating the list of tasks, each task includes at least a target
    and optionally a deadline or time/date info, a task is an instance of the class Task
    so surely it could be more attributes and options in it
    """
    try:
        with open('db.pickle', 'rb') as file:
            tasks = pickle.load(file)
    except:
        tasks = []
        print('No database file has been detected.')

    while run:
        # datetime stuff
        datetime_obj = datetime.now() # get the datetime data from the system
        automatic_weekday_assigning(datetime_obj, tasks) # assign the task(s) with a date to the specific weekday when the specific week comes (automatic process)
        automatic_task_marking(datetime_obj, tasks) # mark periodic completed task(s) as 'to-do' when the next day (different day) comes (automatic process)
        automatic_date_assigning(datetime_obj, tasks) # it is reverse function to automatic_weekday_assigning function (automatic process)

        print()
        print('1. Show the list of all tasks.')
        print('2. Add a new task to the list.')
        print('3. Mark the task as completed.')
        print('4. Modify the task.')
        print('5. Launch the calendar.')
        print('6. Exit.')
        chosen_option = input('Please choose the command: ').strip()

        # Show the list of all tasks
        if chosen_option == '1':
            if len(tasks) == 0:
                print('The list of tasks is empty.')
                continue
            print()
            temp_filtered_tasks = []
            for t in tasks:
                if t.assigned_day == None:
                    if t.date == None:
                        t.show_info() # show tasks without date and have no assigned day firstly
                    else:
                        temp_filtered_tasks.append(t) # append tasks which have no assigned day but have be set a date
            sorted_temp_filtered_tasks_by_day = sorted(temp_filtered_tasks, key=lambda t: t.get_date()[0], reverse=True)
            sorted_temp_filtered_tasks_by_month = sorted(sorted_temp_filtered_tasks_by_day, key=lambda t: t.get_date()[1], reverse=True)
            sorted_temp_filtered_tasks_by_year = sorted(sorted_temp_filtered_tasks_by_month, key=lambda t: t.get_date()[2], reverse=True)
            # show sorted descending tasks with a date
            for t in sorted_temp_filtered_tasks_by_year:
                t.show_info()
            print()
            print('MONDAY:')
            show_tasks_on_specific_day('mon', tasks)
            print()
            print('TUESDAY:')
            show_tasks_on_specific_day('tue', tasks)
            print()
            print('WEDNESDAY:')
            show_tasks_on_specific_day('wed', tasks)
            print()
            print('THURSDAY:')
            show_tasks_on_specific_day('thu', tasks)
            print()
            print('FRIDAY:')
            show_tasks_on_specific_day('fri', tasks)
            print()
            print('SATURDAY:')
            show_tasks_on_specific_day('sat', tasks)
            print()
            print('SUNDAY:')
            show_tasks_on_specific_day('sun', tasks)

        # Add a new task to the list
        elif chosen_option == '2':
            target_info = input('Please enter the target info: ').strip()
            if len(target_info) == 0:
                print(f'{Fore.RED}No info has been detected. The task has not been added.')
                continue
            valid_task_number = generate_valid_task_number(tasks)
            date = input('Please set the date (dd.mm.yyyy): ').strip()
            # without date
            if len(date) == 0:
                assigned_day = input('Please assign day of the week (mon/tue/wed/thu/fri/sat/sun): ').strip().lower()
                # no assigned day
                if len(assigned_day) == 0:
                    tasks.append(Task(valid_task_number, target_info, date=None, assigned_day=None))
                    print(f'{Fore.GREEN}The task has been added to the list properly.')
                    save_to_database(tasks)
                    continue
                # assigned day of the week
                if not re.fullmatch('mon|tue|wed|thu|fri|sat|sun', assigned_day):
                    print(f'{Fore.RED}Wrong input.')
                    continue
                periodic = input('Is it periodic? (y/n): ').strip().lower()
                # periodic
                if periodic == 'y':
                    time = input('Please set the time (hh:mm): ').strip()
                    # without time
                    if len(time) == 0:
                        tasks.append(Task(valid_task_number, target_info, date=None, assigned_day=assigned_day, periodic=True, time=None))
                        print(f'{Fore.GREEN}The task has been added to the list properly.')
                        save_to_database(tasks)
                        continue
                    # set the time
                    if not re.fullmatch('1?[0-9]:[0-5][0-9]|2[0-3]:[0-5][0-9]', time):
                        print(f'{Fore.RED}Wrong input.')
                        continue
                    tasks.append(Task(valid_task_number, target_info, date=None, assigned_day=assigned_day, periodic=True, time=time))
                    print(f'{Fore.GREEN}The task has been added to the list properly.')
                    save_to_database(tasks)
                # no periodic
                elif periodic == 'n':
                    time = input('Please set the time (hh:mm): ').strip()
                    # without time
                    if len(time) == 0:
                        tasks.append(Task(valid_task_number, target_info, date=None, assigned_day=assigned_day, periodic=False, time=None))
                        print(f'{Fore.GREEN}The task has been added to the list properly.')
                        save_to_database(tasks)
                        continue
                    # set the time
                    if not re.fullmatch('1?[0-9]:[0-5][0-9]|2[0-3]:[0-5][0-9]', time):
                        print(f'{Fore.RED}Wrong input.')
                        continue
                    tasks.append(Task(valid_task_number, target_info, date=None, assigned_day=assigned_day, periodic=False, time=time))
                    print(f'{Fore.GREEN}The task has been added to the list properly.')
                    save_to_database(tasks)
                else:
                    print(f'{Fore.RED}Wrong input.')
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
                    continue
                if not last_day_of_february_is_valid(date):
                    print(f'{Fore.RED}Wrong input. February 29 does not exist in that year.')
                    continue
                time = input('Please set the time (hh:mm): ').strip()
                # without time
                if len(time) == 0:
                    # deadline or event type
                    task_type = input('Please define the task typ (deadline/event): ').strip().lower()
                    if task_type == 'deadline' or task_type == 'event':
                        tasks.append(Task(valid_task_number, target_info, date=date, assigned_day=None, periodic=False, time=None, task_type=task_type))
                        print(f'{Fore.GREEN}The task has been added to the list properly.')
                        save_to_database(tasks)
                    else:
                        print(f'{Fore.RED}Wrong input.')
                    continue
                # set the time
                if not re.fullmatch('1?[0-9]:[0-5][0-9]|2[0-3]:[0-5][0-9]', time):
                    print(f'{Fore.RED}Wrong input.')
                    continue
                # deadline or event type
                task_type = input('Please define the task typ (deadline/event): ').strip().lower()
                if task_type == 'deadline' or task_type == 'event':
                    tasks.append(Task(valid_task_number, target_info, date=date, assigned_day=None, periodic=False, time=time, task_type=task_type))
                    print(f'{Fore.GREEN}The task has been added to the list properly.')
                    save_to_database(tasks)
                else:
                    print(f'{Fore.RED}Wrong input.')

        # Mark the task as completed
        elif chosen_option == '3':
            try:
                chosen_task_number = int(input('Please choose the task by its number: ').strip())
            except ValueError:
                print(f'{Fore.RED}Wrong input.')
                continue
            for t in tasks:
                if t.task_number == chosen_task_number:
                    t.mark_as_completed()
                    print(f'{Fore.GREEN}Chosen task has been marked as completed.')
                    save_to_database(tasks)
                    break
            else:
                print(f'{Fore.RED}Wrong task number.')

        # Modify the task
        elif chosen_option == '4':
            try:
                chosen_task_number = int(input('Please choose the task by its number: ').strip())
            except ValueError:
                print(f'{Fore.RED}Wrong input.')
                continue
            for t in tasks:
                if t.task_number == chosen_task_number:
                    print('What do you want to do with the chosen task?')
                    print('1. Change the target info.')
                    print('2. Change the parameters.')
                    print('3. Undo the command: mark the task as completed.')
                    print('4. Delete the task from the list.')
                    chosen_option = input('Please choose the command: ').strip()
                    # Change the target info
                    if chosen_option == '1':
                        new_target_info = input(f'{t.target_info} --> ').strip()
                        if len(new_target_info) == 0:
                            print(f'{Fore.RED}No info has been detected. Target info has not changed.')
                            break
                        t.change_target_info(new_target_info)
                        print(f'{Fore.GREEN}Target info has changed properly.')
                        save_to_database(tasks)
                    # Change the parameters
                    if chosen_option == '2':
                        is_properly_modified = t.change_parameters()
                        if is_properly_modified:
                            save_to_database(tasks)
                    # Undo the command: mark the task as completed
                    elif chosen_option == '3':
                        t.mark_as_to_do()
                        print(f'{Fore.GREEN}Chosen task has been marked as to-do.')
                        save_to_database(tasks)
                    # Delete the task from the list
                    elif chosen_option == '4':
                        tasks.remove(t)
                        print(f'{Fore.GREEN}Chosen task has been deleted from the list.')
                        save_to_database(tasks)
                    else:
                        print(f'{Fore.RED}Not recognized command. Please try again.')
                    break
            else:
                print(f'{Fore.RED}Wrong task number.')

        # Launch the calendar
        elif chosen_option == '5':
            WIN = pygame.display.set_mode((WIDTH, HEIGHT))
            pygame.display.set_caption('To-Do List Manager - GUI')
            pygame.init()
            calendar_loop(WIN, tasks)

        # Exit the app
        elif chosen_option == '6':
            run = False
        else:
            print(f'{Fore.RED}Not recognized command. Please try again.')

# update the database or create a new one if does not exist yet
def save_to_database(tasks):
    try:
        with open('db.pickle', 'wb') as file:
            pickle.dump(tasks, file)
    except:
        print(f'{Fore.RED}Failed to save the tasks to database.')

# generate a valid (first positive free) task number for a new task in order to safely add it to the list
def generate_valid_task_number(tasks):
    number_of_all_tasks = len(tasks)
    # if there is no tasks, the first task's number should be 1
    if number_of_all_tasks == 0:
        return 1

    temp_task_number_list = []
    for t in tasks:
        temp_task_number_list.append(t.task_number)

    highest_task_number = max(temp_task_number_list)
    # if number of all tasks is equal to the highest task number it means that everything is ordered
    if highest_task_number == number_of_all_tasks:
        return highest_task_number + 1

    # if number of all task is lesser than the highest task number it means there is a hole somewhere between the int numbers
    temp_task_number_list.sort()
    i = 1
    for tn in temp_task_number_list:
        if i < tn:
            return i
        i += 1

def last_day_of_february_is_valid(date):
    day, month, year = date.split('.')
    if day == '29' and month == '02':
        if int(year)%4 == 0 and int(year)%100 != 0 or int(year)%400 == 0:
            return True # February 29 is valid
        return False # February 29 is not valid
    return True # not concern February 29

def show_tasks_on_specific_day(day_str, tasks):
    temp_filtered_tasks = [] # with time
    temp_filtered_tasks_without_time = []
    for t in tasks:
        if t.assigned_day == day_str:
            if t.time == None:
                temp_filtered_tasks_without_time.append(t) # append tasks which have assigned day and without time
            else:
                temp_filtered_tasks.append(t) # append tasks which have assigned day and have be set time
    # sort tasks with time only by time
    sorted_temp_filtered_tasks_by_minutes = sorted(temp_filtered_tasks, key=lambda t: t.get_time()[1])
    sorted_temp_filtered_tasks_by_hours = sorted(sorted_temp_filtered_tasks_by_minutes, key=lambda t: t.get_time()[0])
    # concatenate two lists in specific order (tasks without time and tasks with time)
    sorted_temp_filtered_tasks = temp_filtered_tasks_without_time + sorted_temp_filtered_tasks_by_hours
    # sort all tasks by state (inactive/completed/to-do)
    sorted_temp_filtered_tasks_by_state = sorted(sorted_temp_filtered_tasks, key=lambda t: t.get_state())
    # show sorted ascending tasks without time and with time by state
    for t in sorted_temp_filtered_tasks_by_state:
        t.show_info()

def automatic_weekday_assigning(datetime_obj, tasks):
    current_week_num = datetime_obj.strftime("%W") # Week number of year, Monday as the first day of week, 00-53
    current_year = datetime_obj.strftime("%Y") # yyyy str format
    temp_counter = 0
    for t in tasks:
        if t.date:
            temp_datetime_obj = datetime(t.get_date()[2], t.get_date()[1], t.get_date()[0]) # temporarily create an datetime object based on the task date
            if temp_datetime_obj.strftime("%W") == current_week_num and \
                temp_datetime_obj.strftime("%Y") == current_year:
                assigned_day = temp_datetime_obj.strftime("%a").lower() # short version of weekday, str format
                t.move_to_specific_assigned_day(assigned_day)
                temp_counter += 1
    
    if temp_counter == 1:
        print(f'{Fore.GREEN}One task has been assigned to the specific day successfully.')
    elif temp_counter > 1:
        print(f'{Fore.GREEN}{temp_counter} tasks have been assigned to the specific day successfully.')

    if temp_counter > 0:
        save_to_database(tasks)

def automatic_task_marking(datetime_obj, tasks):
    current_weekday = datetime_obj.strftime("%a").lower() # short version of weekday, str format
    temp_counter = 0
    for t in tasks:
        if t.periodic and t.active and t.state == 'completed' and t.assigned_day != current_weekday:
            t.mark_as_to_do()
            temp_counter += 1

    if temp_counter == 1:
        print(f'{Fore.GREEN}One periodic task has been marked as to-do successfully.')
    elif temp_counter > 1:
        print(f'{Fore.GREEN}{temp_counter} periodic tasks have been marked as to-do successfully.')

    if temp_counter > 0:
        save_to_database(tasks)

def automatic_date_assigning(datetime_obj, tasks):
    current_week_num = datetime_obj.strftime("%W") # Week number of year, Monday as the first day of week, 00-53
    temp_counter = 0
    for t in tasks:
        if t.datetime_obj and t.assigned_day:
            if t.datetime_obj.strftime("%W") != current_week_num:
                t.set_date_from_datetime_obj()
                temp_counter += 1
    
    if temp_counter == 1:
        print(f'{Fore.GREEN}For one task has assigned the date again successfully.')
    elif temp_counter > 1:
        print(f'{Fore.GREEN}For {temp_counter} tasks has assigned the date again successfully.')

    if temp_counter > 0:
        save_to_database(tasks)

# GUI
def calendar_loop(WIN, tasks):
    clock = pygame.time.Clock()
    run = True
    calendar = Calendar(WIN, tasks)
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed(3)[0]:
                    pos_x, pos_y = pygame.mouse.get_pos()
                    #print((pos_x, pos_y))
                    # description on the left
                    if pos_x >= MARGIN + GAP and pos_x <= MARGIN + GAP + calendar.description_dims[0] \
                    and pos_y >= HEIGHT - WIDTH - calendar.description_dims[1] and pos_y <= HEIGHT - WIDTH:
                        if calendar.chosen_year and not calendar.chosen_month and not calendar.chosen_day:
                            calendar.generate_chosen_decade()
                        elif calendar.chosen_year and calendar.chosen_month and not calendar.chosen_day:
                            calendar.generate_chosen_year()
                        elif calendar.chosen_year and calendar.chosen_month and calendar.chosen_day:
                            calendar.generate_chosen_month()
                    # up arrow (previous content)
                    if pos_x >= UP_ARROW_LEFT_VERTEX[0] and pos_x <= UP_ARROW_RIGHT_VERTEX[0] \
                    and pos_y >= UP_ARROW_MIDDLE_VERTEX[1] and pos_y <= UP_ARROW_LEFT_VERTEX[1]:
                        if not calendar.chosen_year and not calendar.chosen_month and not calendar.chosen_day:
                            calendar.change_chosen_decade(next=False)
                        elif calendar.chosen_year and not calendar.chosen_month and not calendar.chosen_day:
                            calendar.change_chosen_year(next=False)
                        elif calendar.chosen_year and calendar.chosen_month and not calendar.chosen_day:
                            calendar.change_chosen_month(next=False)
                        elif calendar.chosen_year and calendar.chosen_month and calendar.chosen_day:
                            calendar.change_chosen_day(next=False)
                    # down arrow (next content)
                    if pos_x >= DOWN_ARROW_LEFT_VERTEX[0] and pos_x <= DOWN_ARROW_RIGHT_VERTEX[0] \
                    and pos_y >= DOWN_ARROW_LEFT_VERTEX[1] and pos_y <= DOWN_ARROW_MIDDLE_VERTEX[1]:
                        if not calendar.chosen_year and not calendar.chosen_month and not calendar.chosen_day:
                            calendar.change_chosen_decade()
                        elif calendar.chosen_year and not calendar.chosen_month and not calendar.chosen_day:
                            calendar.change_chosen_year()
                        elif calendar.chosen_year and calendar.chosen_month and not calendar.chosen_day:
                            calendar.change_chosen_month()
                        elif calendar.chosen_year and calendar.chosen_month and calendar.chosen_day:
                            calendar.change_chosen_day()
                    # big tiles (years and month) and regular tiles (days) - generally the board
                    if pos_x >= MARGIN and pos_x <= WIDTH - MARGIN and pos_y >= HEIGHT - WIDTH + MARGIN \
                    and pos_y <= HEIGHT - MARGIN:
                        if not calendar.chosen_year and not calendar.chosen_month and not calendar.chosen_day:
                            calendar.choose_year(pos_x, pos_y)
                        elif calendar.chosen_year and not calendar.chosen_month and not calendar.chosen_day:
                            calendar.choose_month(pos_x, pos_y)
                        elif calendar.chosen_year and calendar.chosen_month and not calendar.chosen_day:
                            calendar.choose_day(pos_x, pos_y)

        calendar.render()

    pygame.quit()

main()
