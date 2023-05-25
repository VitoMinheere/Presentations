class Launchpad:
    def __init__(self) -> None:
        self.claimed = False

    def clear(self):
        print("Clearing launchpad for launch")
        self.claimed = True

    def release(self):
        if self.claimed:
            print("Releasing launchpad after launch sequence")