import datetime
from src.lib.schema import RecordSchema

class NEM12DataParser:
    def __init__(self, config, **kwargs):
        self.config = config

    def parse_nmi_batch(self, batch, **kwargs):
        records = []
        for row in batch["input"][0]:
            record_type = row[0]
            if record_type == '100':  # Header blocks
                continue

            elif record_type == '200':  # NMI Details
                nmi_id = row[1]
                interval_length = int(row[8])
                no_intervals = 24 * 60 // interval_length

            elif record_type == '300':  # Interval Data
                read_date = row[1]
                intervals = row[2:no_intervals+2]
                start_dt = datetime.datetime.strptime(read_date, "%Y%m%d")
                for i, value in enumerate(intervals):
                    reading_ts = start_dt + datetime.timedelta(minutes=interval_length * i)
                    value = float(value) if value else 0.0
                    records.append(RecordSchema(
                        nmi=nmi_id,
                        timestamp=reading_ts,
                        consumption=value
                    ))
        return records
