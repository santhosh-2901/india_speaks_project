India Speaks Data Preprocessing Pipeline
This repository contains india_speaks_cleaner, a Python package designed to validate and preprocess multilingual audio-text data for ASR/TTS model training at India Speaks.

The pipeline takes a raw metadata CSV as input, validates each entry against a set of rules based on the official IndiaSpeaks_Data_Standards.pdf, normalizes the transcriptions according to language-specific standards, and outputs two files: train_ready.csv for clean data and rejected.csv for problematic data.

Features
End-to-End Processing: A single command processes the entire metadata file.

Modular Design: Logic is separated into validation, text normalization, and core processing modules for easy maintenance and extension.

Configurable: Pipeline parameters (e.g., max duration, allowed punctuation) are managed via a config.yaml file.

Language-Specific Normalization: Implements normalization rules for multiple Indic languages as specified in the India Speaks Data Standards.

Robust Validation: Checks for missing transcriptions, invalid audio paths, excessive duration, and low-quality flags.

Audio File Simulation: Includes stubs to simulate audio file validation (e.g., corruption checks) without requiring actual file access.

Comprehensive Logging: Logs progress and errors for better monitoring during execution.

Project Structure
india_speaks_project/
├── india_speaks_cleaner/
│   ├── __init__.py
│   ├── main.py
│   ├── cleaner.py
│   ├── text_normalizer.py
│   ├── validation.py
│   └── config.yaml
├── tests/
│   └── test_text_normalizer.py
├── README.md
└── requirements.txt

Setup
Clone the repository:

git clone <your-repo-url>
cd india_speaks_project

Create a virtual environment (recommended):

python3 -m venv venv
source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Usage
The script is run from the command line. Place your input CSV (utterances_metadata.csv) in the root directory or provide a full path to it.

python -m india_speaks_cleaner.main \
    --input-csv utterances_metadata.csv \
    --output-dir ./output

Arguments:
--input-csv: Path to the input metadata CSV file.

--output-dir: Directory to save the train_ready.csv and rejected.csv files.

--config-path: (Optional) Path to a custom YAML configuration file. Defaults to india_speaks_cleaner/config.yaml.

After running, the output directory will contain the processed files.

Testing
To ensure the text normalization logic is working correctly, you can run the included unit tests. From the root directory of the project, run:

python -m unittest tests/test_text_normalizer.py

This will verify that the text cleaning functions are behaving as expected.
