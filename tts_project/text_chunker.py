"""
text_chunker.py
----------------
Splits arbitrarily long text into small, TTS-friendly chunks.

Why this matters: almost every TTS engine/API (offline or cloud) has a
per-call character limit and tends to produce worse prosody on huge blobs
of text. To support "unlimited" length input, we never hand the whole
document to the engine at once. Instead we:

  1. Split on paragraph breaks first (keeps topic/pause structure).
  2. Split paragraphs into sentences.
  3. Greedily pack sentences into chunks up to `max_chars`, never
     splitting a sentence in half.
  4. If a single "sentence" is still too long (e.g. no punctuation,
     a huge run-on line), hard-split it on word boundaries as a fallback.

The result is a list[str] that can be fed one-by-one into any TTS backend,
then the resulting audio chunks are concatenated back together.
"""

import re
from typing import List

# Matches sentence-ending punctuation followed by whitespace.
# Handles ., !, ?, and combinations like ?!  ...
_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(\u201c])|(?<=[.!?])\s*\n+")

_PARAGRAPH_SPLIT_RE = re.compile(r"\n\s*\n+")


def _split_into_sentences(paragraph: str) -> List[str]:
    paragraph = paragraph.strip()
    if not paragraph:
        return []
    sentences = _SENTENCE_SPLIT_RE.split(paragraph)
    return [s.strip() for s in sentences if s.strip()]


def _hard_split(text: str, max_chars: int) -> List[str]:
    """Fallback: split on word boundaries when a sentence alone exceeds max_chars."""
    words = text.split()
    pieces = []
    current = []
    current_len = 0
    for word in words:
        add_len = len(word) + (1 if current else 0)
        if current_len + add_len > max_chars and current:
            pieces.append(" ".join(current))
            current = [word]
            current_len = len(word)
        else:
            current.append(word)
            current_len += add_len
    if current:
        pieces.append(" ".join(current))
    return pieces


def chunk_text(text: str, max_chars: int = 500) -> List[str]:
    """
    Break `text` (of any length) into a list of chunks, each <= max_chars,
    breaking only at sentence or paragraph boundaries when possible.

    Args:
        text: The full input text (a sentence, a page, or an entire book).
        max_chars: Soft cap on characters per chunk. Keep this modest
                   (300-800) for natural-sounding pacing and to stay well
                   under any engine's hard limit.

    Returns:
        List of text chunks in original reading order.
    """
    if not text or not text.strip():
        return []

    chunks: List[str] = []
    current = ""

    paragraphs = _PARAGRAPH_SPLIT_RE.split(text.strip())

    for para in paragraphs:
        sentences = _split_into_sentences(para)
        for sentence in sentences:
            if len(sentence) > max_chars:
                # Flush whatever we were building, then hard-split the
                # oversized sentence on its own.
                if current:
                    chunks.append(current.strip())
                    current = ""
                chunks.extend(_hard_split(sentence, max_chars))
                continue

            candidate = f"{current} {sentence}".strip() if current else sentence
            if len(candidate) <= max_chars:
                current = candidate
            else:
                chunks.append(current.strip())
                current = sentence

        # Prefer to end a chunk at a paragraph boundary if we're close
        # to the limit already, so pauses line up with the source text.
        if current and len(current) > max_chars * 0.6:
            chunks.append(current.strip())
            current = ""

    if current.strip():
        chunks.append(current.strip())

    return chunks


if __name__ == "__main__":
    sample = (
        "This is a short test. It has a couple of sentences!\n\n"
        "And a new paragraph here, just to check that splitting on blank "
        "lines behaves the way we expect it to behave in practice."
    )
    for i, c in enumerate(chunk_text(sample, max_chars=60), 1):
        print(f"[{i}] ({len(c)} chars) {c}")
