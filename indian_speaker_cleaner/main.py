import argparse
from pathlib import Path
from .cleaner import DataCleaner

def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="India Speaks Data Preprocessing Pipeline.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "--input-csv",
        type=str,
        required=True,
        help="Path to the input metadata CSV file."
    )
    
    parser.add_argument(
        "--output-dir",
        type=str,
        required=True,
        help="Directory to save the train_ready.csv and rejected.csv files."
    )
    
    default_config_path = Path(__file__).parent / "config.yaml"
    parser.add_argument(
        "--config-path",
        type=str,
        default=str(default_config_path),
        help="Path to the pipeline's YAML configuration file."
    )

    args = parser.parse_args()

    # Initialize and run the cleaner
    cleaner = DataCleaner(config_path=args.config_path)
    cleaner.process_csv(input_csv=args.input_csv, output_dir=args.output_dir)

if __name__ == "__main__":
    main()