from code import CodeProject
from template import TemplateProject
from database import DataBaseProject

from crawley.utils import CustomDict

project_types = CustomDict(error="[%s] Not valid project type")
project_types.update({  TemplateProject.name : TemplateProject,
                        CodeProject.name : CodeProject,
                        DataBaseProject.name : DataBaseProject, })
