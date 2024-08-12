from autoe2e.crawler.config.driver_config import DriverConfig
from autoe2e.crawler.config.lifecycle_config import LifecycleConfig


class Config(
    DriverConfig,
    LifecycleConfig
):
    def __init__(self):
        super().__init__()
        
        self.temp_dir = None
    
    
    @staticmethod
    def from_dict(config: dict):
        config_obj: Config = Config()
        config_obj.temp_dir = config.get('temp_dir', '/tmp')
        if 'driver' in config:
            config_obj.driver_config_from_dict(config['driver'])
        if 'lifecycle' in config:
            config_obj.lifecycle_config_from_dict(config['lifecycle'])
        return config_obj