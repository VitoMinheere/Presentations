import asyncio

async def start_motor(motor_number):
    print(f"Starting motor {motor_number}...")
    await asyncio.sleep(1)
    # Simulating a 50% chance of a MotorError occurring
    if motor_number % 2 == 0:
        raise MotorError(f"Motor {motor_number} failed to start")
    print(f"Motor {motor_number} started successfully")

class MotorError(Exception):
    pass

async def start_all_motors():
    retry_count = 0
    max_retries = 3
    motors = [1, 2, 3, 4]

    while True:
        async with asyncio.create_task_group() as group:
            # Start each motor as a separate task in the task group
            for motor in motors:
                group.create_task(start_motor(motor))

            try:
                # Wait for all the tasks to complete within 5 seconds
                await asyncio.wait_for(group, timeout=5)
                print("All motors started successfully")
                break  # Exit the retry loop once all motors have started

            except asyncio.TimeoutError:
                retry_count += 1
                print(f"Retry attempt {retry_count}/{max_retries}")
                if retry_count >= max_retries:
                    print("Maximum retry attempts exceeded")
                    break  # Exit the retry loop if maximum retries are exceeded
            
            # TODO Use except*
            except asyncio.ExceptionGroup as e:
                # Handle any MotorError exceptions raised by the task group
                for task_exc in e.exceptions:
                    if isinstance(task_exc, MotorError):
                        print(f"Motor error occurred: {task_exc}")

async def main():
    await start_all_motors()

# Run the event loop
if __name__ == '__main__':
    asyncio.run(main())
