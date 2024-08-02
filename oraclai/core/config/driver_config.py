class DriverConfig:
    def __init__(self):
        self.base_url: str | None = None
    
    
    def set_base_url(self, url: str):
        self.base_url = url
    
    
    def driver_config_from_dict(self, config: dict):
        if 'base_url' in config:
            self.set_base_url(config['base_url'])