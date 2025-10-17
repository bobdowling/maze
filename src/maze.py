import pydantic
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
        return all(
            coordinate >= 0 and coordinate < limit
            for coordinate, limit in zip(
                coordinates.coordinates, self.limits.coordinates
            )
        )
