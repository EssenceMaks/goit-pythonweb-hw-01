from abc import ABC, abstractmethod
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


# Base class Vehicle
class Vehicle(ABC):
    def __init__(self, make: str, model: str, spec: str) -> None:
        self.make = make
        self.model = model
        self.spec = spec

    @abstractmethod
    def start_engine(self) -> None:
        pass


# Classes inherited from Vehicle
class Car(Vehicle):
    def start_engine(self) -> None:
        logger.info(f"{self.make} {self.model} ({self.spec}): Двигун запущено")


class Motorcycle(Vehicle):
    def start_engine(self) -> None:
        logger.info(f"{self.make} {self.model} ({self.spec}): Мотор заведено")


# Abstract class VehicleFactory
class VehicleFactory(ABC):
    @abstractmethod
    def create_car(self, make: str, model: str) -> Car:
        pass

    @abstractmethod
    def create_motorcycle(self, make: str, model: str) -> Motorcycle:
        pass


# Factory classes
class USVehicleFactory(VehicleFactory):
    def create_car(self, make: str, model: str) -> Car:
        return Car(make, model, "US Spec")

    def create_motorcycle(self, make: str, model: str) -> Motorcycle:
        return Motorcycle(make, model, "US Spec")


class EUVehicleFactory(VehicleFactory):
    def create_car(self, make: str, model: str) -> Car:
        return Car(make, model, "EU Spec")

    def create_motorcycle(self, make: str, model: str) -> Motorcycle:
        return Motorcycle(make, model, "EU Spec")


def main() -> None:
    # US specification vehicles
    us_factory = USVehicleFactory()
    us_car = us_factory.create_car("Ford", "Mustang")
    us_motorcycle = us_factory.create_motorcycle("Harley-Davidson", "Sportster")

    # EU specification vehicles
    eu_factory = EUVehicleFactory()
    eu_car = eu_factory.create_car("Renault", "Clio")
    eu_motorcycle = eu_factory.create_motorcycle("BMW", "R1200GS")

    # Start engines of all vehicles
    us_car.start_engine()
    us_motorcycle.start_engine()
    eu_car.start_engine()
    eu_motorcycle.start_engine()


if __name__ == "__main__":
    main()