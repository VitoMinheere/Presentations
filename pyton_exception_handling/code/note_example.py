class Crew:
    def __init__(self, name, ready=False):
        self.name = name
        self.ready = ready
        
    def __str__(self):
        return f"{self.name} is {'ready' if self.ready else 'not ready'}"
        
crew = [Crew("Alice", True), Crew("Bob")]
backup_crew = [Crew("Carol", True)]

for member in crew:
    print(member)

for member in backup_crew:
    print(member)

class RocketNotReadyError(Exception):
    pass


def personnel_check():
    try:
        print("\tThe captain's name is", crew[0].name)
        print("\tThe pilot's name is", crew[1].name)
        print("\tThe mechanic's name is", crew[2].name)
    except IndexError as e:
        r = RocketNotReadyError('Crew is incomplete')
        r.add_note("Did you check the backup crew?")
        raise r from e

personnel_check()
