import pydantic


class Item(pydantic.BaseModel):
    """An item a player may encounter in a room
    and which the player may be able to carry with them.
    """

    name: str = pydantic.Field(
        description="The name of the item as appearing in inventory lists.",
    )
