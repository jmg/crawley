"""``shell`` command: interactively scrape an url from a Python shell."""

from crawley.manager.commands.command import BaseCommand
from crawley.toolbox import request
from crawley.utils import exit_with_error


class ShellCommand(BaseCommand):
    """Fetch an url and drop into an interactive shell to scrape it.

    The fetched :class:`~crawley.http.response.Response` is exposed as
    ``response`` in the shell namespace.
    """

    name = "shell"

    def validations(self):
        return [(len(self.args) >= 1, "No given url")]

    def execute(self):
        url = self.args[0]
        response = request(url)

        namespace = {"response": response}

        try:
            from IPython import embed

            embed(user_ns=namespace)
        except ImportError:
            import code

            try:
                code.interact(local=namespace)
            except SystemExit:
                pass
            except Exception as ex:  # noqa: BLE001
                exit_with_error("Couldn't start the shell: %s" % ex)
