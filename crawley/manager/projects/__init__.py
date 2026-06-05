"""Project types registry."""

from crawley.manager.projects.code import CodeProject
from crawley.manager.projects.database import DataBaseProject
from crawley.manager.projects.template import TemplateProject
from crawley.utils.collections import CustomDict

project_types = CustomDict(error="[%s] is not a valid project type")
project_types.update(
    {
        CodeProject.name: CodeProject,
        TemplateProject.name: TemplateProject,
        DataBaseProject.name: DataBaseProject,
    }
)

__all__ = ["project_types", "CodeProject", "TemplateProject", "DataBaseProject"]
