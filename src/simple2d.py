import maze
import svg


def room_svg_group(
    room: maze.Room,
    width: int,
    height: int,
    ds: int = 25,  # door size
    sw: int = 5,  # stroke width
    stroke_colour: str = "#ffa500",
    ident: str = "room",
) -> svg.G:
    """Given a room in a maze, generate the SVG group (G) that draws the room.
    The top-left/north-west corner of the room is at (0,0). This expect the group to then
    be translated into place by the calling function. Recall that the stroke is symmetric
    about the corner point so will stretch outside of the "simple" rectangle.
    Parameters:
        room: used to get the door bools
        width, height: Size of the room.
        ds: Door Size.
        sw: Stroke Width: Thickness of walls.
        stroke_colour: Hex of colour to be used for the strokes
        ident: The SVG id assigned to the group.
    """
    if ds < width - 2:
        dx = (width - ds) // 2
    else:
        raise ValueError(f"room_svg(): Impossible door size: {ds=}: {width=}")
    if ds < height - 2:
        dy = (height - ds) // 2
    else:
        raise ValueError(f"room_svg(): Impossible door size: {ds=}: {height=}")

    style_elements = [
        "fill:none",
        f"stroke:{stroke_colour}",
        f"stroke-width:{sw}",
    ]
    style_argument = ";".join(style_elements)

    elements: list[svg.Element] = []

    # walls
    corner_NW = svg.Polyline(
        points=[0, dy, 0, 0, dx, 0],
        style=style_argument,
        id=f"{ident}_NW",
    )
    corner_NE = svg.Polyline(
        points=[dx + ds, 0, 2 * dx + ds, 0, 2 * dx + ds, dy],
        style=style_argument,
        id=f"{ident}_NE",
    )
    corner_SE = svg.Polyline(
        points=[2 * dx + ds, dy + ds, 2 * dx + ds, 2 * dy + ds, dx + ds, 2 * dy + ds],
        style=style_argument,
        id=f"{ident}_SE",
    )
    corner_SW = svg.Polyline(
        points=[dx, 2 * dy + ds, 0, 2 * dy + ds, 0, dy + ds],
        style=style_argument,
        id=f"{ident}_SW",
    )
    elements += [corner_NW, corner_NE, corner_SE, corner_SW]
    # doors / walls
    # North
    direction = maze.Direction(coordinates=(0, -1))
    if direction not in room.doors:
        wall = svg.Line(
            x1=dx,
            y1=0,
            x2=dx + ds,
            y2=0,
            style=style_argument,
            id=f"{ident}_N",
        )
        elements.append(wall)
    # East
    direction = maze.Direction(coordinates=(1, 0))
    if direction not in room.doors:
        wall = svg.Line(
            x1=2 * dx + ds,
            y1=dy,
            x2=2 * dx + ds,
            y2=dy + ds,
            style=style_argument,
            id=f"{ident}_E",
        )
        elements.append(wall)
    # South
    direction = maze.Direction(coordinates=(0, 1))
    if direction not in room.doors:
        wall = svg.Line(
            x1=dx + ds,
            y1=2 * dy + ds,
            x2=dx,
            y2=2 * dy + ds,
            style=style_argument,
            id=f"{ident}_S",
        )
        elements.append(wall)
    # West
    direction = maze.Direction(coordinates=(-1, 0))
    if direction not in room.doors:
        wall = svg.Line(
            x1=0,
            y1=dy + ds,
            x2=0,
            y2=dy,
            style=style_argument,
            id=f"{ident}_W",
        )
        elements.append(wall)

    group = svg.G(
        elements=elements,
        id=f"{ident}_g",
    )
    return group


class SimpleMaze2D(maze.Maze):
    def __init__(
        self,
        M: int,
        N: int,
    ) -> None:
        """Create a M×N 2-D maze."""
        super().__init__(
            limits=maze.Coordinates(coordinates=(M, N)),
        )

    def svg(
        self,
        width: int = 25,
        height: int = 25,
        sw: int = 5,
        stroke_color: str = "#ffa500",
    ) -> svg.SVG:
        ds = min(width, height) // 3
        svg_rooms: list[svg.Element] = list()
        for location, room in self.rooms.items():
            x, y = location.coordinates
            transform = svg.Translate(x=x * width, y=y * height)
            svg_room = room_svg_group(room, width, height, ds=ds, ident=f"room_{x}_{y}")
            svg_room.transform = [transform]
            svg_rooms.append(svg_room)
        whole = svg.SVG(elements=svg_rooms)
        return whole
