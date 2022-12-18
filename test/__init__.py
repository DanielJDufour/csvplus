import csv
import os
import shutil
from unittest import TestCase
import csvplus

directory = os.path.dirname(os.path.realpath(__file__))

src = os.path.join(directory, "_cars.csv")
test_file = os.path.join(directory, "cars.csv")
original = open(src).read()


def _count(filepath, where={}):
    with open(filepath) as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    for key, value in where.items():
        rows = [row for row in rows if row[key] != value]
    return len(rows)


def read_test_file():
    with open(test_file) as f:
        return f.read()


class BaseTestCase(TestCase):
    def setUp(self):
        shutil.copyfile(src, test_file)


class AddTests(BaseTestCase):
    def test_add(self):
        csvplus.add(test_file, {"make": "Tesla", "model": "Roadster", "year": 2011})
        self.assertNotEqual(read_test_file(), original)
        self.assertEqual(_count(test_file), _count(src) + 1)


class MoveTests(BaseTestCase):
    def test_move_item(self):
        self.assertEqual(csvplus._move_item([1, 2, 3, 4], 1, 2), [1, 2, 3, 4])
        self.assertEqual(csvplus._move_item([1, 2, 3, 4], 0, 2), [2, 1, 3, 4])
        self.assertEqual(csvplus._move_item([1, 2, 3, 4], 3, 0), [4, 1, 2, 3])

    def test_move(self):
        rows = csvplus.move(test_file, 0, 4)
        self.assertEqual(len(rows), 3)
        self.assertNotEqual(read_test_file(), original)
        self.assertEqual(read_test_file().split("\n")[1], '"nissan","kicks","2022"')


class ReadTests(BaseTestCase):
    def test_read(self):
        rows = csvplus.read(test_file, {"make": "nissan"})
        self.assertEqual(len(rows), 2)

    def test_read_capitalized(self):
        rows = csvplus.read(test_file, {"make": "Nissan"})
        self.assertEqual(len(rows), 0)


class ExistsTests(BaseTestCase):
    def test_exists(self):
        self.assertFalse(csvplus.exists(test_file, {"make": "Fake"}))
        self.assertTrue(csvplus.exists(test_file, {"make": "nissan"}))


class UpdateTests(BaseTestCase):
    def test_update_without_where(self):
        print("test_update_without_where")
        csvplus.update(test_file, where={}, data={"year": "2022"})
        self.assertNotEqual(read_test_file(), original)

    def test_update_with_where(self):
        print("test_update_with_where")
        csvplus.update(test_file, where={"make": "nissan"}, data={"year": "-1"})
        contents = read_test_file()
        self.assertNotEqual(contents, original)
        self.assertEqual(
            contents.strip(),
            '''"make","model","year"\n"nissan","altima","-1"\n"nissan","kicks","-1"\n"toyota","camry","1982"''',
        )


class DeleteTests(BaseTestCase):
    def test_delete_without_where(self):
        csvplus.delete(test_file)
        self.assertEqual(read_test_file(), original)

    def test_case_sensitivity(self):
        csvplus.delete(test_file, debug_level=2, where={"make": "Nissan"})
        self.assertNotEqual(read_test_file(), original)

    def test_case_sensitivity(self):
        csvplus.delete(test_file, debug_level=2, where={"make": "nissan"})
        self.assertNotEqual(read_test_file(), original)
