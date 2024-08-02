import unittest

from oraclai.core.state import State, StateGraph


class TestStateGraph(unittest.TestCase):
    '''
    Test suite for the StateGraph class.
    '''
    
    def test_get_empty_initial_state(self):
        '''
        If the initial state is not set, then a ValueError should be raised.
        '''
        state_graph = StateGraph()
        with self.assertRaises(ValueError):
            state_graph.get_initial_state()
    
    
    def test_set_initial_state(self):
        '''
        Tests directly setting the initial state of the state graph, and then retrieving it.
        '''
        state_graph = StateGraph()
        state1 = State('http://example.com', '<html></html>')
        state_graph.set_initial_state(state1)
        self.assertEqual(state1, state_graph.get_initial_state())
    
    
    def test_add_first_state_as_initial_state(self):
        '''
        If add a state before setting the initial state,
        then the state should be set as the initial state.
        '''
        state_graph = StateGraph()
        state1 = State('http://example.com', '<html></html>')
        state_graph.add_state(state1)
        self.assertEqual(state1, state_graph.get_initial_state())
    
    
    def test_add_state(self):
        '''
        Tests adding a state to the state graph.
        '''
        state_graph = StateGraph()
        state1 = State('http://example.com', '<html></html>')
        state_graph.add_state(state1)
        self.assertIn(state1, state_graph.states.values())
    
    
    def test_get_state(self):
        '''
        Tests getting a state to the state graph.
        '''
        state_graph = StateGraph()
        state1 = State('http://example.com', '<html></html>')
        state_graph.add_state(state1)
        self.assertEqual(state1, state_graph.get_state(state1.get_id()))
    
    
    def test_add_action(self):
        '''
        Tests add an action to the state graph.
        '''
    
    
    def test_get_incoming_action_from_non_existent_state(self):
        '''
        If the state does not exist, then an empty list should be returned.
        '''
    
    
    def test_get_incoming_action_from_state(self):
        '''
        Tests getting the incoming actions to a state.
        '''
    
    
    def test_get_outgoing_action_from_non_existent_state(self):
        '''
        If the state does not exist, then an empty list should be returned.
        '''
    
    
    def test_get_outgoing_action_from_state(self):
        '''
        Tests getting the outgoing actions from a state.
        '''
    
    
    def test_get_connected_states_from_non_existent_state(self):
        '''
        If the state does not exist, then an empty list should be returned.
        '''
    
    
    def test_get_connected_states_from_state(self):
        '''
        Tests getting the connected states from a state.
        '''
    
    
    def test_can_go_to_state(self):
        '''
        Tests checking if it is possible to go from one state to another.
        '''
    
    
    def test_merge_states_if_target_state_does_not_exist(self):
        '''
        If the target state does not exist, no changes should be made.
        '''
    
    
    def test_merge_states(self):
        '''
        Tests merging two states.
        '''
    
    
    def test_update_id(self):
        '''
        Tests updating the id of a state.
        '''


if __name__ == '__main__':
    unittest.main()