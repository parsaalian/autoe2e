from oraclai.core.state.state_graph import StateGraph
from oraclai.core.state.state import State
from oraclai.core.action import Action


class StateMachine:
    def __init__(self):
        self.current_state: State | None = None
        self.visible_state: State | None = None
        self.state_graph: StateGraph[State, Action] = StateGraph()
        self.visited_states = {}
    
    
    def reset(self):
        self.current_state = None
        self.visible_state = None
        self.state_graph.reset()
        self.visited_states.clear()
    
    
    def set_initial_state(self, state: State) -> None:
        self.state_graph.set_initial_state(state)
        self.current_state = state
    
    
    def get_current_state(self) -> State:
        if self.current_state is None:
            raise ValueError('current state is None')
        return self.current_state
    
    
    def set_current_state(self, state: State) -> None:
        self.current_state = state
    
    
    def reset_current_state(self) -> None:
        self.current_state = self.state_graph.get_initial_state()
    
    
    def set_visible_state(self, state: State) -> None:
        self.visible_state = state
    
    
    def add_state_from_current_state(self, state: State, action: Action) -> None:
        if self.current_state is None:
            self.current_state = state
        else:
            state.set_crawl_path(
                self.current_state.get_crawl_path().extend_path(
                    self.current_state, action
                )
            )
        
        self.state_graph.add_state(state)
        self.state_graph.add_action(action, self.current_state, state)
    
    
    def go_to_state(self, state: State) -> None:
        if self.current_state is None:
            raise ValueError('current state is None')
        if not self.state_graph.can_go_to_state(self.current_state, state):
            raise ValueError('cannot go to state')
        self.current_state = state
