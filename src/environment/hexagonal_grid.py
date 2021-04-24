
from copy import deepcopy
from matplotlib import pyplot as plt
import numpy as np
from abstract_classes.environment import Environment
from enums import BoardType, Color, NodeState
import networkx as nx
from typing import Dict, Tuple
from environment.hexagonal_grid_state import HexagonalGridState
from environment.universal_action import UniversalAction
from environment.universal_state import UniversalState

from utils.config_parser import Config


class HexagonalGrid(Environment):

    def __init__(self, win_multiplier: int):
        self.state = HexagonalGridState()
        self.history = []

        if Config.board_type == BoardType.DIAMOND.value:
            self.fig, self.ax = plt.subplots(figsize=(7, 8))
        else:
            self.fig, self.ax = plt.subplots(figsize=(9, 7))

        self.G = nx.Graph()
        self.G.add_nodes_from(self.state.nodes)
        self.G.add_edges_from(self.state.edges)

        self.initial_nodes = len(self.state.get_occupied_nodes())
        self.win_multiplier = win_multiplier

    def execute_action(self, action: UniversalAction) -> int:
        self.history.append(deepcopy(self.state.nodes))

        (start_node, end_node) = action.action
        jumped_node = ((start_node[0] + end_node[0]) / 2, (start_node[1] + end_node[1]) / 2)

        self.state.start_pos = start_node
        self.state.end_pos = end_node

        self.state.nodes[start_node] = NodeState.EMPTY.value
        self.state.nodes[jumped_node] = NodeState.EMPTY.value
        self.state.nodes[end_node] = NodeState.OCCUPIED.value

        if self.check_win_condition():
            reinforcement = Config.reinforcement * self.win_multiplier
        else:
            reinforcement = Config.reinforcement / (len(self.state.get_occupied_nodes()) - 1)

        return reinforcement

    def undo_action(self) -> None:
        if self.history:
            self.state.nodes = self.history.pop()

    def get_legal_actions(self) -> list:
        return self.state.get_legal_actions()

    def check_win_condition(self) -> bool:
        num_occupied_nodes = len(self.state.get_occupied_nodes())
        if num_occupied_nodes == 1:
            return True
        else:
            return False

    def get_state(self) -> UniversalState:
        universal_state = UniversalState()
        universal_state.nodes = deepcopy(self.state.nodes)

        return universal_state

    def reset(self) -> None:
        self.state = HexagonalGridState()

        self.G = nx.Graph()
        self.G.add_nodes_from(self.state.nodes)
        self.G.add_edges_from(self.state.edges)

    def visualize(self, block: bool, delay: int = None) -> None:
        plt.cla()
        empty_nodes = self.state.get_empty_nodes()
        occupied_nodes = self.state.get_occupied_nodes()
        node_names = self.state.node_names
        node_coordinates = self.state.node_coordinates

        nx.draw(self.G, pos=node_coordinates, nodelist=empty_nodes, node_color=Color.LIGHT_BLUE.value, node_size=800)
        nx.draw(self.G, pos=node_coordinates, nodelist=occupied_nodes, node_color=Color.DARK_BLUE.value, node_size=800, ax=self.ax, labels=node_names, font_color=Color.WHITE.value)

        if self.history:
            nx.draw(self.G, pos=node_coordinates, nodelist=[self.state.start_pos], node_color=Color.RED.value, node_size=1200)
            nx.draw(self.G, pos=node_coordinates, nodelist=[self.state.start_pos], node_color=Color.LIGHT_BLUE.value, node_size=800)
            nx.draw(self.G, pos=node_coordinates, nodelist=[self.state.end_pos], node_color=Color.RED.value, node_size=1200)
            nx.draw(self.G, pos=node_coordinates, nodelist=[self.state.end_pos], node_color=Color.DARK_BLUE.value, node_size=800)

        """ self.ax.set_axis_on()
        self.ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
        plt.title('Peg Solitaire') """

        self.fig.tight_layout()
        plt.show(block=block)
        self.fig.patch.set_facecolor(Color.WHITE.value)
        plt.pause(0.1)

        if delay:
            plt.pause(delay)
