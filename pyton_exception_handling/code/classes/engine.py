import asyncio
import random

class EngineError(Exception):
    pass

class IgnitionError(EngineError):
    def __init__(self, engine) -> None:
        self.engine = engine
        message = f"Engine {engine} failed to ignite"
        super().__init__(message)

    def __str__(self):
        return f"Error in engine {self.engine}"

class Engine:
    def __init__(self, units: int) -> None:
        self.units = units
        self.ignition = False

    def check_ignition(self):
        if not self.ignition:
            raise IgnitionError("Engine has no ignition. Use the ignite() function to ignite the engine.")
        return self.ignition

    def ignite(self):
        self.ignition = True
        print("Engines ignited")
            
    async def apply_throttle(self):
        try:
            async with asyncio.TaskGroup() as tg:
                for x in range(self.motors):
                    tg.create_task(
                        self.fire_engine(x)
                    )
        
        except* IgnitionError as e:
            print(f"Handling IgnitionErrors: {e.exceptions}")
            raise e.exceptions

        except* EngineError as e:
            print(f"Handling EngineErrors: {e.exceptions}")
            raise e.exceptions


    async def fire_engine(self, engine):
        print(f"Attempting to fire engine {engine}")
        await asyncio.sleep(1)
        engine_fires_chance = random.random()
        if engine_fires_chance < 0.3:
            raise EngineError(f"Something went wrong in engine {engine}")
        elif engine_fires_chance >= 0.8:
            print(f"Engine {engine} failed to fire")
            raise IgnitionError(engine)
        print(f"Engine {engine} fired up!")