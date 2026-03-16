import random
import os
from pathlib import Path
from datetime import datetime, timedelta

BASE_DIR = Path("data/raw")

def generate_nem12_sample(filename, nmi_count=2, days_count=4, interval_length=30):
    # 1. Define and Create the DEFAULT output path
    output_dir = BASE_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = output_dir / filename
    
    lines = []
    now_str = datetime.now().strftime("%Y%m%d%H%M")
    update_str = datetime.now().strftime("%Y%m%d%H%M%S")

    # 100 Record: Header
    lines.append(f"100,NEM12,{now_str},UNITEDDP,NEMMCO")

    for i in range(nmi_count):
        nmi = f"NEM12{random.randint(1, 99999):05d}"
        # 200 Record: NMI Details
        lines.append(f"200,{nmi},E1E2,1,E1,N1,01009,kWh,{interval_length},20050610")

        start_date = datetime(2025, 3, 1)
        for d in range(days_count):
            current_date = (start_date + timedelta(days=d)).strftime("%Y%m%d")
            
            no_intervals = 24 * 60 // interval_length
            intervals = [f"{random.uniform(0.1, 1.5):.3f}" for _ in range(no_intervals)]
            intervals_str = ",".join(intervals)
            
            # 300 Record: Interval Data
            line_300 = f"300,{current_date},{intervals_str},A,,,{update_str},{update_str}"
            lines.append(line_300)

        lines.append(f"500,O,S01009,{update_str},") # 500 Record (End of NMI Data)
    
    lines.append("900") # 900 Record (End of File)

    # 2. Write to the specific path
    try:
        with open(file_path, "w") as f:
            f.write("\n".join(lines))
        print(f"File successfully generated at: {file_path}")
    except Exception as e:
        print(f"Failed to write file: {e}")

if __name__ == "__main__":
    timenow = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{timenow}_mock_meter_data.csv"
    generate_nem12_sample(filename, nmi_count=100000, days_count=5, interval_length=30)