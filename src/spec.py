import time
from .lib.common import logger
from .config import Config

class BaseRunSpec:
    strategy = ()
    providers = ()

    def __init__(self, **kwargs):
        self.run_mode = kwargs.get('run_mode')
        self.env = kwargs.get('env')
        self.config = self.get_config(self.env)
        self._update_config_from_kwargs(kwargs)
        self._set_providers()
        

    @classmethod
    def get_config(cls, env):
        return Config.get_config(env)

    def _set_providers(self):
        for name in self.providers:
            lcname = name.lower()
            if hasattr(self, lcname) and getattr(self, lcname) is not None:
                continue
            provider_class = self.config.get(name)
            provider_instance = provider_class(self.config)
            setattr(self, lcname, provider_instance)
            

    def _update_config_from_kwargs(self, kwargs):
        for key, value in kwargs.items():
            if value is not None:
                setattr(self.config, key.upper(), value)

    def next_batch(self):
        return self.event_provider.next_batch()
    
    def run(self):
        _run(self, self.run_mode)

def _run(run_spec, mode):
    for batch in run_spec.next_batch():
        if batch:
            try:
                execute_strategy(run_spec, batch)
                if mode == "once":
                    logger.info("Run mode is 'once'. Stopping after first batch.")
                    return
            except Exception as e:
                logger.error(f"Error processing batch: {e}", exc_info=True)
        else:
            empty_runs += 1
            logger.info(f"Empty batch: {empty_runs}, sleep for 1 seconds.")
            time.sleep(1)

def execute_strategy(run_spec, batch):
    for fn in run_spec.strategy:
        logger.info(f"Running step: {fn.__name__}")
        fn(run_spec=run_spec, batch=batch)
    logger.info("Finished Strategy.")