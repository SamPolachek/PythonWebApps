from os import system
from pathlib import Path
from coder.coder import create_new_project, generate_data_type

def generate_course_builder():
    project_path = Path('/Users/SamPolachek/Github/PythonWebApps/Superhero')
    project_name = 'CourseBuilder'
    project_app = 'course'
    project_path = create_new_project(project_path, project_name)
    generate_data_type(project_path, project_app, 'Lesson', "lesson")
    system(f'tree {project_path}')