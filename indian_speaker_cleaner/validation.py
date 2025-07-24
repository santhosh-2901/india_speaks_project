import numpy as np
from typing import Dict, Any, Tuple, Optional

def validate_row(row: Dict[str, Any], config: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """
    Validates a single row from the metadata DataFrame.

    Args:
        row (Dict[str, Any]): A dictionary representing a row.
        config (Dict[str, Any]): The configuration dictionary.

    Returns:
        Tuple[bool, Optional[str]]: A tuple containing a boolean (True if valid)
                                    and a rejection reason string if invalid.
    """
    # 1. Check for missing or empty transcription
    if not row.get('transcription_raw') or not str(row['transcription_raw']).strip():
        return False, "MISSING_TRANSCRIPTION"

    # 2. Validate audio path format
    path = row.get('audio_path', '')
    if not path.startswith(config['validation_params']['audio_path_prefix']):
        return False, "INVALID_AUDIO_PATH"

    # 3. Check duration constraints
    duration = float(row.get('duration_sec', 0.0))
    max_dur = config['validation_params']['max_duration_sec']
    min_dur = config['validation_params']['min_duration_sec']
    if not (min_dur <= duration <= max_dur):
        return False, f"DURATION_OUT_OF_RANGE ({duration:.2f}s)"

    # 4. Check the quality flag from crowd workers/internal tools
    # We reject files explicitly marked as failed (0)
    if row.get('quality_flag') == 0:
        return False, "LOW_QUALITY_FLAG"

    # 5. Simulate checking for corrupted audio files
    failure_rate = config['simulation_params']['corruption_failure_rate']
    if np.random.rand() < failure_rate:
        return False, "AUDIO_CORRUPT_SIMULATED"
        
    return True, None