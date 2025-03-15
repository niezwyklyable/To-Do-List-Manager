
from task import Task
import colorama
from colorama import Fore
colorama.init(autoreset=True)
tasks = [] # list of tasks, each task includes at least a target
# and optionally a deadline or time/date info, a task is an instance of the class Task
# so surely it could be more attributes and options in it

def main():
    run = True
    task_counter = 0 # constantly increments to provide the tasks being unique
    print()
    print('Hello, welcome at the To-Do List Manager :)')
    
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
                print(f'{Fore.RED}No info has detected. The task has not been added.')
                continue
            task_counter += 1
            tasks.append(Task(task_counter, target_info))
            print(f'{Fore.GREEN}The task has been added to the list properly.')

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
                            print(f'{Fore.RED}No info has detected. Target info has not changed.')
                            break
                        t.change_target_info(new_target_info)
                        print(f'{Fore.GREEN}Target info has changed properly.')
                    # Undo the command: mark the task as completed
                    elif chosen_option == '2':
                        t.mark_as_to_do()
                        print(f'{Fore.GREEN}Chosen task has been marked as to-do.')
                    # Delete the task from the list
                    elif chosen_option == '3':
                        tasks.remove(t)
                        print(f'{Fore.GREEN}Chosen task has been deleted from the list.')
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

main()
