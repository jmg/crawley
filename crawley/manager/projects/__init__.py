from code import CodeProject
from template import TemplateProject

from crawley.manager.utils import CustomDict

project_types = CustomDict(error="[%s] Not valid project type")
project_types.update({ TemplateProject.name : TemplateProject, CodeProject.name : CodeProject })
