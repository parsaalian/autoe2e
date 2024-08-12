class LifecycleConfig:
    def __init__(self):
        self.on_visit = []
        self.on_state_discovery = []
    
    
    def set_on_visit(self, on_visit: list):
        self.on_visit = on_visit
    
    
    def set_on_state_discovery(self, on_state_discovery: list):
        self.on_state_discovery = on_state_discovery
    
    
    def lifecycle_config_from_dict(self, config: dict):
        if 'on_visit' in config:
            self.set_on_visit(config['on_visit'])
        if 'on_state_discovery' in config:
            self.set_on_state_discovery(config['on_state_discovery'])
