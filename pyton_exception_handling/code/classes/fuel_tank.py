class FuelTankError(Exception):
    pass

class FuelTypeError(FuelTankError):
    def __init__(self, fuel_type):
        message = f"Invalid fuel type: {fuel_type}. Only 'Hydrogen' fuel is allowed."
        super().__init__(message)

class FuelLevelError(FuelTankError):
    """_summary_

    Args:
        max_volume (int): The maximum amount that the tank can hold
        volume (int): Volume of the fuel that will be added to the tank
        
    Attributes:
        value(int): Max amount of fuel that can be added to the tank
    """    
    def __init__(self, max_volume: int, volume: int) -> None:
        amount_left_to_fill = max_volume - volume
        message = f"Max amount of fuel to add is {str(amount_left_to_fill)}" 
        self.value = amount_left_to_fill
        super().__init__(message)

class FuelTank:
    def __init__(self, fuel_type: str, max_volume: int) -> None:
        self.fuel_type = fuel_type
        self.volume = 0
        self.max_volume = max_volume 

    def refuel(self, fuel_type, amount):
        """
        Raises:
            FuelTypeException: If fuel_type is not the correct fuel for the rocket
            FuelLevelException: If the amount of fuel to add would overflow the tank
        """        
        if fuel_type != self.fuel_type:
            raise FuelTypeError(fuel_type)

        elif (self.volume + amount) > self.max_volume:
            raise FuelLevelError(self.max_volume, self.volume)

        else:
            self.volume += amount
            print(f"Fuel tank refueled. Fuel level is now {self.volume} liter.")
        