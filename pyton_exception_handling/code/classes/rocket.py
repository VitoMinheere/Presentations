from classes.fuel_tank import FuelTank, FuelLevelError, FuelTypeError
from classes.command_centre import CommandCentre, SignalTooLowError, CommunicationError
from classes.engine import Engine, IgnitionError

from contextlib import suppress

class Abort(Exception):
    pass

class StartUpAbort(Abort):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    

class Rocket:
    def __init__(self, name):
        self.name = name
        self.altitude = 0
        self.crew = []
        self.fuel_tank = FuelTank("Hydrogen", 100)
        self.command_centre = CommandCentre()
        self.engine = Engine(motors=4)
        self.startup_completed = False
        
    def launch(self):
        if self.startup_completed and self.fuel_tank.volume > 0:
            print(f"{self.name} launched!")
            self.altitude += 100
            self.fuel_tank.volume -= 1

    def refuel(self, fuel_type, amount):
        try:
            self.fuel_tank.refuel(fuel_type, amount)
        except FuelTypeError as e:
            print("Switching to correct fuel and retrying")
            self.refuel(self.fuel_tank.fuel_type, amount)
        except FuelLevelError as e:
            print("Setting correct fuel amount and retrying")
            self.refuel(fuel_type, e.value)
        else:
            print(f"{self.name} refueled.")

    def test_communication(self):
        try:
            self.command_centre.check_communication()
        except SignalTooLowError:
            print("Signal is not strong enough, starting signal booster")
            self.command_centre.signal += 20
            self.command_centre.check_communication()
        except CommunicationError as e:
            print(e)
            print("Something went wrong while communicating with the command centre")
            raise StartUpAbort from e
        else:
            print("Communication works")

    def check_ignition(self):
        try:
            self.engine.check_ignition()
        except IgnitionError as e:
            raise StartUpAbort("Aborted startup do to the above error") from e

    def receive_transmissions(self):
        transmission_generator = self.command_centre.generate_transmissions()
        while True:
            try:
                transmission = next(transmission_generator)
                with suppress((AttributeError, TypeError)):
                    transmission = transmission.strip()
                    print(f"Received: {transmission}")
            except StopIteration:
                print("End of transmission")
                break

    def status(self):
        print(f"{self.name} is at an altitude of {self.altitude} and has {self.fuel_tank.volume} units of fuel.")

    def startup_sequence(self):
        try:
            self.refuel("Diesel", 110) 
            self.test_communication()
            self.check_ignition()
        except StartUpAbort as abort:
            print("Found something wrong, startup halted!")
            raise abort
        else:
            print("All systems are go!")
        finally:
            print("Completed startup check procedure")
            
