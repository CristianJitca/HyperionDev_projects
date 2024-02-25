# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = [] 
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


# Function to display tasks details.
def display_task_details(t):     
    disp_str = f"Task: \t\t {t['title']}\n"
    disp_str += f"Assigned to: \t {t['username']}\n"
    disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
    disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
    disp_str += f"Task Description: \n {t['description']}\n"
    return disp_str
    
# Function to register a new user.
def reg_user(username_password):
    """
    The `reg_user` function allows a user to register a new username and password, checks if the
    username already exists, and stores the new user data in a file.
    """
    
    while True:

        new_username = input("New Username: ")        
        if new_username in username_password.keys():
            print("Username already exist. Please enter a different username.")    
        else:
            break 
            
    while True:
        
        new_password = input("New Password: ") 
        confirm_password = input("Confirm Password: ") 
        
        if new_password == confirm_password:             
            print("New user added")
            username_password[new_username] = new_password

            # Modified the block of code and changed the way we open the file from 'w' to 'a',
            # append mode is more efficient as it avoids reading and writing the entire file.            
            with open("user.txt", "a") as out_file:  
                out_file.write(f"\n{new_username};{new_password}")
            break       
        else:
            print("Passwords do no match")

# Function to add a new task to a task list for a specific user.
def add_task(task_list, username_password): 
    '''Allow a user to add a new task to task.txt file
        Prompt a user for the following:
        - A username of the person whom the task is assigned to,
        - A title of a task,
        - A description of the task and the due date of the task.'''
    while True:
        task_username = input("Name of person assigned to task: ")
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
        else:
            break
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    # Then get the current date.
    curr_date = date.today()
    ''' Add the data to the file task.txt and
        Include 'No' to indicate if the task is complete.'''
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

# Modified the block of code and changed the way we open the file from 'w' to 'a',
# append mode is more efficient as it avoids reading and writing the entire file. 
    task_list.append(new_task)
    with open("tasks.txt", "a") as task_file:
        t = new_task
        str_attrs = [
            t['username'],
            t['title'],
            t['description'],
            t['due_date'].strftime(DATETIME_STRING_FORMAT),
            t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
            "Yes" if t['completed'] else "No"
        ]
        task_file.write("\n" + ";".join(str_attrs))
    

# Function to view all the tasks listed in ‘tasks.txt’.
def view_all(task_list):
    '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling) 
        '''         
    for t in task_list:
        print(display_task_details(t))
                           
# Function to view all the tasks that have been assigned to the current user.
def view_mine(task_list, curr_user):
    '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling)
    '''
    index = 1
    user_tasks = []
    for t in task_list:
        if t['username'] == curr_user:
            user_tasks.append(t)
            print(f"Task number: {index} \n{display_task_details(t)}")
            index += 1
        
    while True:
        try:
            task_index = input("Select a task by entering its number (or enter -1 to return to the main menu): ")
            task_index = int(task_index)

            if task_index == -1:
                break
            
            else:
                task_index = task_index - 1
                selected_task = user_tasks[task_index]
                print(display_task_details(selected_task))

            while True:        
                view_my_task_options = input(
                    """Select one of the following Options below:
et - Edit task
mt - Mark task as complete
""").lower()
                if view_my_task_options in ["et", "mt"]:
                    break
                else:
                    print("Invalid input. Please try again.\n")

            if not selected_task['completed']:
                if view_my_task_options == "et":
                    new_username = input("Enter new username (press Enter to keep current): ")

                    if new_username:                   
                        selected_task['username'] = new_username
                    while True: 
                        try:
                            new_due_date = input("Enter new due date (YYYY-MM-DD) (press Enter to keep current): ")

                            if new_due_date:
                                selected_task['due_date']  = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                            break
                        except ValueError:
                            print("Invalid datetime format. Please use the format specified\n")

                    with open("tasks.txt", "w") as task_file:
                        task_list_to_write = []
                        for t in task_list:
                            str_attrs = [
                                t['username'],
                                t['title'],
                                t['description'],
                                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                                "Yes" if t['completed'] else "No"
                            ]
                            task_list_to_write.append(";".join(str_attrs))
                        task_file.write("\n".join(task_list_to_write))                  
                    print("Task successfully updated.")
                    break
                elif view_my_task_options == "mt":
                    selected_task['completed'] = "Yes"

                    with open("tasks.txt", "w") as task_file:
                            task_list_to_write = []
                            for t in task_list:
                                str_attrs = [
                                    t['username'],
                                    t['title'],
                                    t['description'],
                                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                                    "Yes" if t['completed'] else "No"
                                ]
                                task_list_to_write.append(";".join(str_attrs))
                            task_file.write("\n".join(task_list_to_write))
                            print("Task marked as completed")
                            break
            else: 
                print("Task is already completed. Cannot be edited.") 
                break      
        except (ValueError, IndexError):
            print("Invalid input. Please enter a valid task number.\n")
    
# Function to generate reports
def generate_reports(task_list, username_password):
    """
    The function `generate_reports` generates task and user overviews based on a given task list and
    username-password dictionary. 
    """

    total_tasks = len(task_list)
    completed_tasks = sum(1 for t in task_list if t['completed'])
    uncompleted_tasks = total_tasks - completed_tasks
    overdue_tasks = sum(1 for t in task_list if not t['completed'] and t['due_date'] < datetime.today())

    incomplete_tasks_percentage = (uncompleted_tasks / total_tasks) * 100 if uncompleted_tasks != 0 else 0
    overdue_tasks_percentage = (overdue_tasks / uncompleted_tasks) * 100 if uncompleted_tasks != 0 else 0

    with open("task_overview.txt", "w") as task_overview_file:
        task_overview_file.write(f"Total tasks: {total_tasks}\n")
        task_overview_file.write(f"Completed tasks: {completed_tasks}\n")
        task_overview_file.write(f"Uncompleted tasks: {uncompleted_tasks}\n")
        task_overview_file.write(f"Overdue tasks: {overdue_tasks}\n")
        task_overview_file.write(f"Incomplete percentage: {incomplete_tasks_percentage:.2f}%\n")
        task_overview_file.write(f"Overdue percentage: {overdue_tasks_percentage:.2f}%\n")
    
    
    total_users = len(username_password)
    tasks_assigned_to_users = [t for t in task_list if t['username'] in username_password]

    with open("user_overview.txt", "w") as user_overview_file:
        user_overview_file.write(f"Total users: {total_users}\n")
        user_overview_file.write(f"Total tasks: {total_tasks}\n")

        for user, username_password in username_password.items():
            user_tasks = [t for t in tasks_assigned_to_users if t['username'] == user]
            total_user_tasks = len(user_tasks)

            if total_user_tasks > 0:
                completed_user_tasks = sum(1 for t in user_tasks if t['completed'])
                incomplete_user_tasks = total_user_tasks - completed_user_tasks
                overdue_user_tasks = sum(1 for t in user_tasks if not t['completed'] and t['due_date'] < datetime.today())

                user_tasks_percentage = (total_user_tasks / total_tasks) * 100
                completed_user_tasks_percentage = (completed_user_tasks / total_user_tasks) * 100 if total_user_tasks != 0 else 0
                incomplete_user_tasks_percentage = (incomplete_user_tasks / total_user_tasks) * 100 if incomplete_user_tasks != 0 else 0
                overdue_user_tasks_percentage = (overdue_user_tasks / incomplete_user_tasks) * 100 if incomplete_user_tasks != 0 else 0

                user_overview_file.write(f"\nUser: {user}\n")
                user_overview_file.write(f"Total tasks assigned: {total_user_tasks}\n")
                user_overview_file.write(f"Percentage of total tasks: {user_tasks_percentage:.2f}%\n")
                user_overview_file.write(f"Percentage of completed tasks: {completed_user_tasks_percentage:.2f}%\n")
                user_overview_file.write(f"Percentage of incomplete tasks: {incomplete_user_tasks_percentage:.2f}%\n")
                user_overview_file.write(f"Percentage of overdue tasks: {overdue_user_tasks_percentage:.2f}%\n")

# Function to display statistics
def display_statistics(task_list, username_password):
    """
    The function `display_statistics` reads and prints the contents of two text files,
    `task_overview.txt` and `user_overview.txt`.
    First check if these text files exist, if they don`t exist generate the text files.
    """
    if not (os.path.exists("task_overview.txt") and os.path.exists("user_overview.txt")):
        generate_reports(task_list, username_password)
        
    with open("task_overview.txt", "r") as file:
        task_info = file.readlines()

        for line in task_info:
            task_overview_info = line.strip()
            print(task_overview_info)
            
    with open("user_overview.txt", "r") as file:
        user_info = file.readlines()
        
        for line in user_info:
            user_overview_info = line.strip()
            print(user_overview_info)

while True:
    # Presenting the menu to the user.
    # If the user is the admin present extra options(gr = Generate reports and ds = Display statistics)
    print()
    if curr_user == "admin":
        menu = input('''\nSelect one of the following Options below:
r  - Registering a user
a  - Adding a task
va - View all tasks
vm - View my task
gr - Generate reports             
ds - Display statistics
e  - Exit
: ''').lower()
    
    else:
        menu = input('''\nSelect one of the following Options below:
r  - Registering a user
a  - Adding a task
va - View all tasks
vm - View my task             
e  - Exit
: ''').lower()


    
    if menu == 'r':
        print()
        reg_user(username_password)
            
    elif menu == 'a':
        print()
        add_task(task_list, username_password)
        for t in task_list:
            print(display_task_details(t))
        
    elif menu == 'va':
        print()   
        view_all(task_list)
            
    elif menu == 'vm':
        print()
        view_mine(task_list, curr_user)

    elif menu == 'gr' and curr_user == 'admin':
        print()
        generate_reports(task_list, username_password)

    elif menu == 'ds' and curr_user == 'admin':
        print()
        display_statistics(task_list, username_password)
        
    elif menu == 'e':
        print()
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice. Please try again.")
        