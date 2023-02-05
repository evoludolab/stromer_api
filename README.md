Stromer API

This Python package contains the interfaces for interacting with the Stromer web API that is normally used by the Stromer mobile app. Using this API you can retrieve data of your bike.

Installation:

    pip install stromer_api

Usage:

    from stromer_api import StromerBike
    mybike = StromerBike(<your username>, <your password>, <stromer client id>)

    print(mybike.state.trip_distance)
    print(mybike.position.latitude)

The client_id you should intercept using a proxy (eg. mitm proxy) or maybe it can be obtained from decompiling the android apk of the Stromer OMNI app. Many discussions can be found on the internet how to get hold of it.

Properties and methods of `StromerBike`:
* `.bike` Bike object with the following properties:
    * `.nickname` string
    * `.bikeid` int
    * `.bikemodel` string
    * `.biketype` string
    * `.color` string
    * `.size` string
    * `.hardware` string
    * `.connectivity` string
    * `.has_crash_detection` bool

    as well as objects:
    * `.state`
    * `.position`
    * `.settings`
    * `.sensors`
    * `.motor_tuning`
    * `.maintenance`

* `bike.state` BikeState object with the following properties
    * `.trip_distance` float
    * `.suiversion` string
    * `.average_speed_trip` float
    * `.average_speed_total` float
    * `.power_on_cycles` int
    * `.tntversion` string
    * `.atmospheric_pressure` int/float (?)
    * `.battery_SOC` int
    * `.assistance_level` int
    * `.bike_speed` float
    * `.trip_time` float (?)
    * `.battery_health` int
    * `.theft_flag` bool
    * `.motor_temp` float
    * `.battery_temp` float
    * `.rcvts` int: received time stamp
    * `.rcvts_str` string: formatted received time stamp
    * `.average_energy_consumption` int/float (?)
    * `.total_time` int: total riding time
    * `.total_time_str` string: formatted total riding time
    * `.total_distance` float
    * `.light_on` int
    * `.total_energy_consumption` int/float (?)
    * `.locked` bool

    and methods
    * `.lock(lock = True)` locks and unlocks the bike
    * `.unlock()` unlocks the bike (convenience method, same as `.lock(lock = False)`)
    * `.light(mode = `on`)` turns light on, off, or flash (requires that bike is unlocked)

* `.bike.position` BikePosition object with the following properties
    * `.latitude` float
    * `.longitude` float
    * `.altitude` int/float (?)
    * `.speed` float
    * `.timets` int
    * `.timets_str` string
    * `.rcvts` int: received time stamp
    * `.rcvts_str` string: formatted received time stamp

* `.bike.settings` BikeSettings object with the following properties
    * `.auto_lock_mode` bool
    * `.auto_power_off_time` int
    * `.clock_format` string
    * `.date_format` string
    * `.distance_unit` string
    * `.language` string
    * `.speed_unit` string

* `.bike.sensors` BikePosition object with the following properties
    * `.user_torque_sensitivity` int [0-50]
    * `.recup_level_user_offset` int [6-14]

    and methods
    * `.set(torque = None, recup = None)`

* `.bike.motor_tuning` BikeMotorTuning object with the following properties
    * `.motor_tuning.tuning_speed` int [0-100]
    * `.motor_tuning.tuning_torque` int [0-100]
    * `.motor_tuning.tuning_agility` int [0-100]

    and methods
    * `.set(speed = None, torque = None, agility = None)`

* `.bike.maintenance` BikeMaintenance object with the following properties
    * `.display_maintenance_event` bool
    * `.next_maintenance_km` int
    * `.next_maintenance_date` string
    * `.next_maintenance_interval` int
    * `.customer_enabled_maintenance` bool
    * `.last_maintenance_reset_km` int
    * `.last_maintenance_reset_date` string

* `.statistics` BikeStatistics object with the following properties
    * `total_km` float
    * `average_km` float
    * `total_sec` int
    * `average_sec` float
    * `total_wh` int
    * `average_wh` float
    * `kmh` float
    * `average_kmh` float
    * `active_days` int
    * `average_days` float

    and methods
    * `.day_stats(self, year: int, month: int, day: int, num_days: int = 1)`
    * `.week_stats(self, year: int, week: int, num_weeks: int = 1)`
    * `.month_stats(self, year: int, month: int, num_months: int = 1)`
    * `.year_stats(self, year: int, num_years: int = 1)`

    as well as objects:
    * `.day_stats`
    * `.week_stats`
    * `.month_stats`
    * `.year_stats`

* `.statistics.day_stats` DayStats object with properties
    * `.start_date` string
    * `.end_date` string
    * `.total_days` int
    * `.km_avg_30_days` float
    * `.day_record` float
    * `.info` dict with daily info TODO
    * `[day]` CHECK
 
    and methods
    * `.csv_dump()` CHECK

* `.statistics.week_stats` WeekStats object with properties
    * `.start_date` string
    * `.end_date` string
    * `.total_weeks` int
    * `.km_avg_12_weeks` float
    * `.week_record` float
    * `.info` dict with weekly info TODO
    * `[week]` CHECK
 
    and methods
    * `.csv_dump()` CHECK

* `.statistics.month_stats` MonthStats object with properties
    * `.start_date` string
    * `.end_date` string
    * `.total_months` int
    * `.km_avg_12_months` float
    * `.month_record` float
    * `.info` dict with monthly info TODO
    * `[month]` CHECK
 
    and methods
    * `.csv_dump()` CHECK

* `.statistics.year_stats` YearStats object with properties
    * `.start_date` string
    * `.end_date` string
    * `.total_years` int
    * `.km_avg_12_years` float
    * `.year_record` float
    * `.info` dict with annual info TODO
    * `.km_avg_years_since_beginning` CHECK
    * `[year]` CHECK

    and methods
    * `.csv_dump()` CHECK

* `.user` BikeUser object with the following properties
    * `.first_name` string
    * `.last_name` string
    * `.email` string
    * `.phone` string
    * `.mobile` string
    * `.street_name` string
    * `.house_number` string
    * `.postal_code` string
    * `.city` string
    * `.country` string
    * `.size` float
    * `.weight` float
    * `.gender` string
    * `.may_receive_mails` bool
    * `.accepted_gdpr_version` string
    * `.birthday` string

    as well as objects:
    * `.shop`

* `.user.shop` BikeShop object with the following properties
    * `latitude` float
    * `longitude` float
    * `name` string
    * `debitor` string
    * `phone` string
    * `street` string
    * `postal_code` string
    * `city` string
    * `country_name` string
    * `country_code` string

This API makes use of the following "unofficial" endpoints:
* `/bike/`
* `/bike/<bike_id>/state/`
* `/bike/<bike_id>/position/`
* `/bike/<bike_id>/settings/`
* `/bike/<bike_id>/service_info/`
* `/bike/<bike_id>/light/`
* `/bike/statistics/`
* `/bike/statistics/all/`
* `/bike/statistics/extra_data/`
* `/user/`

If you are aware of new or other endpoints that work please leave a message.

Any suggestions for additions are of course also very welcome!
