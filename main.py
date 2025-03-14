
from task import Task
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
        print('2. Add a task to the list.')
        print('3. Exit.')
        choosed_option = input('Please choose the number: ')
        if choosed_option == '1':
            for t in tasks:
                t.show_info()
        elif choosed_option == '2':
            target_info = input('Please enter the target info: ')
            task_counter += 1
            tasks.append(Task(task_counter, target_info))
            print('The task has been added to the list properly.')
        elif choosed_option == '3':
            run = False
        else:
            print('Not recognized command. Please try again.')

main()
