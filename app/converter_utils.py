import subprocess
import os
from werkzeug.utils import secure_filename

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def convert_to_mp3(file_path, bitrate="192k", samplerate="44100", channels="2", normalize=False):
    filename = os.path.basename(file_path)
    base_name = os.path.splitext(secure_filename(filename))[0]
    output_path = os.path.join(OUTPUT_DIR, f"{base_name}.mp3")

    cmd = [
        "ffmpeg", "-y", "-i", file_path,
        "-ac", channels,
        "-ar", samplerate,
        "-b:a", bitrate,
        "-codec:a", "libmp3lame"
    ]

    if normalize:
        cmd.extend(["-af", "loudnorm"])

    cmd.append(output_path)
    subprocess.run(cmd, check=True)
    return output_path