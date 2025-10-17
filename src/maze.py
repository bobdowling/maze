import pydantic


class Item(pydantic.BaseModel):
    """An item a player may encounter in a room
    and which the player may be able to carry with them.
    """

    name: str = pydantic.Field(
        description="The name of the item as appearing in inventory lists.",
    )


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
