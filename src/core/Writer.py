import psycopg
from ..lib.common import logger

class BaseAdapter:
    def __init__(self, config):
        self.config = config
        self.table_name = config.get('table_name', None)
        self.sql_template = self._init_template()

    def _init_template(self):
        SQL_TEMPLATE = f"""
INSERT INTO {self.table_name} (nmi, "timestamp", consumption)
VALUES
 {{values}}
ON CONFLICT ("nmi", "timestamp")
DO UPDATE SET consumption = EXCLUDED.consumption;
""".strip()
        return SQL_TEMPLATE
    
    def build_query(self, records):
        value_strings = []
        for e in records:
            value_strings.append(f"('{e.nmi}', '{e.timestamp}', {e.consumption})")

        all_values = ",\n ".join(value_strings)
        return self.sql_template.format(values=all_values)
    
    def generate_queries(self, records, limit=1000):
        if not records:
            return []
        queries = []
        for i in range(0, len(records), limit):
            batch = records[i : i + limit]
            query = self.build_query(batch)
            queries.append(query)
        return queries


class PostgresWriter(BaseAdapter):
    def __init__(self, config, **kwargs):
        super().__init__(config)
        self.connection = None
        self.cursor = None


    def write(self, records):
        self.ensure_connected()
        queries = self.generate_queries(records)
        for query in queries:
            try:
                self.cursor.execute(query)
                self.connection.commit()
            except Exception as e:
                self.connection.rollback()
                return None

    def connect(self):
        try:
            self.connection = psycopg.connect(self.config.db)
        except psycopg.OperationalError as e:
            logger.info(f"Connection to PostgreSQL server failed: {e}")
            self.connection = None

    def ensure_connected(self):
        if self.connection is None or self.connection.closed:
            self.connect()


class LocalFileWriter(BaseAdapter):
    def __init__(self, config):
        super().__init__(config)
        self.output_file_path = config.get('output_file_path')

    def write(self, records):
        with open(self.output_file_path, 'a') as f:
            queries = self.generate_queries(records)
            for query in queries:
                f.write(query + "\n")

