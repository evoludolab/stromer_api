from .connection import Connection
from .bike import Bike
from .bikestatistics import BikeStatistics
from .bikeuser import BikeUser

class StromerBike:

    def __init__(self, username: str, password: str, client_id: str) -> None:
        self.__statistics = None
        self.__user = None

        self._connection = Connection(username, password, client_id)
        # does 'bike' return an array if user has multiple stromers registered in their name?
        self.__bike = Bike(self._connection)

    def refresh(self):
        if self.__statistics is not None:
            self.__statistics.refresh
            self.__statistics = None
        if self.__user is not None:
            self.__user.refresh
            self.__user = None

    @property
    def bike(self) -> Bike:
        return self.__bike

    @property
    def statistics(self) -> BikeStatistics:
        if self.__statistics is None:
            self.__statistics = BikeStatistics(self._connection)
        return self.__statistics

    @property
    def user(self) -> BikeUser:
        if self.__user is None:
            self.__user = BikeUser(self._connection)

        return self.__user

