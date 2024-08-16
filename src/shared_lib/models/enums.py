from enum import Enum

class ResolutionLevel(Enum):
    Tick = "t"
    Second = "s"
    Minute = "min"
    Hourly = "h"
    Daily = "d"
    Weekly = "wk"
    Monthly = "mo"
    Other = "other"
