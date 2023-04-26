class IgnitionException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class Engine:
    def __init__(self, motors: int) -> None:
        self.motors = motors
        self.ignition = False

    def check_ignition(self):
        if not self.ignition:
            raise IgnitionException("Engine has no ignition")
        return self.ignition
            