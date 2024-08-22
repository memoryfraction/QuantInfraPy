import unittest
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from matplotlib.ticker import MaxNLocator
from src.shared_lib.bll.diff_calculator import DiffCalculatorSP500
from src.shared_lib.models.enums import ResolutionLevel
from src.shared_lib.models.time_series import *

# Assuming PairTradingDiffCalculatorFixLengthWindow and TimeSeriesElement are already defined

class TestSP500DiffCalculator(unittest.TestCase):

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

        # Perform the diff calculation
        calculator.update_diff_and_equation()

        # Assert that 'diff' column is not empty
        self.assertFalse(calculator.df['diff'].isna().all(), "The 'diff' column should not be all NaN")

        # Assert that 'equation' column is not empty
        self.assertFalse(calculator.df['equation'].isna().all(), "The 'equation' column should not be all NaN")

        # Optionally, print some values for debugging
        print(calculator.df[['diff', 'equation']].tail())

    def test_draw_diff_chart(self):
        symbol1 = "AAPL"
        symbol2 = "ABNB"

        # Load data from CSV files
        time_series1 = self.load_time_series(Path(__file__).parent / f"data/{symbol1}.csv")
        time_series2 = self.load_time_series(Path(__file__).parent / f"data/{symbol2}.csv")

        # Initialize the calculator
        calculator = DiffCalculatorSP500(symbol1, symbol2, resolution=ResolutionLevel.Hourly)

        # Update the time series in the calculator
        calculator.update_time_series(time_series1, time_series2)

        # Perform the diff calculation
        calculator.update_diff_and_equation()

        # 使用calculator.df中diff列所有有值的行，绘制chart。 其中：横轴为self.df中date_time中的值(日期格式)，纵轴为diff列的值(float类型)
        # Filter out rows where 'diff' is NaN
        df_diff = calculator.df.dropna(subset=['diff'])

        # Ensure 'date_time' is used as the index for plotting
        df_diff.set_index('date_time', inplace=True)

        # Plotting the 'diff' column
        plt.figure(figsize=(12, 6))
        plt.plot(df_diff.index, df_diff['diff'], marker='o', linestyle='-', color='b', label='Diff')

        # Formatting the x-axis to show dates
        plt.xlabel('Date')
        plt.ylabel('Diff')
        plt.title(f'Diff Chart for {symbol1} and {symbol2}')
        plt.legend()
        plt.grid(True)

        # Set x-axis to date format
        plt.gca().xaxis.set_major_locator(MaxNLocator(10))  # Limit the number of ticks on x-axis
        plt.gca().xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))  # Set date format

        plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
        plt.tight_layout()

        # Save or show the plot
        plt.savefig(f"diff_chart_{symbol1}_{symbol2}.png")  # Save the chart as a PNG file
        plt.show()  # Display the chart

    def test_single_update(self):
        symbol1 = "AAPL"
        symbol2 = "ABNB"

        # Load data from CSV files
        time_series1 = self.load_time_series(Path(__file__).parent / f"data/{symbol1}.csv")
        time_series2 = self.load_time_series(Path(__file__).parent / f"data/{symbol2}.csv")

        # Initialize the calculator
        calculator = DiffCalculatorSP500(symbol1, symbol2, resolution=ResolutionLevel.Hourly)

        # Update the time series in the calculator
        calculator.update_time_series(time_series1, time_series2)

        # init fake data for 2024-8-1, for AAPL, and ABNB, named: series_a_elm and series_b_elm
        fake_date = datetime(2024, 8, 1, 9, 30)
        fake_value_symbol1 = 218.0  # Example value for AAPL
        fake_value_symbol2 = 135.0  # Example value for ABNB

        # Create TimeSeriesElement instances with fake data
        series_a_elm = TimeSeriesElement(date_time=fake_date, value=fake_value_symbol1)
        series_b_elm = TimeSeriesElement(date_time=fake_date, value=fake_value_symbol2)
        calculator.update_time_series_element(series_a_elm, series_b_elm)

        # Optionally, print some values for debugging
        print(calculator.df.tail())


if __name__ == '__main__':
    unittest.main()
