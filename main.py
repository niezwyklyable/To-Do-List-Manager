
from task import Task
import colorama
from colorama import Fore
colorama.init(autoreset=True)
import pickle

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
        print()
        print('1. Show the list of all tasks.')
        print('2. Add a new task to the list.')
        print('3. Mark the task as completed.')
        print('4. Modify the task.')
        print('5. Exit.')
        chosen_option = input('Please choose the command: ').strip()

        # Show the list of all tasks
        if chosen_option == '1':
            if len(tasks) == 0:
                print('The list of tasks is empty.')
                continue
            for t in tasks:
                t.show_info()

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
                assigned_day = input('Please assign day of the week (mon/tue/wed/thu/fri/sat/sun): ').strip()
                # no assigned day
                if len(assigned_day) == 0:
                    tasks.append(Task(valid_task_number, target_info, date=None, assigned_day=None))
                    print(f'{Fore.GREEN}The task has been added to the list properly.')
                    save_to_database(tasks)
                    continue
                # assigned day of the week
                periodic = input('Is it periodic? (y/n): ').strip()
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
                    tasks.append(Task(valid_task_number, target_info, date=None, assigned_day=assigned_day, periodic=False, time=time))
                    print(f'{Fore.GREEN}The task has been added to the list properly.')
                    save_to_database(tasks)
                else:
                    print(f'{Fore.RED}Wrong input.')
            # set the date
            else:
                time = input('Please set the time (hh:mm): ').strip()
                # without time
                if len(time) == 0:
                    # deadline or event type
                    task_type = input('Please define the task typ (deadline/event): ').strip()
                    if task_type == 'deadline' or task_type == 'event':
                        tasks.append(Task(valid_task_number, target_info, date=date, assigned_day=None, periodic=False, time=None, task_type=task_type))
                        print(f'{Fore.GREEN}The task has been added to the list properly.')
                        save_to_database(tasks)
                    else:
                        print(f'{Fore.RED}Wrong input.')
                    continue
                # set the time
                # deadline or event type
                task_type = input('Please define the task typ (deadline/event): ').strip()
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
                    print('2. Undo the command: mark the task as completed.')
                    print('3. Delete the task from the list.')
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
                    # Undo the command: mark the task as completed
                    elif chosen_option == '2':
                        t.mark_as_to_do()
                        print(f'{Fore.GREEN}Chosen task has been marked as to-do.')
                        save_to_database(tasks)
                    # Delete the task from the list
                    elif chosen_option == '3':
                        tasks.remove(t)
                        print(f'{Fore.GREEN}Chosen task has been deleted from the list.')
                        save_to_database(tasks)
                    else:
                        print(f'{Fore.RED}Not recognized command. Please try again.')
                    break
            else:
                print(f'{Fore.RED}Wrong task number.')

        # Exit the app
        elif chosen_option == '5':
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

main()
