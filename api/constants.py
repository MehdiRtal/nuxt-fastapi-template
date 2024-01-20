from enum import Enum


class Environment(str, Enum):
    DEV = "DEV"
    PROD = "PROD"

    @property
    def is_dev(self):
        return self == self.DEV

    @property
    def is_prod(self) :
        return self == self.PROD
