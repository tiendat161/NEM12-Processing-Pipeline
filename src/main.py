import argparse
from .spec import BaseRunSpec

RECORDS = 'records'

def parse_data(run_spec, batch, **kwargs):
    parser = run_spec.parser_provider
    batch["output"] = {}
    batch["output"][RECORDS] = parser.parse_nmi_batch(batch, **kwargs)
    return dict(run_spec=run_spec, batch=batch, **kwargs)

def write_data(run_spec, batch, **kwargs):
    writer = run_spec.writer_provider
    writer.write(batch["output"].get(RECORDS, []))
    return dict(run_spec=run_spec, batch=batch, **kwargs)

class RunSpec(BaseRunSpec):
    strategy = [
        parse_data,
        write_data,
    ]
    providers = {
        'EVENT_PROVIDER',
        'PARSER_PROVIDER',
        'WRITER_PROVIDER',
    }

def do_run(args):
    return RunSpec(env=args.env, run_mode=args.mode, file_name=args.file_name, batch_size=args.batch_size)

def main():
    parser = argparse.ArgumentParser(description="NEM12 Pipeline Runner")
    parser.add_argument('--env', type=str, default='dev', help='Environment (dev, prod)')
    parser.add_argument('--mode', type=str, default='all', help='Run mode (all, once)')
    parser.add_argument('--file_name', type=str, default='sample_nem12.csv', help='Name of the input NEM12 file')
    parser.add_argument('--batch_size', type=int, default=2, help='Batch size for processing')
    args = parser.parse_args()
    do_run(args).run()

if __name__ == "__main__":
    main()
