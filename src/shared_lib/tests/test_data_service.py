import unittest
import pandas as pd

from shared_lib.bll.data_source_service import get_data


class TestDataService(unittest.TestCase):
    def test_get_data_not_empty(self):
        # 调用 get_data 方法
        df = get_data()
        # 检查 df 不为空
        self.assertTrue(isinstance(df, pd.DataFrame), "返回的不是 DataFrame 类型")
        self.assertFalse(df.empty, "返回的 DataFrame 为空")


if __name__ == '__main__':
    unittest.main()
