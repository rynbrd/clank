"""Manager and complementary commands."""
import os
import sys
from .base import Command
from .errors import ArgumentError, CommandError


class Manager(object):
    """Manage and call commands."""

    def __init__(self, commands=None):
        """Initialize a manager with the given commands."""
        self.commands = {}
        for command in commands or []:
            self.register(command)

    def register(self, command):
        """Register a command with the manager."""
        self.commands[command.name] = command

    def get_names(self):
        """Return a list of command names."""
        return self.commands.keys()

    def get_command_usage(self, command, brief=False):
        """
        Return usage text for an initialized command. If brief is True then the command docstring
        will not be included.
        """
        base = os.path.basename(sys.argv[0])
        usage = "{} {} {}".format(base, command.name, command.get_usage().strip())

        if brief:
            return usage

        doc = command.__class__.__doc__.strip()
        return "{}\n{}".format(usage, doc).strip()

    def get_command_help(self, command):
        """Return the help text of an initialized command."""
        usage = self.get_command_usage(command, True)
        help = command.get_help().strip()
        return "usage: {}\n{}".format(usage, help).strip()

    def get_usage(self, name, brief=False):
        """
        Return the usage text of a command. If brief is True then the command docstring will not be
        included.
        """
        command = self.get_command(name)(self)
        return self.get_command_usage(command, brief)

    def get_help(self, name):
        """Return the help text of a command."""
        command = self.get_command(name)(self)
        return self.get_command_help(command)

    def has_command(self, name):
        """Return True if the command exists or False."""
        return self.commands.keys()

    def get_command(self, name):
        """Return the named command class or raise a CommandError if it does not exist."""
        if name not in self.commands:
            raise CommandError("Command not found: {}".format(name))
        return self.commands[name]

    def call(self, args):
        """
        Call a command. Return the result. Raise CommandError on error. The args param will include
        the command name.
        """
        command = self.get_command(args[0])
        return command(self).run(args)

    def run(self):
        """Run the manager."""
        if len(sys.argv) < 2:
            print("not enough arguments")
            self.call(['usage'])
            return 1

        try:
            ret = self.call(sys.argv[1:])
            if isinstance(ret, int):
                return ret
            return 0
        except ArgumentError as e:
            if e.message:
                print(e.message)
            else:
                print("invalid arguments")
            print("usage: {}".format(self.get_usage(sys.argv[1], True)))
            return e.retcode
        except CommandError as e:
            sys.stderr.write("error: {}\n".format(e))
            return e.retcode


class UsageCommand(Command):
    """Print usage text for one or all commands."""
    name = 'usage'

    def get_usage(self):
        return "[COMMAND]"

    def get_help(self):
        return self.__class__.__doc__.strip()

    def run(self, args):
        if len(args) > 2:
            raise ArgumentError("too many arguments")

        if len(args) == 2:
            print(self.manager.get_usage(args[1]))
        else:
            for name in sorted(self.manager.get_names()):
                print(self.manager.get_usage(name, True))


class HelpCommand(Command):
    """Print help text for a command."""

    name = 'help'

    def get_usage(self):
        return "COMMAND"

    def get_help(self):
        return self.__class__.__doc__.strip()

    def run(self, args):
        if len(args) < 2:
            raise ArgumentError("not enough arguments")
        if len(args) > 2:
            raise ArgumentError("too many arguments")
        print(self.manager.get_help(args[1]))
