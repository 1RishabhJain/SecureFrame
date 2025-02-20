import json
import subprocess

def write_metadata(file_path, selected_ids, tracked_data, method):
    """
    Writes metadata (IV, selected IDs, and tracking data) directly into an MP4 file using ExifTool.
    """
    metadata = {
        "method": method, 
        "selected_ids": selected_ids
    }
    
    metadata_json = json.dumps(metadata)

    # Use ExifTool to embed metadata
    command = [
        "exiftool",
        f"-Description={metadata_json}",
        "-overwrite_original",
        file_path
    ]
    
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    if result.returncode == 0:
        print(f"Metadata successfully written to {file_path}")
    else:
        print(f"Error writing metadata: {result.stderr}")

def read_metadata(file_path):
    """
    Extracts encryption metadata (IV, selected object IDs, and tracking data) from the media file.
    """

    # Use ExifTool to extract metadata from the Description field
    command = ["exiftool", "-Description", "-json", file_path]
    
    # Run the ExifTool command
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    if result.returncode == 0:
        try:
            # Parse the JSON response from ExifTool
            exif_data = json.loads(result.stdout)
            metadata_json = exif_data[0].get("Description", None)

            if metadata_json:
                # Parse and process the metadata
                metadata = json.loads(metadata_json)
                print(f"Metadata successfully extracted from {file_path}")
                return metadata
            else:
                raise ValueError("No metadata found in the 'Description' field.")
        except Exception as e:
            raise ValueError(f"Error parsing metadata: {e}")
    else:
        # Handle ExifTool errors
        raise ValueError(f"Error reading metadata: {result.stderr}")
