from .general import item, time_str, datetime_str, BikeData
from .connection import Connection


class BikeState(BikeData):
    def __init__(self, connection: Connection, bikeid: int, cached: bool = True) -> None:
        super().__init__
        self._connection = connection
        self._bikeid = bikeid
        self._cached = cached
        self.refresh(self._cached)

    def refresh(self, cached: bool = True):
        if cached:
            params = {"cached": "true"}
        else:
            params = {"cached": "false"}
        self._data = self._connection.get_endpoint("bike/%s/state/" % self._bikeid, params)

    def trip_reset(self) -> bool:
        return self._connection.delete_endpoint("bike/id/%s/trip_data/" % self._bikeid)

    @property
    def trip_distance(self) -> float:
        return item(self._data, "trip_distance")

    @property
    def suiversion(self) -> str:
        return item(self._data, "suiversion")

    @property
    def average_speed_trip(self) -> float:
        return item(self._data, "average_speed_trip")

    @property
    def power_on_cycles(self) -> int:
        return item(self._data, "power_on_cycles")

    @property
    def tntversion(self) -> str:
        return item(self._data, "tntversion")

    @property
    def atmospheric_pressure(self) -> int:
        return item(self._data, "atmospheric_pressure")

    @property
    def battery_SOC(self) -> int:
        return item(self._data, "battery_SOC")

    @property
    def assistance_level(self) -> int:
        return item(self._data, "assistance_level")

    @property
    def bike_speed(self) -> float:
        return item(self._data, "bike_speed")

    @property
    def trip_time(self) -> int:
        return item(self._data, "trip_time")

    @property
    def trip_time_str(self) -> str:
        return time_str(item(self._data, "trip_time"))

    @property
    def battery_health(self) -> int:
        return item(self._data, "battery_health")

    @property
    def theft_flag(self) -> bool:
        return item(self._data, "theft_flag")

    @property
    def motor_temp(self) -> float:
        return item(self._data, "motor_temp")

    @property
    def battery_temp(self) -> float:
        return item(self._data, "battery_temp")

    @property
    def rcvts(self) -> int:
        return item(self._data, "rcvts")

    @property
    def rcvts_str(self) -> str:
        return datetime_str(item(self._data, "rcvts"))

    @property
    def average_energy_consumption(self) -> int:
        return item(self._data, "average_energy_consumption")

    @property
    def total_time(self) -> int:
        return item(self._data, "total_time")

    @property
    def total_time_str(self) -> str:
        return time_str(item(self._data, "total_time"))

    @property
    def total_distance(self) -> float:
        return item(self._data, "total_distance")

    @property
    def light_on(self) -> int:
        return item(self._data, "light_on")

    @property
    def total_energy_consumption(self) -> int:
        return item(self._data, "total_energy_consumption")

    @property
    def locked(self) -> bool:
        return item(self._data, "lock_flag")

    # return false if changing locked state unsuccessful
    def lock(self, lock: bool = True) -> bool:
        if lock == self.locked:
            # nothing to do
            return True
        data = {"lock": lock}
        response = self._connection.post_endpoint("bike/%s/settings/" % self._bikeid, data)
        newlock = item(response, "lock")
        if newlock is None:
            # something went wrong...
            return False
        # update _data
        self._data["lock_flag"] = newlock
        return True

    def unlock(self) -> bool:
        return self.lock(lock = False)

    # successfully tested modes: {on, off, flash}
    # return false if changing light settings unsuccessful
    def light(self, mode: str = 'on') -> bool:
        if self.locked:
            # cannot manipulate lights if bike is locked
            return False
        json = {"mode": mode}
        response = self._connection.post_endpoint("bike/%s/light/" % self._bikeid, json)
        newmode = item(response, "mode")
        if newmode is None:
            # something went wrong...
            return False
        # update _data
        match newmode:
            case 'flash':
                return True
            case 'off':
                self._data["light_on"] = 0
                return True
            case 'on':
                self._data["light_on"] = 1
                return True
        return False

    def flash(self, force: bool = False) -> bool:
        # if force = True unlock bike first
        if force and self.locked:
            self.unlock()
            success = self.light('flash')
            self.lock()
        else:
            success = self.light('flash')
        return success
