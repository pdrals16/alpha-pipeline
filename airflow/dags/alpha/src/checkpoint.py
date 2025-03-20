import os
import json
import glob
import logging
from datetime import datetime


def update_checkpoint(file_path, checkpoint_file='.checkpoint'):
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'r') as f:
            checkpoint_data = json.load(f)
    else:
        checkpoint_data = {}

    checkpoint_data[file_path] = {
        'processed_at': datetime.now().isoformat(),
        'file_size': os.path.getsize(file_path),
        'file_mtime': os.path.getmtime(file_path)
    }

    with open(checkpoint_file, 'w') as f:
        f.write(json.dumps(checkpoint_data, indent=4))

def get_files_to_process(directory, file_pattern='*.csv', checkpoint_file='.checkpoint'):
    all_files = glob.glob(os.path.join(directory, file_pattern))

    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'r') as f:
            checkpoint_data = json.load(f)
    else:
        checkpoint_data = {}

    files_to_process = []
    for file_path in all_files:
        if file_path not in checkpoint_data:
            files_to_process.append(file_path)
            continue
    
    return files_to_process