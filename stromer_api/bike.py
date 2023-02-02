from .general import item, BikeData
from .connection import Connection
from .bikemaintenance import BikeMaintenance
from .bikeposition import BikePosition
from .bikestate import BikeState
from .bikesensors import BikeSensors
from .bikemotortuning import BikeMotorTuning
from .bikesettings import BikeSettings

# note: does connection.get_endpoint("bike") return an array if multiple 
# stromers are registered under the same name?
class Bike(BikeData):
    def __init__(self, connection: Connection) -> None:
        super().__init__(None)
        self._connection = connection
        self.__maintenance = None
        self.__position = None
        self.__state = None
        self.__sensors = None
        self.__motor_tuning = None
        self.__settings = None
        self.refresh()

    def refresh(self):
        self._data = self._connection.get_endpoint("bike")

    @property
    def nickname(self) -> str:
        return item(self._data, "nickname")

    @property
    def bikeid(self) -> int:
        return item(self._data, "bikeid")

    @property
    def bikemodel(self) -> str:
        return item(self._data, "bikemodel")

    @property
    def biketype(self) -> str:
        return item(self._data, "biketype")

    @property
    def color(self) -> str:
        return item(self._data, "color")

    @property
    def size(self) -> str:
        return item(self._data, "size")

    @property
    def hardware(self) -> str:
        return item(self._data, "hardware")

    @property
    def connectivity(self) -> str:
        return item(self._data, "connectivity")

    @property
    def has_crash_detection(self) -> bool:
        return item(self._data, "has_crash_detection")

    @property
    def maintenance(self) -> BikeMaintenance:
        if self.__maintenance is None:
            self.__maintenance = BikeMaintenance(item(self._data, "maintenance_feature"))
        return self.__maintenance

    @property
    def position(self, cached: bool = True) -> BikePosition:
        if self.__position is None:
            self.__position = BikePosition(self._connection, self.bikeid, cached)
        return self.__position

    @property
    def state(self, cached: bool = True) -> BikeState:
        if self.__state is None:
            self.__state = BikeState(self._connection, self.bikeid, cached)
        return self.__state

    @property
    def sensors(self) -> BikeSensors:
        if self.__sensors is None:
            self.__sensors = BikeSensors(self._connection, self.bikeid)
        return self.__sensors

    @property
    def motor_tuning(self) -> BikeMotorTuning:
        if self.__motor_tuning is None:
            self.__motor_tuning = BikeMotorTuning(self._connection, self.bikeid)
        return self.__motor_tuning

    @property
    def settings(self) -> BikeSettings:
        if self.__settings is None:
            self.__settings = BikeSettings(self._connection, self.bikeid)
        return self.__settings
