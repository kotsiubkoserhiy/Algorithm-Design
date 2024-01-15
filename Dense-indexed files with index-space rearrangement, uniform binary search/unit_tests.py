import unittest
import os
from DenseIndexFile import DenseIndexFile

class TestDenseIndexFile(unittest.TestCase):

    def setUp(self):
        self.test_file_name = "test_database.txt"
        self.db = DenseIndexFile(self.test_file_name)
        with open(self.test_file_name, 'w') as file:
            file.write("1,Data1\n")
            file.write("5,Data5\n")
            file.write("10,Data10\n")

    def tearDown(self):
        if self.test_file_name and os.path.exists(self.test_file_name):
            os.remove(self.test_file_name)

    def test_search_nonexistent_key(self):
        result = self.db.search(12)
        self.assertIsNone(result)

    def test_delete_existing_key(self):
        key_to_delete = 5
        self.db.delete(key_to_delete)
        self.assertNotIn(key_to_delete, self.db.index)

    def test_add_key(self):
        new_key = 6
        new_data = "Data6"
        self.db.add(new_key, new_data)
        result = self.db.search(new_key)
        self.assertEqual(result, new_data)

if __name__ == '__main__':
    unittest.main()