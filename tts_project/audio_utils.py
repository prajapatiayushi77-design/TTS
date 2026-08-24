"""
audio_utils.py
--------------
Stitches per-chunk audio files into one continuous output track, and
provides small helpers for silence-padding between chunks so long-form
speech doesn't sound like chunks glued end-to-end with no breathing room.
"""

from pydub import AudioSegment


def concatenate_wavs(chunk_paths: list[str], out_path: str,
                      gap_ms: int = 150) -> None:
    """
    Concatenate a list of WAV files (in order) into a single output file.
    A short silence (`gap_ms`) is inserted between chunks to mimic natural
    sentence/paragraph pauses. Output format is inferred from `out_path`'s
    extension (wav, mp3, ogg, etc. - anything ffmpeg supports).

    This function itself does not care how many chunk files there are, so
    a 5-chunk clip and a 50,000-chunk audiobook are handled identically -
    total duration is bounded only by disk space, not by any engine limit.
    """
    if not chunk_paths:
        raise ValueError("No audio chunks to concatenate.")

    silence = AudioSegment.silent(duration=gap_ms)
    combined = AudioSegment.empty()
    for path in chunk_paths:
        combined += AudioSegment.from_file(path) + silence

    fmt = out_path.rsplit(".", 1)[-1].lower()
    combined.export(out_path, format="mp3" if fmt == "mp3" else fmt)
