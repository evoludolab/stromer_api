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
        if self.__user is not None:
            self.__user.refresh

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
        # share shop info if already set through .bike.service
        myshop = self.bike._shop
        if myshop is None:
            # init shop and share with bike
            self.bike.set_shop(self.__user.set_shop())
        else:
            # share shop with user
            self.__user.set_shop(myshop)

        return self.__user

