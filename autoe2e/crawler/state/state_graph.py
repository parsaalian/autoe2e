from typing import Generic, TypeVar


S = TypeVar('S')
A = TypeVar('A')


class StateGraph(Generic[S, A]):
    def __init__(self):
        self.initial_state: S | None = None
        self.states: dict[str, S] = {}
        self.adjacency_list: dict[str, dict[A, str]] = {}
        self.transpose_adjacency_list: dict[str, dict[A, str]] = {}
    
    
    def reset(self) -> None:
        '''
        Resets the state graph by removing all states and actions.
        '''
        self.initial_state = None
        self.states.clear()
        self.adjacency_list.clear()
        self.transpose_adjacency_list.clear()
    
    
    def get_initial_state(self) -> S:
        '''
        Returns the initial state of the state graph.
        '''
        if self.initial_state is None:
            raise ValueError('initial state is not set')
        return self.initial_state
    
    
    def set_initial_state(self, state: S) -> None:
        '''
        Sets the initial state of the state graph.
        '''
        self.initial_state = state
        self.states[state.get_id()] = state
    
    
    def get_state(self, state_id: str) -> S | None:
        '''
        Returns the state with the given id.
        '''
        return self.states.get(state_id, None)
    
    
    def get_outgoing_actions(self, state: S) -> list[A]:
        '''
        Returns the actions that can be taken from the given state.
        '''
        return list(self.adjacency_list.get(state.get_id(), {}).keys())
    
    
    def get_incoming_actions(self, state: S) -> list[A]:
        '''
        Returns the actions that can be taken to reach the given state.
        '''
        return list(self.transpose_adjacency_list.get(state.get_id(), {}).keys())
    
    
    def get_state_connected_with_action(self, state: S, action: A) -> S | None:
        '''
        Returns the state that can be reached from the given state with the given action.
        '''
        target_state_id = self.adjacency_list.get(state.get_id(), {}).get(action, None)
        if target_state_id is not None:
            return self.states[target_state_id]
        return None
    
    
    def get_connected_states(self, state: S) -> list[S | None]:
        '''
        Returns the states that are connected to the given state.
        '''
        connections = [
            self.states.get(state_id, None) for state_id in self.adjacency_list.get(state.get_id(), {}).values()
        ]
        return list(filter(lambda x: x is not None, connections))
    
    
    def can_go_to_state(self, source_state: S, target_state: S) -> bool:
        '''
        Returns True if there is an edge from the source to the target state.
        '''
        return target_state.get_id() in self.adjacency_list.get(source_state.get_id(), {}).values()
    
    
    def add_state(self, state: S) -> None:
        '''
        Adds a state to the state graph if not already there.
        '''
        if self.initial_state is None:
            self.initial_state = state
        
        if state.get_id() not in self.states:
            self.states[state.get_id()] = state
    
    
    def add_action(self, action: A, source_state: S, target_state: S) -> None:
        '''
        Adds an action to the state graph if not already there.
        '''
        if source_state.get_id() not in self.adjacency_list:
            self.adjacency_list[source_state.get_id()] = {}
        if action not in self.adjacency_list[source_state.get_id()]:
            self.adjacency_list[source_state.get_id()][action] = target_state.get_id()
        
        if target_state.get_id() not in self.transpose_adjacency_list:
            self.transpose_adjacency_list[target_state.get_id()] = {}
        if action not in self.transpose_adjacency_list[target_state.get_id()]:
            self.transpose_adjacency_list[target_state.get_id()][action] = source_state.get_id()
    
    
    def get_shortest_path(self, source_state: S, target_state: S) -> list[A]:
        # TODO: implement Dijkstra's algorithm
        '''
        Returns the shortest path between the source and target states.
        '''
