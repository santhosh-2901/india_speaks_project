import pandas as pd
import yaml
import logging
from tqdm import tqdm
from pathlib import Path
from typing import Dict, Any

from .validation import validate_row
from .text_normalizer import normalize_text

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataCleaner:
    """
    A class to orchestrate the cleaning and validation of the India Speaks dataset.
    """
    def __init__(self, config_path: str):
        """
        Initializes the DataCleaner with a configuration file.

        Args:
            config_path (str): Path to the YAML configuration file.
        """
        self.config = self._load_config(config_path)
        logging.info("DataCleaner initialized with configuration.")

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Loads the YAML configuration file."""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    def process_csv(self, input_csv: str, output_dir: str):
        """
        Processes the input CSV file, separates clean and rejected rows,
        and saves them to the specified output directory.

        Args:
            input_csv (str): Path to the input metadata CSV.
            output_dir (str): Path to the directory for saving output files.
        """
        try:
            df = pd.read_csv(input_csv)
            logging.info(f"Successfully loaded {input_csv} with {len(df)} rows.")
        except FileNotFoundError:
            logging.error(f"Input file not found at {input_csv}")
            return

        clean_rows = []
        rejected_rows = []

        # Use tqdm for a progress bar
        for _, row in tqdm(df.iterrows(), total=len(df), desc="Processing rows"):
            row_dict = row.to_dict()
            is_valid, reason = validate_row(row_dict, self.config)

            if is_valid:
                # Normalize transcription if the row is valid
                normalized_transcript = normalize_text(
                    row_dict['transcription_raw'],
                    row_dict.get('language', ''),
                    self.config
                )
                
                # Check if normalization resulted in an empty string
                if not normalized_transcript:
                    row_dict['rejection_reason'] = "EMPTY_AFTER_NORMALIZATION"
                    rejected_rows.append(row_dict)
                else:
                    row_dict['transcription_normalized'] = normalized_transcript
                    clean_rows.append(row_dict)
            else:
                row_dict['rejection_reason'] = reason
                rejected_rows.append(row_dict)

        # Create DataFrames from the lists of dictionaries
        train_ready_df = pd.DataFrame(clean_rows)
        rejected_df = pd.DataFrame(rejected_rows)
        
        # Ensure 'transcription_normalized' is the last column in the clean set
        if 'transcription_normalized' in train_ready_df.columns:
            cols = [c for c in train_ready_df.columns if c != 'transcription_normalized'] + ['transcription_normalized']
            train_ready_df = train_ready_df[cols]


        # Create output directory if it doesn't exist
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        train_ready_path = Path(output_dir) / 'train_ready.csv'
        rejected_path = Path(output_dir) / 'rejected.csv'

        train_ready_df.to_csv(train_ready_path, index=False)
        rejected_df.to_csv(rejected_path, index=False)

        logging.info(f"Processing complete.")
        logging.info(f"{len(train_ready_df)} rows saved to {train_ready_path}")
        logging.info(f"{len(rejected_df)} rows saved to {rejected_path}")