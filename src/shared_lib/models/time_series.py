from datetime import datetime


class TimeSeriesElement:
    def __init__(self, date_time: datetime, value: float):
        self.date_time = date_time
        self.value = value

    def __str__(self):
        return f"DateTime: {self.date_time}, Value: {self.value}"

    def __eq__(self, other):
        if not isinstance(other, TimeSeriesElement):
            return False
        return self.date_time == other.date_time and self.value == other.value

    def __hash__(self):
        return hash((self.date_time, self.value))


class TimeSeries:
    def __init__(self):
        self.series = []

    def __str__(self):
        return f"TimeSeries with {len(self.series)} elements: [{', '.join(str(elm) for elm in self.series)}]"

    def __eq__(self, other):
        if not isinstance(other, TimeSeries):
            return False
        return self.series == other.series

    def __hash__(self):
        return hash(tuple(self.series))
