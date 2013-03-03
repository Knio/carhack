import re

from time_series import TimeSeriesInterface
get_logger = TimeSeriesInterface.get_handler

from sqlite_logger import SQLiteTimeSeries
from struct_logger import StructTimeSeries
