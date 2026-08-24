#!/usr/bin/env python3
"""
main.py
-------
CLI entry point for unlimited-length text-to-speech.

Usage examples:

    # Convert a text file to an mp3, using the offline default backend
    python3 main.py --input book.txt --output book.mp3

    # Read text piped/typed directly
    python3 main.py --text "Hello, this can be as long as you like." --output hello.wav

    # Tune chunk size, speaking rate, and pick a different backend
    python3 main.py --input article.txt --output article.mp3 \\
        --backend pyttsx3 --rate 190 --chunk-size 400

    # Resume an interrupted run (uses --output's name to find the
    # checkpoint folder from the earlier attempt)
    python3 main.py --input book.txt --output book.mp3 --resume

Design for "unlimited" length:
  - Text is chunked (text_chunker.py) so no single TTS call ever exceeds
    a safe character count.
  - Each chunk is synthesized to its own small WAV file in a checkpoint
    directory (".tts_checkpoints_<output-name>/"), numbered in order.
  - Already-synthesized chunks are skipped on re-run (--resume), so a
    100,000-word document can be processed across multiple sessions,
    survive a crash, or be safely Ctrl-C'd and picked back up.
  - Once every chunk exists, they are concatenated into the single final
    output file and the checkpoint directory is removed.

There is no hard ceiling on total output length: it's bounded only by
disk space and time, not by any API/engine per-request limit.
"""

import argparse
import os
import shutil
import sys

from text_chunker import chunk_text
from tts_engine import get_backend
from audio_utils import concatenate_wavs

try:
    from tqdm import tqdm
except ImportError:  # tqdm is a soft dependency for the progress bar only
    def tqdm(iterable, **kwargs):
        return iterable


def _checkpoint_dir(output_path: str) -> str:
    base = os.path.splitext(os.path.basename(output_path))[0]
    return os.path.join(os.path.dirname(os.path.abspath(output_path)) or ".",
                         f".tts_checkpoints_{base}")


def synthesize_long_text(text: str, output_path: str, backend_name: str = "pyttsx3",
                          chunk_size: int = 500, gap_ms: int = 150,
                          resume: bool = False, voice_opts: dict | None = None) -> None:
    voice_opts = voice_opts or {}
    chunks = chunk_text(text, max_chars=chunk_size)
    if not chunks:
        raise ValueError("Input text is empty after chunking; nothing to synthesize.")

    ckpt_dir = _checkpoint_dir(output_path)
    if not resume and os.path.isdir(ckpt_dir):
        shutil.rmtree(ckpt_dir)
    os.makedirs(ckpt_dir, exist_ok=True)

    backend = get_backend(backend_name)

    chunk_paths = []
    print(f"Synthesizing {len(chunks)} chunk(s) with backend='{backend_name}' "
          f"({sum(len(c) for c in chunks):,} characters total)...")

    for i, chunk in enumerate(tqdm(chunks, desc="Synthesizing", unit="chunk")):
        chunk_path = os.path.join(ckpt_dir, f"chunk_{i:06d}.wav")
        chunk_paths.append(chunk_path)
        if resume and os.path.exists(chunk_path):
            continue  # already done in a previous run
        backend.synth(chunk, chunk_path, **voice_opts)

    print("Merging chunks into final output...")
    concatenate_wavs(chunk_paths, output_path, gap_ms=gap_ms)

    shutil.rmtree(ckpt_dir)
    print(f"Done. Wrote: {output_path}")


def _parse_args():
    p = argparse.ArgumentParser(description="Unlimited-length text-to-speech generator.")
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--input", help="Path to a .txt file of any length.")
    src.add_argument("--text", help="Literal text to synthesize (any length).")

    p.add_argument("--output", required=True,
                    help="Output audio file path, e.g. out.mp3 or out.wav.")
    p.add_argument("--backend", default="pyttsx3",
                    choices=["pyttsx3", "edge", "gtts"],
                    help="TTS engine to use. 'pyttsx3' is offline and default.")
    p.add_argument("--chunk-size", type=int, default=500,
                    help="Max characters per internal chunk (default: 500).")
    p.add_argument("--gap-ms", type=int, default=150,
                    help="Silence (ms) inserted between chunks (default: 150).")
    p.add_argument("--rate", type=int, default=175,
                    help="Speaking rate for pyttsx3 (words/min-ish, default: 175).")
    p.add_argument("--voice-id", default=None,
                    help="Backend-specific voice identifier "
                         "(e.g. an edge-tts voice name, or a pyttsx3 voice id).")
    p.add_argument("--list-voices", action="store_true",
                    help="List available voices for the pyttsx3 backend and exit.")
    p.add_argument("--resume", action="store_true",
                    help="Resume a previous interrupted run for this --output.")
    return p.parse_args()


def main():
    args = _parse_args()

    if args.list_voices:
        from tts_engine import Pyttsx3Backend
        for vid, vname, langs in Pyttsx3Backend.list_voices():
            print(f"{vid}\t{vname}\t{langs}")
        sys.exit(0)

    if args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        text = args.text

    voice_opts = {"rate": args.rate}
    if args.voice_id:
        voice_opts["voice_id"] = args.voice_id

    synthesize_long_text(
        text=text,
        output_path=args.output,
        backend_name=args.backend,
        chunk_size=args.chunk_size,
        gap_ms=args.gap_ms,
        resume=args.resume,
        voice_opts=voice_opts,
    )


if __name__ == "__main__":
    main()
