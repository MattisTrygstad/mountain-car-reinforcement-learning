

from math import pi
from enums import BoardType, NodeState
from environment.universal_state import UniversalState
from utils.config_parser import Config
from utils.trigonometry import rotation_matrix


class HexagonalGridState(UniversalState):

    def __init__(self) -> None:
        super().__init__()

        self.neighbors = [(-1, -1), (-1, 0), (0, -1), (0, 1), (1, 0), (1, 1)]
        self.size = Config.board_size

        self.edges = []  # [((x,y),(i,j)),...)]
        self.node_names = {}  # (row, col): str
        self.node_coordinates = {}  # (row,col): (x_value, y_value)

        # Describes the last executed action
        self.start_pos = ()
        self.end_pos = ()

        self.__generate_nodes()
        self.__generate_edges()
        self.__generate_coordinates()

    def __generate_nodes(self) -> None:
        if Config.board_type == BoardType.TRIANGLE.value:
            for row in range(self.size):
                for col in range(row + 1):
                    self.nodes[(row, col)] = NodeState.OCCUPIED.value
                    self.node_names[(row, col)] = f'{row},{col}'
        elif Config.board_type == BoardType.DIAMOND.value:
            for row in range(self.size):
                for col in range(self.size):
                    # Constuct two right triangles, which together will form a parallelogram. Will be offset to a diamond pattern when visualizing.
                    if row >= col:
                        # Top triangle
                        self.nodes[(row, col)] = NodeState.OCCUPIED.value
                        self.node_names[(row, col)] = f'{row},{col}'
                    else:
                        # Bottom triangle
                        self.nodes[(row + self.size, col)] = NodeState.OCCUPIED.value
                        self.node_names[(row + self.size, col)] = f'{row + self.size}, {col}'

        # Set empty nodes
        for (row, col) in Config.empty_nodes:
            self.nodes[(row, col)] = NodeState.EMPTY.value

    def __generate_edges(self) -> None:
        for (row, col) in self.nodes.keys():
            for (x, y) in self.neighbors:
                if (row + x, col + y) in self.nodes:
                    self.edges.append(((row, col), (row + x, col + y)))

    def __generate_coordinates(self) -> None:
        for (row, col) in self.nodes:
            # Rotate entire grid 90deg to match action offsets
            (x, y) = rotation_matrix(row, col, -pi / 2)

            # Offset in x direction (parallelogram -> diamond and right triangle -> equilateral triangle)
            self.node_coordinates[(row, col)] = (x + 1 / 2 * y, y)

    def get_empty_nodes(self) -> dict:
        return {key: value for (key, value) in self.nodes.items() if value == NodeState.EMPTY.value}

    def get_occupied_nodes(self) -> dict:
        return {key: value for (key, value) in self.nodes.items() if value == NodeState.OCCUPIED.value}

    def get_legal_actions(self) -> list:
        legal_actions = []  # [((x,y),(i,j)),...]

        for (row, col) in self.get_occupied_nodes().keys():
            for x, y in self.neighbors:
                jumped_node = (row + x, col + y)
                end_node = (row + 2 * x, col + 2 * y)

                # Check if jumped node and landing node is on the grid
                if jumped_node not in self.nodes or end_node not in self.nodes:
                    continue

                # Check if jumped node and landing node has valid states
                if self.nodes[jumped_node] == NodeState.OCCUPIED.value and self.nodes[end_node] == NodeState.EMPTY.value:
                    legal_actions.append(((row, col), end_node))

        return legal_actions
