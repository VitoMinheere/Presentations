import asyncio
import random

class MotorError(Exception):
    pass

class IgnitionError(MotorError):
    def __init__(self, motor) -> None:
        self.motor = motor
        message = f"Motor {motor} failed to ignite"
        super().__init__(message)

    def __str__(self):
        return f"Error in engine {self.motor}"

class Engine:
    def __init__(self, motors: int) -> None:
        self.motors = motors
        self.ignition = False

    def check_ignition(self):
        if not self.ignition:
            raise IgnitionError("Engine has no ignition")
        return self.ignition
            
    async def apply_throttle(self):
        try:
            async with asyncio.TaskGroup() as tg:
                for x in range(self.motors):
                    tg.create_task(
                        self.fire_engine(x)
                    )
        except* IgnitionError as e:
            print(f"Handling IgnitionErrors: {e.exceptions}")
            print(e.exceptions)
        except* MotorError as e:
            print(f"Handling MotorErrors: {e.exceptions}")
            print(e.exceptions)


    async def fire_engine(self, motor):
        print(f"Attempting to fire motor {motor}")
        engine_fires_chance = random.random()
        if engine_fires_chance < 0.3:
            raise MotorError(f"Something went wrong in motor {motor}")
        elif engine_fires_chance >= 0.8:
            print(f"Motor {motor} failed to fire")
            raise IgnitionError(motor)
        print(f"Motor {motor} fired up!")

eg = Engine(motors=4)

async def check_engine():
    result = await eg.apply_throttle()
    return result

asyncio.run(check_engine())