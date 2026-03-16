# NEM12 Processing Pipeline

A professional-grade Python engine designed to parse, clean, and batch-process Australian National Electricity Market (NEM12) interval metering data. This system is optimized for high-scale performance, handling datasets with millions of records while maintaining a low memory footprint.

## 📁 Project Structure

```text
nem12_project/
├── devtools/                # Local development & debugging tools
├── src/
│   ├── main.py              # Entry point
│   ├── core/                # Engine logic
│   │   ├── Parser.py        # NEM12 cleaning & stitching
│   │   ├── Reader.py        # File stream, batch & generator logic
│   │   └── Writer.py        # Output & SQL generation
│   └── lib/                 # Shared resources
│       ├── common.py        # Utility helpers
│       └── schema.py        # Data model
├── tests/                   # Automated unittests
│   └── test_parser.py
├── .gitignore               
├── requirements.txt         
└── README.md
```

## Running & Operations Guide

### Prerequisite
Ensure you are using Python 3.8+ and set up your virtual environ

### Running the Pipeline


**Process a NEM12 sample file:**
```bash
python3 -m src.main
```

**Run development tool - NEM12 file generator with 1 million records:**
```bash
python3 -m devtools.generate_nem12_file
```
Sample output:
```bash
File successfully generated at: data/raw/20260317035813_mock_meter_data.csv
```

Copy the generated file name and run:

```bash
python3 -m src.main --file_name='{your_file_name}' --batch_size=10000
```

**Run unittest:**
```bash
python3 -m unittest discover tests   
```