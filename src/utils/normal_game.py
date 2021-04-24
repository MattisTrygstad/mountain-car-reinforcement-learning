import ast

from matplotlib import pyplot as plt
from environment.hexagonal_grid import HexagonalGrid
from environment.universal_action import UniversalAction
from utils.config_parser import Config


def normal_game():
    env = HexagonalGrid(Config.win_multiplier)

    env.visualize(False)

    while True:
        # Check win condition
        if env.check_win_condition():
            print('Congratulations, you won!')
            break

        legal_actions = env.get_legal_actions()

        print('-----\nLegal moves:')
        for action in legal_actions:
            print(f'From: {action[0]}, To: {action[1]}')
        print('-----')

        first_input = input('Enter start node: ')
        if first_input == 'q':
            break

        if first_input == 'undo':
            print('Action reversed')
            env.undo_action()
            env.visualize(False)
            continue

        try:
            start_node = tuple(ast.literal_eval(first_input))
            end_node = tuple(ast.literal_eval(input('Enter end node: ')))
        except:
            print('Invalid input, try again!')
            continue

        if (start_node, end_node) not in legal_actions:
            print('Illegal move, try again!')
            continue

        action = UniversalAction()
        action.action = (start_node, end_node)
        env.execute_action(action)
        env.visualize(False)

    plt.close()
