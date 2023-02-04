from .general import item, time_str, BikeData
from .connection import Connection
from .yearstats import YearStats
from .monthstats import MonthStats
from .weekstats import WeekStats
from .daystats import DayStats

import datetime
import calendar

# note: caching for "bike/statistics/all" request does not work 

class BikeStatistics(BikeData):
    def __init__(self, connection: Connection) -> None:
        super().__init__(None)
        self._connection = connection
        self.refresh()

    @property
    def total_km(self) -> float:
        return item(self._data, "total_km")

    @property
    def average_km(self) -> float:
        return item(self._data, "average_km")

    @property
    def total_sec(self) -> int:
        return item(self._data, "total_sec")

    @property
    def total_time_str(self) -> str:
        return time_str(item(self._data, "total_sec"))

    @property
    def average_sec(self) -> float:
        return item(self._data, "average_sec")

    @property
    def average_time_str(self) -> str:
        return time_str(item(self._data, "average_sec"))

    @property
    def total_wh(self) -> int:
        return item(self._data, "total_wh")

    @property
    def average_wh(self) -> float:
        return item(self._data, "average_wh")

    @property
    def kmh(self) -> float:
        return item(self._data, "kmh")

    @property
    def average_kmh(self) -> float:
        return item(self._data, "average_kmh")

    @property
    def active_days(self) -> int:
        return item(self._data, "active_days")

    @property
    def average_days(self) -> float:
        return item(self._data, "average_days")

    def refresh(self):
        self._data = self._connection.get_endpoint("bike/statistics/all/")
        self.__day_stats = None
        self.__week_stats = None
        self.__month_stats = None
        self.__year_stats = None

    # are the statistics for the bike or the user? the endpoint suggests the bike 
    # (except that the bikeid is not required) but the user would seem more natural...
    def day_stats(self, year: int, month: int, day: int, num_days: int = 1) -> DayStats:
        if self.__day_stats is None:
            # start day cannot be in the future
            start_date = datetime.date(year, month, day)
            if start_date > datetime.date.today():
                raise Exception("Start date is in the future")
            start = start_date.strftime("%Y%m%d")

            # set stop_date to today if it is in the future
            stop_date = datetime.date(year, month, day) + datetime.timedelta(days=num_days - 1)
            if stop_date > datetime.date.today():
                stop_date = datetime.date.today()
                stop = datetime.date.today().strftime("%Y%m%d")
            else:
                stop = stop_date.strftime("%Y%m%d")

            avg_rec = self._connection.get_endpoint("bike/statistics/extra_data/",
                                        params={"end": stop, "resolution": "days"})
            daily_info = self._connection.get_endpoint("bike/statistics/",
                                           params={"start": start, "end": stop, "resolution": "days"},
                                           full_list=True)
            day_stats = {"start_date": start,
                         "end_date": stop,
                         "total_days": len(daily_info),
                         "km_avg_30_days": avg_rec["km_avg_30_days"],
                         "day_record": avg_rec["day_record"],
                         "daily_info": {}}

            for day_info in daily_info:
                day_stats["daily_info"][day_info["start"]] = {"total_days": day_info["total_days"],
                                                              "active_days": day_info["active_days"],
                                                              "km": day_info["km"],
                                                              "sec": day_info["sec"],
                                                              "wh": day_info["wh"],
                                                              "first_record": day_info["first_record"]}
            self.__day_stats = DayStats(day_stats)
        return self.__day_stats

    def week_stats(self, year: int, week: int, num_weeks: int = 1) -> WeekStats:
        if self.__week_stats is None:
            # start day cannot be in the future
            start_date = datetime.date.fromisocalendar(year, week, 1)
            if start_date > datetime.date.today():
                raise Exception("Start date is in the future")
            start = start_date.strftime("%Y%m%d")

            # set stop_date to today if it is in the future
            stop_date = datetime.date.fromisocalendar(year, week + num_weeks - 1, 7)
            if stop_date > datetime.date.today():
                stop = datetime.date.today().strftime("%Y%m%d")
            else:
                stop = stop_date.strftime("%Y%m%d")

            avg_rec = self._connection.get_endpoint("bike/statistics/extra_data/",
                                        params={"end": stop, "resolution": "weeks"})
            weekly_info = self._connection.get_endpoint("bike/statistics/",
                                            params={"start": start, "end": stop, "resolution": "weeks"},
                                            full_list=True)

            week_stats = {"start_date": start,
                          "end_date": stop,
                          "total_weeks": len(weekly_info),
                          "km_avg_12_weeks": avg_rec["km_avg_12_weeks"],
                          "week_record": avg_rec["week_record"],
                          "weekly_info": {}}

            for week_info in weekly_info:
                year_nr = datetime.datetime.strptime(week_info["start"], "%Y%m%d").year
                week_nr = datetime.datetime.strptime(week_info["start"], "%Y%m%d").isocalendar().week
                week_nr_str = "%04d-W%02d" % (year_nr, week_nr)

                # week_end_day cannot be in the future
                week_last_day = datetime.datetime.strptime(week_info["start"], "%Y%m%d") + datetime.timedelta(days=6)
                if week_last_day > datetime.datetime.today():
                    week_end_day = stop
                else:
                    week_end_day = week_last_day.strftime("%Y%m%d")

                week_stats["weekly_info"][week_nr_str] = {"start_date": week_info["start"],
                                                          "end_date": week_end_day,
                                                          "total_days": week_info["total_days"],
                                                          "active_days": week_info["active_days"],
                                                          "km": week_info["km"],
                                                          "sec": week_info["sec"],
                                                          "wh": week_info["wh"],
                                                          "first_record": week_info["first_record"]}
            self.__week_stats = WeekStats(week_stats)
        return self.__week_stats

    def month_stats(self, year: int, month: int, num_months: int = 1) -> MonthStats:
        if self.__month_stats is None:
            # start day cannot be in the future
            start_date = datetime.date(year, month, 1)
            if start_date > datetime.date.today():
                raise Exception("Start date is in the future")
            start = "%04d%02d%02d" % (year, month, 1)

            # set stop_date to today if it is in the future
            stop_month = (month + num_months - 2) % 12 + 1
            stop_year = year + (month + num_months - 2) // 12
            stop_date = datetime.date(stop_year, stop_month, calendar.monthrange(stop_year, stop_month)[1])
            if stop_date > datetime.date.today():
                stop = datetime.date.today().strftime("%Y%m%d")
            else:
                stop = "%04d%02d%02d" % (stop_year, stop_month, calendar.monthrange(stop_year, stop_month)[1])

            avg_rec = self._connection.get_endpoint("bike/statistics/extra_data/",
                                        params={"end": stop, "resolution": "months"})
            monthly_info = self._connection.get_endpoint("bike/statistics/",
                                             params={"start": start, "end": stop, "resolution": "months"},
                                             full_list=True)

            month_stats = {"start_date": start,
                           "end_date": stop,
                           "total_months": len(monthly_info),
                           "km_avg_12_months": avg_rec["km_avg_12_months"],
                           "month_record": avg_rec["month_record"],
                           "monthly_info": {}}

            for month_info in monthly_info:
                year_nr = datetime.datetime.strptime(month_info["start"], "%Y%m%d").year
                month_nr = datetime.datetime.strptime(month_info["start"], "%Y%m%d").month
                month_nr_str = "%04d-%02d" % (year_nr, month_nr)
                month_end_day = calendar.monthrange(year_nr, month_nr)[1]

                # end_day cannot be future date
                if datetime.date(year_nr, month_nr, month_end_day) > datetime.date.today():
                    end_date = stop
                else:
                    end_date = "%04d%02d%02d" % (year_nr, month_nr, month_end_day)

                month_stats["monthly_info"][month_nr_str] = {"start_date": month_info["start"],
                                                             "end_date": end_date,
                                                             "total_days": month_info["total_days"],
                                                             "active_days": month_info["active_days"],
                                                             "km": month_info["km"],
                                                             "sec": month_info["sec"],
                                                             "wh": month_info["wh"],
                                                             "first_record": month_info["first_record"]}
            self.__month_stats = MonthStats(month_stats)
        return self.__month_stats

    def year_stats(self, year: int, num_years: int = 1) -> YearStats:
        if self.__year_stats is None:
            # start day cannot be in the future
            start_date = datetime.date.fromisocalendar(year, 1, 1)
            if start_date > datetime.date.today():
                raise Exception("Start date is in the future")
            start = "%04d%02d%02d" % (year, 1, 1)

            # set stop_date to today if it is in the future
            stop_date = datetime.date(year + num_years - 1, 12, 31)
            if stop_date > datetime.date.today():
                stop = datetime.date.today().strftime("%Y%m%d")
            else:
                stop = stop_date.strftime("%Y%m%d")

            avg_rec = self._connection.get_endpoint("bike/statistics/extra_data/",
                                        params={"end": stop, "resolution": "years"})
            yearly_info = self._connection.get_endpoint("bike/statistics/",
                                            params={"start": start, "end": stop, "resolution": "years"},
                                            full_list=True)

            year_stats = {"start_date": start,
                          "end_date": stop,
                          "total_years": len(yearly_info),
                          "km_avg_years_since_beginning": avg_rec["km_avg_years_since_beginning"],
                          "year_record": avg_rec["year_record"],
                          "yearly_info": {}}

            for year_info in yearly_info:
                year_nr = datetime.datetime.strptime(year_info["start"], "%Y%m%d").year

                # end_date cannot be in the future
                if datetime.date(year_nr, 12, 31) > datetime.date.today():
                    end_date = stop
                else:
                    end_date = "%04d%02d%02d" % (year_nr, 12, 31)

                year_stats["yearly_info"][str(year_nr)] = {"start_date": year_info["start"],
                                                           "end_date": end_date,
                                                           "total_days": year_info["total_days"],
                                                           "active_days": year_info["active_days"],
                                                           "km": year_info["km"],
                                                           "sec": year_info["sec"],
                                                           "wh": year_info["wh"],
                                                           "first_record": year_info["first_record"]}
            self.__year_stats = YearStats(year_stats)
        return self.__year_stats
