"""``startproject`` command: scaffold a new crawley project."""

from argparse import ArgumentParser

from crawley.manager.commands.command import BaseCommand
from crawley.manager.projects import CodeProject, project_types


class StartProjectCommand(BaseCommand):
    """Generate a new crawley project from the bundled templates."""

    name = "startproject"

    def __init__(self, args=None, project_type=None, project_name=None, base_dir=None):
        if args is None:
            args = []

        self.project_type = project_type
        self.base_dir = base_dir

        if project_type is not None:
            args = list(args) + ["--type", project_type]
        if project_name is not None:
            args = list(args) + [project_name]

        super().__init__(args)

    def validations(self):
        return [(len(self.args) >= 1, "No given project name")]

    def execute(self):
        parser = ArgumentParser()
        parser.add_argument(
            "-t", "--type", default=CodeProject.name,
            help="Project type: 'code', 'template' or 'database'",
        )
        parser.add_argument("project_name")

        options = parser.parse_args(self.args)

        self.project_type = options.type
        self.project_name = options.project_name

        project = project_types[self.project_type]()
        project.set_up(self.project_name, base_dir=self.base_dir)
