from expert_system.Cmd import ESCmd


class Logger:
    def __init__(self, type):
        self.type = type

    def info(self, message, type=None):
        if ESCmd.args.verbose:
            if type:
                print(f"<{type}> {message}")
            else:
                print(f"<{self.type}> {message}")
