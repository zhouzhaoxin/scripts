import os
from unittest import TestCase
from src.excel import write_line_by_line

BASE_DIR = os.getcwd()


class TestUtils(TestCase):
    def setUp(self):
        self.new_row_data = [
            ['a', 'b', 'c', 'd', ],
            ['e', 'f', 'g', 'h', ],
        ]
        self.file_path = '{}/test.xlsx'.format(BASE_DIR)

    def test_write_line_by_line(self):
        write_line_by_line(self.file_path, self.new_row_data)
