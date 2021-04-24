from abc import ABC, abstractmethod
from environment.universal_action import UniversalAction

from environment.universal_state import UniversalState


class Environment(ABC):
    """
    Abstract class to be implemented by each environment
    """

    @abstractmethod
    def execute_action(self, action: UniversalAction) -> None:
        pass

    @abstractmethod
    def check_win_condition(self) -> bool:
        pass

    @abstractmethod
    def get_state(self) -> UniversalState:
        pass

    @abstractmethod
    def reset(self) -> None:
        pass

    @abstractmethod
    def visualize(self) -> None:
        pass
