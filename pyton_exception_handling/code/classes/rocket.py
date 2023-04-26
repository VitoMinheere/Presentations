from classes.fuel_tank import FuelTank, FuelLevelException, FuelTypeException
from classes.command_centre import CommandCentre, SignalTooLowException, CommunicationException
from classes.engine import Engine, IgnitionException

class Abort(Exception):
    pass

class StartUpAbort(Abort):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    

class Rocket:
    def __init__(self, name):
        self.name = name
        self.altitude = 0
        self.allowed_fuel = "Hydrogen"
        self.fuel_tank = FuelTank("Hydrogen", 100)
        self.command_centre = CommandCentre()
        self.engine = Engine(1)
        
    def launch(self):
        if self.fuel > 0:
            print(f"{self.name} launched!")
            self.altitude += 100
            self.fuel -= 1
        else:
            print(f"{self.name} has no fuel left.")

    def refuel(self, fuel_type, amount):
        try:
            self.fuel_tank.refuel(fuel_type, amount)
        except FuelTypeException as e:
            print(e)
            print("Grabbing correct fuel and retrying")
            self.refuel("Hydrogen", amount)
        except FuelLevelException as e:
            print(e)
            print("Setting correct fuel amount and retrying")
            self.refuel(fuel_type, e.value)
        else:
            print(f"{self.name} refueled.")

    def test_communication(self):
        try:
            self.command_centre.check_communication()
        except SignalTooLowException:
            print("Signal is not strong enough, starting signal booster")
            self.command_centre.signal += 20
            self.command_centre.check_communication()
        except CommunicationException as e:
            print(e)
            print("Something went wrong while communicating with the command centre")
            raise StartUpAbort from e
        else:
            print("Communication works")

    def check_ignition(self):
        try:
            self.engine.check_ignition()
        except IgnitionException as e:
            # TODO Upgrade to Python 3.11
            # e.add_note("Did you try flicking the switch?")
            raise StartUpAbort from e

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
            