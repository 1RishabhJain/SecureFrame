import json
import subprocess

import os
import json
import subprocess
import tempfile

def write_metadata(file_path, selected_ids, tracked_data, method):
    """
    Write metadata (in JSON form) to a local file called 'metadata.json'.
    Will be updated to write metadata directly to file
    """
    try:
        metadata = {
            "method": method, 
            "selected_ids": selected_ids,
            "tracked_objects": tracked_data
        }
        
        # Dump the metadata dictionary directly as JSON
        with open("output/metadata.json", 'w', encoding="utf-8") as json_file:
            json.dump(metadata, json_file, indent=4)
            
        print("Metadata successfully written to metadata.json")
    
    except Exception as e:
        print(f"Error writing metadata: {e}")


def read_metadata(file_path):
    """
    Reads the metadata from the local 'metadata.json' file.
    Will be updated to read metadata directly from file
    """
    try:
        with open("output/metadata.json", "r", encoding="utf-8") as metadata_file:
            data = json.load(metadata_file)
            print("Metadata successfully read from metadata.json")
            return data
    except FileNotFoundError:
        print("metadata.json not found.")
        return None
    except json.JSONDecodeError:
        print("Failed to decode metadata.json as valid JSON.")
        return None
    except Exception as e:
        print(f"Error reading metadata: {e}")
        return None
