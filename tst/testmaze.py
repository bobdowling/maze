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


class TestItem(unittest.TestCase):
    def testCreation(self) -> None:
        NAME = "Broadsword"
        thing = maze.Item(name=NAME)
        self.assertEqual(thing.name, NAME)

    def testKeywords(self) -> None:
        with self.assertRaises(pydantic.ValidationError):
            thing = maze.Item()  # type: ignore


class TestDirection(unittest.TestCase):
    def testCreation(self) -> None:
        xy = (1, 0)
        direction = maze.Direction(coordinates=xy)
        self.assertEqual(direction.coordinates, xy)

    def testNegation(self) -> None:
        xy1 = (1, 0)
        xy2 = (-1, 0)
        direction1 = maze.Direction(coordinates=xy1)
        direction2 = -direction1
        self.assertEqual(direction2.coordinates, xy2)

    def testHash0(self) -> None:
        xy = (1, 0)
        direction1 = maze.Direction(coordinates=xy)
        direction2 = -direction1
        direction3 = -direction2
        self.assertNotEqual(id(direction1), id(direction3))
        self.assertNotEqual(id(direction1.coordinates), id(direction3.coordinates))
        self.assertEqual(hash(direction1), hash(direction3))

    def testHash1(self) -> None:
        xy = (1, 0)
        direction1 = maze.Direction(coordinates=xy)
        direction2 = -direction1
        self.assertNotEqual(hash(direction1), hash(direction2))

    def testAll(self) -> None:
        target_vectors = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        created_vectors = [d.coordinates for d in maze.Direction.all(2)]
        self.assertEqual(target_vectors, created_vectors)


class TestCoordinates(unittest.TestCase):
    def testCreation(self) -> None:
        xy = (1, 0)
        c = maze.Coordinates(coordinates=xy)
        self.assertEqual(c.coordinates, xy)

    def testAdd(self) -> None:
        xy1 = (1, 0)
        delta = (0, 1)
        xy2 = (1, 1)
        c1 = maze.Coordinates(coordinates=xy1)
        d = maze.Direction(coordinates=delta)
        c2 = c1 + d
        self.assertEqual(c2.coordinates, xy2)


class TestRoom(unittest.TestCase):
    def testCreationDefault(self) -> None:
        xy = (1, 0)
        c = maze.Coordinates(coordinates=xy)
        room = maze.Room(coordinates=c)
        self.assertEqual(room.coordinates, c)
        self.assertEqual(len(room.doors), 0)
        self.assertEqual(len(room.contents), 0)

    def testCreation1(self) -> None:
        xy = (1, 0)
        c = maze.Coordinates(coordinates=xy)
        s = maze.Item(name="Broadsword")
        room = maze.Room(coordinates=c, contents={s})
        self.assertEqual(room.coordinates, c)
        self.assertEqual(len(room.doors), 0)
        self.assertEqual(len(room.contents), 1)


class TestMaze(unittest.TestCase):
    def testCreationDefault(self) -> None:
        m = maze.Maze()
        self.assertEqual(len(m.rooms), 0)
        self.assertEqual(m.limits.coordinates, (3, 4))

    def testAddRoom1(self) -> None:
        m = maze.Maze()
        c = maze.Coordinates(coordinates=(1, 2))
        r = maze.Room(coordinates=c)
        self.assertEqual(len(m.rooms), 0)
        m.add_room(r)
        self.assertEqual(len(m.rooms), 1)

    def testAddRoom2(self) -> None:
        m = maze.Maze()
        c = maze.Coordinates(coordinates=(10, 20))
        r = maze.Room(coordinates=c)
        with self.assertRaises(ValueError):
            m.add_room(r)

    def testAddRoom3(self) -> None:
        m = maze.Maze()
        c1 = maze.Coordinates(coordinates=(1, 2))
        c2 = maze.Coordinates(coordinates=(1, 2))
        r1 = maze.Room(coordinates=c1)
        r2 = maze.Room(coordinates=c2)
        self.assertNotEqual(id(c1), id(c2))
        self.assertNotEqual(id(r1), id(r2))
        m.add_room(r1)
        with self.assertRaises(ValueError):
            m.add_room(r2)

    def testCreate(self) -> None:
        M = 3
        N = 4
        limits = maze.Coordinates(coordinates=(M, N))
        m = maze.Maze(limits=limits)
        r = random.Random(x=0)
        m.create(r)
        self.assertEqual(len(m.rooms), M * N)


if __name__ == "__main__":
    unittest.main()
