from classes.rocket import Rocket, StartUpAbort, RocketNotReadyError
from classes.engine import IgnitionError

import asyncio
import traceback

rocket_2 = Rocket("Artemis 2")
try:
    rocket_2.startup_sequence()
except StartUpAbort as e:
#     raise e
    tb = traceback.format_exc()
    print("\n", tb)
    rocket_2.engine.ignite()
    rocket_2.startup_sequence()

print("\n")
async def launch_rocket(rocket):
    try:
        await rocket.launch()
    except RocketNotReadyError as e:
        print(e)
    else:
        print(rocket_2)

asyncio.run(launch_rocket(rocket_2))