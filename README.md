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

## Developer notes

### The rationale for the technologies I have decided to use
Python is selected for its extensive ecosystem of data processing libraries and its "developer-first" syntax. Python allows for high-level abstractions of complex file-parsing logic, suitable for rapid prototyping to build Minimum Viable Products
but still can meet business requirements.

### What would I have done differently if I had more time

Add Validation Layer that catches bad rows without stopping the whole process. The current logic raise error if it reads bad rows and stop the process.

Get higher test coverage reduces the risk of "regressions" and ensures the system handles edge cases gracefully.

Mock specific providers to test how the core logic handles different edge cases like connection timeouts or "Disk Full" errors.

Create a full End-to-end Integration Test.

Optimize performance for Batching and Async, use Multiprocessing to handle large files and AsyncIO for faster database writes, increasing overall throughput.

Perform benchmark testing that measures throughput metrics, resource profiling and database batch size optimization.

### The rationale for the design choices that I have made

#### Hexagonal Architecture
Separate core business logic (parsing NEM12 rules)from external dependencies like the File System or the PostgreSQL database. Clear interface for Reader, Parser and Writer.
This makes the system future-proof. If the data source or storage changes, we just need to make new adapters.

#### Strategic Data Batching
Writing to a database row-by-row is slow due to the network overhead of thousands of individual transactions. Batching helps significantly reduces database overhead and increases the overall throughput of the pipeline.

#### Dependency Injection
The system injects necessary providers at runtime instead of hardcoding configurations.
Testing and development is simplified. Mock providers can be injected during development and real providers for production environment.
