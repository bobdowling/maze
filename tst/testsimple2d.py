from pathlib import Path
import pydantic
import random
import sys
import unittest

f = Path(__file__)
s = f.parent.parent / "src"
sys.path.append(str(s))
print(__file__)
del f, s
import maze  # type: ignore
import simple2d  # type: ignore


class TestSimple2D(unittest.TestCase):
    def testCreation(self) -> None:
        M, N = 5, 6
        thing = simple2d.SimpleMaze2D(M, N)
        self.assertEqual((M, N), thing.limits.coordinates)


if __name__ == "__main__":
    unittest.main()
