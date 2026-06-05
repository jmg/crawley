"""Base classes for the management commands."""

import os
from argparse import ArgumentParser

from crawley.manager.projects import project_types
from crawley.utils import (
    add_to_path,
    exit_with_error,
    fix_file_extension,
    has_valid_attr,
    import_user_module,
)


class BaseCommand:
    """Base crawley command."""

    name = "BaseCommand"

    def __init__(self, args=None):
        self.args = args if args is not None else []

    def check_validations(self):
        for validation, message in self.validations():
            if not validation:
                exit_with_error(message)

    def validations(self):
        return []

    def execute(self):
        raise NotImplementedError

    def checked_execute(self):
        self.check_validations()
        self.execute()


class ProjectCommand(BaseCommand):
    """A command that requires a ``settings.py`` file to run."""

    def __init__(self, args=None, settings=None, **kwargs):
        self.kwargs = kwargs
        self.settings = settings
        super().__init__(args)

    def checked_execute(self):
        if self.settings is None:
            self._add_options()
            self.settings = self._check_for_settings()
        else:
            add_to_path(self.settings.PROJECT_ROOT, 1)

        self._check_settings_errors()
        self._check_project_type()
        super().checked_execute()

    def _add_options(self):
        self.parser = ArgumentParser()
        self.parser.add_argument(
            "-s", "--settings", help="Indicates the settings.py file"
        )

    def _check_for_settings(self):
        options, _unknown = self.parser.parse_known_args(self.args)

        if options.settings is not None:
            settings_dir, file_name = os.path.split(options.settings)
            add_to_path(settings_dir)
            settings_file = os.path.splitext(file_name)[0]
        else:
            add_to_path(os.getcwd())
            settings_file = "settings"

        settings = import_user_module(settings_file)
        add_to_path(settings.PROJECT_ROOT, 1)
        return settings

    def _check_settings_errors(self):
        if hasattr(self.settings, "DATABASE_ENGINE"):
            if self.settings.DATABASE_ENGINE == "sqlite":
                self.settings.DATABASE_NAME = fix_file_extension(
                    self.settings.DATABASE_NAME, "sqlite"
                )

        if hasattr(self.settings, "JSON_DOCUMENT") and self.settings.JSON_DOCUMENT:
            self.settings.JSON_DOCUMENT = fix_file_extension(
                self.settings.JSON_DOCUMENT, "json"
            )

        if hasattr(self.settings, "XML_DOCUMENT") and self.settings.XML_DOCUMENT:
            self.settings.XML_DOCUMENT = fix_file_extension(
                self.settings.XML_DOCUMENT, "xml"
            )

        if hasattr(self.settings, "CSV_DOCUMENT") and self.settings.CSV_DOCUMENT:
            self.settings.CSV_DOCUMENT = fix_file_extension(
                self.settings.CSV_DOCUMENT, "csv"
            )

    def _check_project_type(self):
        if has_valid_attr(self.settings, "PROJECT_TYPE"):
            project_type = self.settings.PROJECT_TYPE
        else:
            meta_data = import_user_module("__init__")
            project_type = meta_data.project_type

        self.project_type = project_types[project_type]()
