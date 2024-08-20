import unittest
from pathlib import Path
import pandas as pd
from shared_lib.bll.diff_calculator import DiffCalculatorSP500
from shared_lib.models.enums import ResolutionLevel
from shared_lib.models.time_series import TimeSeriesElement


# Assuming PairTradingDiffCalculatorFixLengthWindow and TimeSeriesElement are already defined

class TestDiffCalculator(unittest.TestCase):

    def load_time_series(self, full_path_filename):
        """
        Load time series data from CSV using pandas.
        The CSV file should have the format: DateTime,Open,High,Low,Close,Volume.
        :param full_path_filename: Path to the CSV file.
        :return: List of TimeSeriesElement instances.
        """
        # Read the CSV file
        df = pd.read_csv(full_path_filename, parse_dates=['DateTime'])

        # Convert the DataFrame to a list of TimeSeriesElement instances
        time_series = [
            TimeSeriesElement(row['DateTime'], row['Close'])
            for _, row in df.iterrows()
        ]

        return time_series

    def test_calculate_diff(self):
        symbol1 = "AAPL"
        symbol2 = "ABNB"

        # Load data from CSV files
        time_series1 = self.load_time_series(Path(__file__).parent / f"data/{symbol1}.csv")
        time_series2 = self.load_time_series(Path(__file__).parent / f"data/{symbol2}.csv")

        # Initialize the calculator
        calculator = DiffCalculatorSP500(symbol1, symbol2, resolution=ResolutionLevel.Hourly)

        # Update the time series in the calculator
        calculator.update_time_series(time_series1, time_series2)

        # Choose an endDateTime for the calculation, or use None to use the latest available
        end_date_time = None

        # Perform the diff calculation
        diff = calculator.calculate_diff(end_date_time)

        # Assert that the diff is within an expected range (for this example, we'll assume 0 is the expected value)
        self.assertAlmostEqual(5.259246, diff, places=4)

    def test_generate_diff_equation_should_work(self):
        symbol1 = "DASH"
        symbol2 = "ALGO"

        # Load data from CSV files
        time_series1 = self.load_time_series(Path(__file__).parent / f"data/{symbol1}USDT.csv")
        time_series2 = self.load_time_series(Path(__file__).parent / f"data/{symbol2}USDT.csv")

        # Initialize the calculator
        calculator = DiffCalculatorSP500(symbol1, symbol2, resolution=ResolutionLevel.Hourly)

        # Update the time series in the calculator
        calculator.update_time_series(time_series1, time_series2)

        # Choose an endDateTime for the calculation, or use None to use the latest available
        end_date_time = None

        # Perform the diff equation generation
        equation = calculator.print_equation(end_date_time)

        self.assertIsNotNone(equation)
        print(equation)


if __name__ == '__main__':
    unittest.main()
