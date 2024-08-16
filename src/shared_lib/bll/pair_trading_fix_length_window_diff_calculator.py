from collections import deque
from datetime import datetime
from typing import List, Optional, Tuple, Set
import statsmodels.api as sm
import numpy as np
from shared_lib.models.enums import ResolutionLevel
from shared_lib.models.time_series import TimeSeriesElement


# Assuming TimeSeriesElement and ResolutionLevel are already defined

class PairTradingDiffCalculatorFixLengthWindow:
    FixedWindowLength = 183  # Default length, unit: days

    def __init__(self, symbol1: str, symbol2: str, resolution: ResolutionLevel = ResolutionLevel.Daily):
        self.symbol1 = symbol1
        self.symbol2 = symbol2
        self.resolution = resolution
        self.FixedWindowLength = self.calculate_window_length(resolution)
        self.time_series_queue1 = deque(maxlen=self.FixedWindowLength)
        self.time_series_queue2 = deque(maxlen=self.FixedWindowLength)
        self.time_series1: Set[TimeSeriesElement] = set()
        self.time_series2: Set[TimeSeriesElement] = set()

    def update_time_series(self, time_series1: List[TimeSeriesElement], time_series2: List[TimeSeriesElement]):
        if len(time_series1) != len(time_series2):
            raise ValueError("time_series1 and time_series2 must have the same number of elements.")

        for i in range(len(time_series1)):
            if time_series1[i].date_time != time_series2[i].date_time:
                raise ValueError(f"Element {i} of time_series1 and time_series2 have different DateTime values.")

        self.time_series1 = set(time_series1)
        self.time_series2 = set(time_series2)

        for element in time_series1:
            self.time_series_queue1.append(element)

        for element in time_series2:
            self.time_series_queue2.append(element)

    def update_time_series_element(self, time_series_elm1: TimeSeriesElement, time_series_elm2: TimeSeriesElement):
        if not self.validate_source_data():
            raise ValueError("Data source not valid, please execute update_time_series() first.")

        if time_series_elm1.date_time != time_series_elm2.date_time:
            raise ValueError("time_series_elm1 and time_series_elm2 must have the same DateTime.")

        self.time_series1.add(time_series_elm1)
        self.time_series2.add(time_series_elm2)

        self.time_series_queue1.append(time_series_elm1)
        self.time_series_queue2.append(time_series_elm2)

    def calculate_diff(self, end_datetime: Optional[datetime] = None) -> float:
        if not self.validate_source_data():
            raise ValueError("Data source not valid, please execute update_time_series() first.")

        if end_datetime is None:
            end_datetime = max(self.time_series1, key=lambda x: x.date_time).date_time

        series_a = [x.value for x in sorted(self.time_series1, key=lambda x: x.date_time, reverse=True) if
                    x.date_time <= end_datetime][:self.FixedWindowLength]
        series_b = [x.value for x in sorted(self.time_series2, key=lambda x: x.date_time, reverse=True) if
                    x.date_time <= end_datetime][:self.FixedWindowLength]

        if len(series_a) != self.FixedWindowLength or len(series_b) != self.FixedWindowLength:
            raise ValueError("Not enough data points to perform the calculation.")

        regression_result = self.ols_regression(series_a, series_b)
        a = regression_result["a"]
        constant = regression_result["constant"]
        lastElmInSeriesA = series_a[0] # 注意：此时SeriesA和SeriesB为DateTime倒序;
        lastElmInSeriesB = series_b[0] # 注意：此时SeriesA和SeriesB为DateTime倒序;
        diff = lastElmInSeriesA - (a * lastElmInSeriesB + constant) # use the last element to calculate diff
        return diff

    def print_equation(self, end_datetime: Optional[datetime] = None) -> str:
        if not self.validate_source_data():
            raise ValueError("Data source not valid, please execute update_time_series() first.")

        if end_datetime is None:
            end_datetime = max(self.time_series1, key=lambda x: x.date_time).date_time

        series_a = [x.value for x in sorted(self.time_series1, key=lambda x: x.date_time, reverse=True) if
                    x.date_time <= end_datetime][:self.FixedWindowLength]
        series_b = [x.value for x in sorted(self.time_series2, key=lambda x: x.date_time, reverse=True) if
                    x.date_time <= end_datetime][:self.FixedWindowLength]

        if len(series_a) != self.FixedWindowLength or len(series_b) != self.FixedWindowLength:
            raise ValueError("Not enough data points to perform the calculation.")

        regression_result = self.ols_regression(series_a, series_b)
        a = regression_result["a"]
        constant = regression_result["constant"]
        equation = f"diff = {self.symbol1} - ({float(a):.4f} * {self.symbol2} + {float(constant):.4f})"
        return equation

    def validate_source_data(self) -> bool:
        if not self.time_series1 or not self.time_series2:
            return False
        if len(self.time_series1) != len(self.time_series2):
            return False
        return True

    def calculate_window_length(self, resolution_level: ResolutionLevel) -> int:
        if resolution_level == ResolutionLevel.Daily:
            return self.FixedWindowLength
        elif resolution_level == ResolutionLevel.Weekly:
            return self.FixedWindowLength * 7
        elif resolution_level == ResolutionLevel.Monthly:
            return self.FixedWindowLength * 30
        elif resolution_level == ResolutionLevel.Hourly:
            return self.FixedWindowLength * 24
        elif resolution_level == ResolutionLevel.Minute:
            return self.FixedWindowLength * 24 * 60
        elif resolution_level == ResolutionLevel.Second:
            return self.FixedWindowLength * 24 * 60 * 60
        elif resolution_level == ResolutionLevel.Tick:
            return self.FixedWindowLength * 24 * 60 * 60 * 1000
        else:
            raise ValueError(f"Unsupported resolution level: {resolution_level}")

    def ols_regression(self, seriesA, seriesB):
        # 提取SeriesA和SeriesB
        series_a = np.array(seriesA)
        series_b = np.array(seriesB)

        # 在自变量中添加常数项以拟合截距
        series_b = sm.add_constant(series_b)

        # 拟合OLS模型
        model = sm.OLS(series_a, series_b)
        results = model.fit()

        # 返回回归系数和截距
        return {
            "a": results.params[1],  # 系数
            "constant": results.params[0]  # 截距
        }
