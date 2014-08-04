"""Command base classes."""
import os
import re
import sys
from .errors import CommandError
from argparse import ArgumentParser, _StoreAction


class Command(object):
    """Base class for a cloud command."""

    def __init__(self, manager):
        """Iniitialize the command."""
        self.manager = manager

    def get_usage(self):
        """Return usage text for the command. Should not include the command name."""
        return ""

    def get_help(self):
        """
        Return help text for the command. The help command will first print the usage followed by
        this help text.
        """
        return self.__class__.__doc__.strip()

    def run(self, args):
        """Run the command with the provided args. Should raise a CommandError on error."""
        raise CommandError("Command not implemented.")


class ArgumentCommand(Command):
    """A base command with argparse support rolled in."""

    def __init__(self, manager):
        """Initialize the command with an argument parser."""
        super(ArgumentCommand, self).__init__(manager)
        prog = "{} {}".format(os.path.basename(sys.argv[0]), self.name)
        self.argparser = ArgumentParser(add_help=False, prog=prog)
        self.options = None
        self.args = None
        self.add_arguments()

    def add_arguments(self):
        """Build the argument parser here. It's in self.argparser."""

    def parse_args(self, args, known=False):
        """
        Parse arguments into self.options. Flatten out any action=store values with nargs=1 or
        None. If known is True then only parse known args and place the remaining args into
        self.args.
        """
        def get_valid_action(dest):
            for action in self.argparser._actions:
                if isinstance(action, _StoreAction) and action.dest == dest:
                    if action.nargs is None or action.nargs == 1:
                        return action
                    break
            return None

        if known:
            self.options, self.args = self.argparser.parse_known_args(args[1:])
        else:
            self.options = self.argparser.parse_args(args[1:])

        for name, value in self.options.__dict__.iteritems():
            if hasattr(value, '__iter__'):
                action = get_valid_action(name)
                if action:
                    setattr(self.options, name, value[0])

    def get_usage(self):
        """Print usage text generated from argparse."""
        usage = self.argparser.format_usage().strip()
        return re.sub(r'^usage:\s[^\s]+\s[^\s]+\s', '', usage)

    def get_help(self):
        """Print help text generated from argparse."""
        text = self.argparser.format_help()
        regex = re.compile(r'^optional arguments')
        while text and not regex.match(text):
            start = text.find('\n') + 1
            text = text[start:]
        return text

    def run(self, args):
        """Parse the commandline arguments."""
        self.parse_args(args)
