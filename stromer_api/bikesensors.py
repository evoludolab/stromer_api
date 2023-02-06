from .general import item, BikeData
from .connection import Connection

# note: caching for "bike/<bikeid>/settings" request does not work 

class BikeSensors(BikeData):
    def __init__(self, connection: Connection, bikeid: int, ) -> None:
        super().__init__
        self._connection = connection
        self._bikeid = bikeid
        self.refresh()

    def refresh(self):
        params = {"fields": "recup_level_user_offset,user_torque_sensitivity"}
        self._data = self._connection.get_endpoint("bike/%s/settings/" % self._bikeid, params)

    @property
    def user_torque_sensitivity(self) -> int:
        return item(self._data, "user_torque_sensitivity")

    @property
    def recup_level_user_offset(self) -> int:
        return item(self._data, "recup_level_user_offset")

    def set(self, torque: int | None = None, recup: int | None = None):
        if torque is None:
            torque = self.user_torque_sensitivity
        if recup is None:
            recup = self.recup_level_user_offset
        # range of recup levels: [6-14]
        recup = max(min(recup, 14), 6)
        # range of torque sensitivity: [0-50]
        torque = max(min(torque, 50), 0)
        data = {"user_torque_sensitivity": torque, "recup_level_user_offset": recup}
        # note: both settings must be set at the same time otherwise the POST request
        #   is rejected with a syntax error
        return self._connection.post_endpoint("bike/%s/settings/" % self._bikeid, data)
