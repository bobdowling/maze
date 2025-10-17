from pathlib import Path
import pydantic
import sys
import unittest

f = Path(__file__)
s = f.parent.parent / "src"
sys.path.append(str(s))
print(__file__)
del f, s
import maze  # type: ignore


class TestItem(unittest.TestCase):
    def testCreation(self) -> None:
        NAME = "Broadsword"
        thing = maze.Item(name=NAME)
        self.assertEqual(thing.name, NAME)

    def testKeywords(self) -> None:
        with self.assertRaises(pydantic.ValidationError):
            thing = maze.Item()  # type: ignore


if __name__ == "__main__":
    unittest.main()
