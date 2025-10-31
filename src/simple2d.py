import maze
import svg


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
