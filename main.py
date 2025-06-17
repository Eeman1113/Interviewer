from pydub import AudioSegment
import json
import os

def extract_questions_to_audio(audio_path, json_data, output_dir="./questions"):
    """
    Extracts individual questions from an audio file based on timestamps
    and saves them as separate audio files.

    Args:
        audio_path (str): Path to the input audio file.
        json_data (list): A list of dictionaries containing 'start', 'end', and 'text'
                          for each question.
        output_dir (str): Directory to save the extracted question audio files.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    try:
        audio = AudioSegment.from_mp3(audio_path)
    except Exception as e:
        print(f"Error loading audio file from {audio_path}: {e}")
        print("Please ensure the audio file exists and is a valid MP3.")
        return

    print(f"Successfully loaded audio file: {audio_path}")
    print(f"Total audio duration: {len(audio) / 1000:.2f} seconds")

    for i, q_data in enumerate(json_data):
        start_ms = int(q_data['start'] * 1000)
        end_ms = int(q_data['end'] * 1000)
        question_text = q_data['text']

        # Ensure the timestamps are within the audio duration
        if start_ms >= len(audio):
            print(f"Warning: Question {i+1} ('{question_text}') starts beyond audio length ({start_ms}ms > {len(audio)}ms). Skipping.")
            continue
        if end_ms > len(audio):
            print(f"Warning: Question {i+1} ('{question_text}') ends beyond audio length ({end_ms}ms > {len(audio)}ms). Truncating.")
            end_ms = len(audio)
        
        if start_ms >= end_ms:
            print(f"Warning: Question {i+1} ('{question_text}') has an invalid time range (start >= end). Skipping.")
            continue

        segment = audio[start_ms:end_ms]

        # Sanitize filename:
        # 1. Replace spaces with underscores
        # 2. Keep only alphanumeric characters and underscores
        # 3. Limit length to avoid excessively long filenames
        filename_prefix = "".join(c for c in question_text if c.isalnum() or c.isspace())
        filename_prefix = filename_prefix.replace(" ", "_")
        filename_prefix = filename_prefix[:60].strip('_') # Keep first 60 chars and strip trailing underscores
        
        # Add a counter to ensure unique filenames in case of identical text
        output_filename = os.path.join(output_dir, f"question_{i+1:03d}_{filename_prefix}.mp3")

        try:
            segment.export(output_filename, format="mp3")
            print(f"Extracted question {i+1}: '{question_text}' to {output_filename}")
        except Exception as e:
            print(f"Error exporting segment for question {i+1} ('{question_text}'): {e}")

# Define the paths
audio_file_path = "/Users/eemanmajumder/code_shit/inter/interview.mp3"
json_file_path = "./values.json"
output_directory = "./questions"

# Load the JSON data from the file
try:
    with open(json_file_path, 'r') as f:
        questions_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    exit()
except json.JSONDecodeError as e:
    print(f"Error decoding JSON from {json_file_path}: {e}")
    exit()

# Run the extraction function
extract_questions_to_audio(audio_file_path, questions_data, output_directory)