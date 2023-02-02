from .general import item, BikeData


class BikeMaintenance(BikeData):
    def __init__(self, data: dict) -> None:
        self._data = data

    @property
    def display_event(self) -> bool:
        return item(self._data, "display_maintenance_event")

    @property
    def next_km(self) -> int:
        return item(self._data, "next_maintenance_km")

    @property
    def next_date(self) -> str:
        return item(self._data, "next_maintenance_date")

    @property
    def next_interval(self) -> int:
        return item(self._data, "next_maintenance_interval")

    @property
    def customer_enabled(self) -> bool:
        return item(self._data, "customer_enabled_maintenance")

    @property
    def last_reset_km(self) -> int:
        return item(self._data, "last_maintenance_reset_km")

    @property
    def last_reset_date(self) -> str:
        return item(self._data, "last_maintenance_reset_date")
