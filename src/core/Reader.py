import csv
from ..lib.common import logger
from typing import Generator, List

def get_cleaned_rows(file_path):
    """
    Reads a file and joins broken lines that don't start with 
    valid NEM12 record indicators.
    """
    valid_starts = ('100', '200', '300', '400', '500', '900')
    
    with open(file_path, 'r') as f:
        buffer = ""
        for line in f:
            clean_line = line.strip()
            if not clean_line:
                continue

            if clean_line.startswith(valid_starts):
                if buffer:
                    yield list(csv.reader([buffer]))[0]
                buffer = clean_line
            else:
                buffer += clean_line
        
        if buffer:
            yield list(csv.reader([buffer]))[0]

class NEM12FileHandler:
    """
    An adapter that handles reading the physical NEM12 file from disk.
    It yields chunks of data grouped by NMI to keep memory usage low.
    """
    def __init__(self, config):
        self.file_path = config.get('BASE_PATH', './data/raw/') + config.get('FILE_NAME', 'sample_nem12.csv')
        print(f"Initialized NEM12FileHandler with file path: {self.file_path}")
        self.batch_size = config.get('BATCH_SIZE', 1)

    def next_batch(self) -> Generator[List[str], None, None]:
        batch = {"input": []}
        current_nmi_block = []
        nmi_count = 0

        for row in get_cleaned_rows(self.file_path):
            if row[0] == '200':
                if current_nmi_block:
                    batch["input"].append(current_nmi_block)
                    nmi_count += 1
                
                if nmi_count >= self.batch_size:
                    logger.info(f"Reading {len(batch['input'])} NMI blocks.") 
                    yield batch
                    batch = {"input": []}
                    nmi_count = 0
                
                current_nmi_block = []

            # Skip header/footer but keep data records
            if row[0] in ('200', '300', '400', '500'):
                current_nmi_block.append(row)

        if current_nmi_block:
            batch["input"].append(current_nmi_block)
            logger.info(f"Reading {len(batch['input'])} NMI blocks.") 
            yield batch
