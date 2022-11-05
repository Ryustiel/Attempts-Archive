"""
Main webpages management for django

Allows to manage individual projects, create pages, manage URLs, routing... and other stuff
"""
import os

if __name__ == '__main__':
    meep_path = os.getcwd() # get variable from meep otherwise

def create_django_project(project_name):
    """
    action
    creates a new project
    """

    projects_path = os.path.join(meep_path, 'MODULES', 'django', 'projects')
    folder_path = os.path.join(projects_path, project_name)

    if os.path.exists(folder_path):
        print('Project %s already exists' % project_name)
    else:
        os.chdir(projects_path)
        os.system("django-admin startproject " + project_name)

def manage(project_name, command, *args): # IMPLEMENTER UN CHECKER D'ATTRIBUTS COMMANDE
    """
    action
    runs the specified command on manage.py (from the specified project)
    """
    projects_path = os.path.join(meep_path, 'MODULES', 'django', 'projects')
    folder_path = os.path.join(projects_path, project_name)
    
    if os.path.exists(folder_path):
        os.chdir(folder_path)
        command_line_str = "py -3 manage.py " + command
        for arg in args:
            command_line_str += " " + arg
        os.system(command_line_str)
    else:
        print('Project %s does not exist' % project_name)

def start_app(project_name, app_name):
    """
    action
    starts an app using manage.py
    """
    manage(project_name, "startapp", app_name)

def migrate_shortcut(project_name):
    manage(project_name, 'makemigrations')
    manage(project_name, 'migrate')

def runserver(project_name):
    """
    action
    runs the server
    """
    manage(project_name, 'runserver')


runserver('tgvmax')