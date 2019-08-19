from expert_system.Cmd import ESCmd
from .Color import Color


class Logger:
    def __init__(self, type):
        self.type = type

    def info(self, message, type=None):
        if ESCmd.args.verbose:
            type = type or self.type
            print(f"{Color.BLUE}<{type}>{Color.END} {message}")
