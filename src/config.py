from .core.Reader import NEM12FileHandler
from .core.Parser import NEM12DataParser
from .core.Writer import LocalFileWriter, PostgresWriter

class Config:
    def get_config(env):
        if env == "prod":
            return ProdConfig()
        elif env == "dev":
            return DevConfig()
        else:
            raise ValueError(f"Unknown environment: {env}")


class BaseConfig:
    EVENT_PROVIDER = NotImplemented
    PARSER_PROVIDER = NotImplemented
    WRITER_PROVIDER = NotImplemented
    TABLE_NAME = "meter_readings"
    BATCH_SIZE = 2

    def get(cls, key, default=None):
        return getattr(cls, key.upper(), default)


class ProdConfig(BaseConfig):
    EVENT_PROVIDER = NEM12FileHandler
    PARSER_PROVIDER = NEM12DataParser
    WRITER_PROVIDER = PostgresWriter


class DevConfig(BaseConfig):
    EVENT_PROVIDER = NEM12FileHandler
    PARSER_PROVIDER = NEM12DataParser
    WRITER_PROVIDER = LocalFileWriter
    BASE_PATH = './data/raw/'
    FILE_NAME = '/sample_nem12.csv'
    OUTPUT_FILE_PATH = './data/processed/log.txt'
    BATCH_SIZE = 10000
