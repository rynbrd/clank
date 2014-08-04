Clank
=====
A library to quickly build monolithic commandline tools.

Standard Example
----------------
This creates a tool with a `hello` command which prints "Hello, world!":

from clank import Command, HelpCommand, Manager, UsageCommand

    class HelloCommand(Command):
        """Say hello."""
        name = 'hello'

        def run(self, args):
            print("Hello, world!")

    if __name__ == '__main__':
        Manager([HelloCommand, HelpCommand, UsageCommand]).run()

Argument Example
----------------
The `ArgumentCommand` class uses `argparse` to parse commandline arguments.
This code reimplments the `HelloCommand` class to accept a name as an option:

    from clank import ArgumentCommand, HelpCommand, Manager, UsageCommand

    class HelloCommand(ArgumentCommand):
        """Say hello."""
        name = 'hello'

        def add_arguments(self):
            self.argparser.add_argument(
                '-n', '--name', dest='name', nargs=1, default='world',
                help="The name to run the app in.")

        def run(self, args):
            self.parse_args(args)
            print("Hello, {}!".format(self.options.name))

    if __name__ == '__main__':
        Manager([HelloCommand, HelpCommand, UsageCommand]).run()

License
-------
Copyright (c) 2014 Ryan Bourgeois. This project and all of its contents is
licensed under the BSD-derived license as found in the included [LICENSE][1]
file.

[1]: https://github.com/BlueDragonX/clank/blob/master/LICENSE "LICENSE"
