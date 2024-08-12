from autoe2e.crawler.action import Action


class CrawlPath:
    def __init__(self, state_path: list | None = None, action_path: list[Action] | None = None):
        self.action_path: list = list(action_path) if action_path is not None else []
        self.state_path: list = list(state_path) if state_path is not None else []
    
    
    # not using 'State' as a type due to circular import
    def extend_path(self, state, action: Action) -> 'CrawlPath':
        new_path: CrawlPath = CrawlPath(self.state_path + [state], self.action_path + [action])
        return new_path

    
    def __len__(self) -> int:
        return len(self.action_path)
    
    
    def get_actions(self) -> list[Action]:
        return self.action_path

    
    def get_states(self) -> list:
        return self.state_path
    
    
    def get_action(self, index: int) -> Action:
        return self.action_path[index]
    
    
    def get_state(self, index: int):
        return self.state_path[index]
