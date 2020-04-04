import datetime
from math import ceil

COST_PER_DAY_SUMMER = 4.3
COST_PER_DAY_WINTER = 1


def count_parking_fee(date_from, date_to, yacht):
    date_from = datetime.datetime.combine(date_from, datetime.time(0, 0))
    date_to = datetime.datetime.combine(date_to, datetime.time(0, 0))
    price = 0
    this_year = datetime.date.today().year
    start_summer_season = datetime.datetime(this_year, 5, 1)
    end_summer_season = datetime.datetime(this_year, 10, 31)
    start_winter_season = datetime.datetime(this_year, 11, 1)
    end_winter_season = datetime.datetime(this_year + 1, 4, 30)

    if start_summer_season <= date_from <= end_summer_season:
        if date_to <= end_summer_season:
            # od /sezon letni/ do /sezon letni/
            price = summer_fee(date_from, date_to, yacht)
        elif date_from == start_summer_season and date_to == end_winter_season:
            # od początku sezonu letniego do końca sezonu zimowego (REZYDENT CALOROCZNY)
            summer = summer_fee(start_summer_season, end_summer_season, yacht)
            winter = winter_fee(start_winter_season, end_winter_season, yacht)
            price = summer + winter / 2
        elif date_to > end_summer_season:
            # od /sezon letni/ do /sezon zimowy/
            summer = summer_fee(date_from, end_summer_season, yacht)
            winter = winter_fee(start_winter_season, date_to, yacht)
            price = summer + winter
    elif end_summer_season < date_from <= end_winter_season:
        price = winter_fee(date_from, date_to, yacht)
    else:
        price = winter_fee(date_from, date_to, yacht)
    return price


def count_days(date_from, date_to):
    number_of_days = date_to - date_from
    return number_of_days.days + 1


def summer_fee(date_from, date_to, yacht):
    number_of_days = count_days(date_from, date_to)

    if number_of_days == 184:
        return COST_PER_DAY_SUMMER * number_of_days * ceil(yacht['length']) * 0.7
    else:
        return COST_PER_DAY_SUMMER * number_of_days * ceil(yacht['length'])


def winter_fee(date_from, date_to, yacht):
    number_of_days = count_days(date_from, date_to)
    return COST_PER_DAY_WINTER * ceil(yacht['length']) * ceil(yacht['width']) * number_of_days
