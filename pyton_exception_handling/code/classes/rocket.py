from classes.fuel_tank import FuelTank, FuelLevelError, FuelTypeError, FuelTankError
from classes.command_centre import CommandCentre, SignalTooLowError, CommunicationError
from classes.engine import Engine, IgnitionError, EngineError

from contextlib import suppress

PRESENTATION_DONE = True

class Abort(Exception):
    pass

class StartUpAbort(Abort):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    

class RocketNotReadyError(Exception):
    pass


class Rocket:
    def __init__(self, name):
        self.name = name
        self.altitude = 0
        self.crew = []
        self.fuel_tank = FuelTank("Hydrogen", 100)
        self.command_centre = CommandCentre()
        self.engine = Engine(units=4)
        self.startup_completed = False

    def __str__(self):
        return f"Rocket {self.name} has {self.engine.units} engines and is at an altitude of {self.altitude} meters"
        
    async def launch(self):
        if not self.startup_completed:
            raise RocketNotReadyError("Please run through the startup sequence before trying to launch")

        if self.fuel_tank.volume == 0:
            raise RocketNotReadyError("The rocket has no fuel. Refuel the rocket before launch")

        try:
            print("Applying throttle to the engine")
            await self.engine.apply_throttle()
        except ExceptionGroup as e:
            if len(e.exceptions) <= 2:
                print("Atleast 2 engines fired, launching anyway")
            else:
                print("Launch failed")

        print(f"{self.name} launched!")
        self.altitude += 100
        self.fuel_tank.volume -= 1

    def refuel(self, fuel_type, amount):
        try:
            self.fuel_tank.refuel(fuel_type, amount)
        except FuelTankError as e:
            raise RocketNotReadyError("Can't launch Rocket today") from e
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
            self.refuel("Hydrogen", 100) 
            self.test_communication()
            self.check_ignition()
        except StartUpAbort as abort:
            print("Found something wrong, startup halted!")
            raise abort
        else:
            print("All systems are go!")
            print("Startup sequence completed. Ready to launch")
            self.startup_completed = True
        finally:
            print("Finished startup check procedure")
            