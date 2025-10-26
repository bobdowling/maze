import logging
import pydantic
import random
import uuid


class Item(pydantic.BaseModel):
    """An item a player may encounter in a room
    and which the player may be able to carry with them.
    """

    name: str = pydantic.Field(
        description="The name of the item as appearing in inventory lists.",
    )
    ident: uuid.UUID = pydantic.Field(
        description="UUID to keep things unique and hashable. (Not intended for direct user access.)",
        default_factory=uuid.uuid4,
    )

    def __hash__(self):
        return self.ident.__hash__()


class Direction(pydantic.BaseModel):
    """A direction out of a room in the maze."""

    coordinates: tuple[int, ...] = pydantic.Field(
        description="The values of the coordinates of the direction.",
    )

    def __neg__(self) -> "Direction":
        """Directions are used as the labels for doors out of a room in the maze.
        The assumption is that if direction D leads from room A to room B then direction -D will lead from
        room B to room A.
        """
        xyz = tuple(-x for x in self.coordinates)
        return Direction(coordinates=xyz)

    def __hash__(self):
        return self.coordinates.__hash__()

    @classmethod
    def all(
        cls,
        ND: pydantic.PositiveInt,
    ) -> list["Direction"]:
        """Give a list of all possible directions (ignoring walls, etc.)
        You may want to override this class method for funky topologies.
        These directions come in a predictable order. It is up to the caller
        to shuffle them if randomness is required.
        """
        all_directions = []
        for index in range(ND):
            for offset in [-1, 1]:
                vector = [0] * ND
                vector[index] = offset
                direction = cls(coordinates=tuple(vector))
                all_directions.append(direction)
        return all_directions


class Coordinates(pydantic.BaseModel):
    """The location of a room in the maze."""

    coordinates: tuple[int, ...] = pydantic.Field(
        description="The values of the coordinates of the room.",
    )

    def __add__(
        self,
        offset: Direction,
    ) -> "Coordinates":
        """Given an offset from the current room, determine the coordinates of the target room."""
        if len(self.coordinates) != len(offset.coordinates):
            raise ValueError(
                f"Coordinates.__add__: Dimension mismatch: {len(self.coordinates)=}: {len(offset.coordinates)=}",
            )
        xyz = tuple(a + b for a, b in zip(self.coordinates, offset.coordinates))
        return Coordinates(coordinates=xyz)

    def __hash__(self):
        return self.coordinates.__hash__()

    def __eq__(
        self,
        other,
    ) -> bool:
        if not isinstance(other, Coordinates):
            raise ValueError(
                f"Coordinates.__eq__: Can only compare Coordinates with Coordinates: {other}"
            )
        return self.coordinates == other.coordinates


class Room(pydantic.BaseModel):
    """A space in the maze.
    It will have routes to adjacent rooms and possibly contain items.
    """

    coordinates: Coordinates = pydantic.Field(
        description="The location of the room in the maze.",
    )
    doors: set[Direction] = pydantic.Field(
        description="A set of the directions in which there is a door.",
        default=set(),
    )
    contents: set[Item] = pydantic.Field(
        description="A set of the items in the room.",
        default=set(),
    )

    def __hash__(self):
        return self.coordinates.__hash__()


class Maze(pydantic.BaseModel):
    rooms: dict[Coordinates, Room] = pydantic.Field(
        description="The rooms of the maze, indexed by their coordinates.",
        default=dict(),
    )
    limits: Coordinates = pydantic.Field(
        description="The size of the maze in each direction, specified as the coordinates of the extreme corner.",
        default=Coordinates(coordinates=(3, 4)),
    )

    def _in_bounds(
        self,
        coordinates: Coordinates,
    ) -> bool:
        # logging.debug(f"Make._in_bounds(): ENTRY: {coordinates}")
        return all(
            coordinate >= 0 and coordinate < limit
            for coordinate, limit in zip(
                coordinates.coordinates, self.limits.coordinates
            )
        )

    def add_room(
        self,
        room: Room,
    ) -> None:
        logging.debug(f"Make.add_room(): ENTRY: {room.coordinates}")
        if not self._in_bounds(room.coordinates):
            raise ValueError(
                f"Make.add_room: Coordinates of room not in bounds: {room.coordinates=}: {self.limits=}"
            )
        if room.coordinates in self.rooms:
            raise ValueError(
                f"Make.add_room: Room already in maze: {room.coordinates=}"
            )
        self.rooms[room.coordinates] = room
        logging.debug(f"Make.add_room(): EXIT: {room.coordinates}")

    def create(
        self,
        rnd: random.Random,
    ) -> None:
        logging.debug(f"Maze.create(): ENTRY")
        ND = len(self.limits.coordinates)
        logging.debug(f"Maze.create(): {ND=}")
        all_directions = Direction.all(ND)
        logging.debug(f"Maze.create(): {all_directions=}")
        location = Coordinates(coordinates=(0,) * ND)
        room_zero = Room(coordinates=location)
        self.add_room(room_zero)
        stack = [room_zero]
        logging.debug(f"Maze.create(): Entering stack loop")
        while stack:
            room = stack.pop()
            logging.debug(f"Maze.create(): Stack loop")
            while True:
                location = room.coordinates
                logging.debug(f"Maze.create(): Depth loop: {location}")
                rnd.shuffle(all_directions)
                room_created = False
                for direction in all_directions:
                    logging.debug(f"Maze.create(): Direction loop: {direction=}")
                    new_location = location + direction
                    logging.debug(f"Maze.create(): {new_location=}")
                    if not self._in_bounds(new_location):
                        logging.debug(f"Maze.create(): Out of bounds: {new_location}")
                        continue  # next direction
                    if new_location in self.rooms:
                        logging.debug(
                            f"Maze.create(): New location already in self.rooms: {new_location}"
                        )
                        continue  # next direction
                    logging.debug(
                        f"Maze.create(): Creating room for new location: {new_location}"
                    )
                    new_room = Room(coordinates=new_location)
                    room.doors.add(direction)
                    new_room.doors.add(-direction)
                    self.add_room(new_room)
                    stack.append(new_room)
                    room_created = True
                    room = new_room
                    break

                # None of the directions worked - pop from the stack
                if not room_created:
                    break  # break from the depth loop, return to the stack loop
