class CommunicationError(Exception):
    pass

class SignalTooLowError(CommunicationError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        
class SignalLostError(CommunicationError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class CommandCentre:
    def __init__(self) -> None:
        self.signal = 100

    def check_communication(self):
        if self.signal < 20 and self.signal > 0:
            raise SignalTooLowError()
        elif self.signal == 0:
            raise SignalLostError("Lost communication with command centre")
        else:
            return True

    def generate_transmissions(self):
        messages = [
            "Message 1",
            {"number": 5},
            "Message 2",
            5,
            "Message 3"
        ]
        for message in messages:
            yield message
            