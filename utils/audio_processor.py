import os
import re
import glob
import yt_dlp
from pydub import AudioSegment

TEMP_DIR = "temp_audio"


def is_youtube_url(url: str) -> bool:
    """Check if the given string is a YouTube or generic media URL."""
    url_pattern = re.compile(
        r'^(https?://)?(www\.)?(youtube\.com|youtu\.be|vimeo\.com|soundcloud\.com)/.+$',
        re.IGNORECASE,
    )
    return bool(url_pattern.match(url.strip())) or url.strip().startswith("http://") or url.strip().startswith("https://")


def download_youtube_audio(url: str, output_dir: str = TEMP_DIR) -> str:
    """Download audio from a YouTube URL and convert it to WAV format."""
    os.makedirs(output_dir, exist_ok=True)
    out_template = os.path.join(output_dir, "downloaded_%(id)s.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": out_template,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
        "quiet": False,
        "no_warnings": True,
    }

    print(f"Downloading audio from {url} ...")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        video_id = info.get("id", "audio")
        wav_path = os.path.join(output_dir, f"downloaded_{video_id}.wav")

    if not os.path.exists(wav_path):
        # Fallback: search for newly created wav file in output_dir
        wav_files = glob.glob(os.path.join(output_dir, "downloaded_*.wav"))
        if wav_files:
            wav_path = max(wav_files, key=os.path.getmtime)
        else:
            raise FileNotFoundError(f"Failed to find downloaded audio file for {url}")

    print(f"Downloaded and converted audio to: {wav_path}")
    return wav_path


def split_audio(audio_path: str, chunk_length_sec: int = 300, output_dir: str = TEMP_DIR) -> list[str]:
    """Split an audio file into smaller chunks (default 5 minutes / 300s each)."""
    os.makedirs(output_dir, exist_ok=True)
    print(f"Loading audio file: {audio_path} ...")
    audio = AudioSegment.from_file(audio_path)

    chunk_ms = chunk_length_sec * 1000
    total_length_ms = len(audio)

    # If the audio is shorter than the chunk duration, export as a single chunk
    if total_length_ms <= chunk_ms:
        single_chunk_path = os.path.join(output_dir, "chunk_0.wav")
        audio.export(single_chunk_path, format="wav")
        return [single_chunk_path]

    chunks = []
    total_chunks = (total_length_ms + chunk_ms - 1) // chunk_ms
    print(f"Splitting audio into {total_chunks} chunks of {chunk_length_sec} seconds each ...")

    for i in range(0, total_length_ms, chunk_ms):
        chunk_idx = i // chunk_ms
        chunk = audio[i : i + chunk_ms]
        chunk_file = os.path.join(output_dir, f"chunk_{chunk_idx}.wav")
        chunk.export(chunk_file, format="wav")
        chunks.append(chunk_file)

    return chunks


def process_input(source: str, chunk_length_sec: int = 300) -> list[str]:
    """
    Main entry point for audio processing:
    - If URL -> download audio as WAV.
    - If local file -> extract/read audio.
    - Slice into chunks and return list of filepaths.
    """
    os.makedirs(TEMP_DIR, exist_ok=True)
    source = source.strip()

    if is_youtube_url(source):
        wav_path = download_youtube_audio(source, output_dir=TEMP_DIR)
    else:
        if not os.path.exists(source):
            raise FileNotFoundError(f"Specified input file not found: {source}")
        wav_path = source

    chunks = split_audio(wav_path, chunk_length_sec=chunk_length_sec, output_dir=TEMP_DIR)
    print(f"Audio processing complete: generated {len(chunks)} chunk(s).")
    return chunks
