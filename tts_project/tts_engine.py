"""
tts_engine.py
-------------
Pluggable TTS backends. Every backend implements the same interface:

    synth(text: str, out_wav_path: str, **voice_opts) -> None

so main.py doesn't care which engine is actually producing the audio.

Backends included:

  * "pyttsx3"  (default) - fully OFFLINE, uses espeak-ng under the hood
                on Linux. No internet, no API key, no rate limit, no
                character cap -> genuinely unlimited total duration.
                Robotic-ish voice quality, but rock solid for long jobs.

  * "edge"     - Microsoft Edge neural voices via the `edge-tts` package.
                Free, no API key, much more natural voice, but requires
                internet access at synth time. Install with:
                    pip install edge-tts
                (Not usable inside this sandbox's restricted network,
                but works fine on a normal machine/CI runner.)

  * "gtts"     - Google Translate's TTS via the `gTTS` package. Free,
                no API key, needs internet. Install with:
                    pip install gTTS

Add a new backend by writing one more class with a `synth()` method and
registering it in `get_backend()`.
"""

from __future__ import annotations
import abc
import os


class TTSBackend(abc.ABC):
    name: str = "base"

    @abc.abstractmethod
    def synth(self, text: str, out_wav_path: str, **voice_opts) -> None:
        """Render `text` to a WAV file at `out_wav_path`."""
        raise NotImplementedError


class Pyttsx3Backend(TTSBackend):
    """Offline backend. Works with zero network access. Default choice."""

    name = "pyttsx3"

    def __init__(self):
        import pyttsx3  # imported lazily so other backends don't need it installed
        self._pyttsx3 = pyttsx3

    def synth(self, text: str, out_wav_path: str, rate: int = 175,
              volume: float = 1.0, voice_id: str | None = None) -> None:
        # A fresh engine instance per chunk avoids a known pyttsx3 issue
        # where the driver hangs after many sequential runOnce/save calls
        # in one long-lived process.
        engine = self._pyttsx3.init()
        engine.setProperty("rate", rate)
        engine.setProperty("volume", volume)
        if voice_id:
            engine.setProperty("voice", voice_id)
        engine.save_to_file(text, out_wav_path)
        engine.runAndWait()
        engine.stop()

    @staticmethod
    def list_voices():
        import pyttsx3
        engine = pyttsx3.init()
        voices = engine.getProperty("voices")
        engine.stop()
        return [(v.id, v.name, getattr(v, "languages", None)) for v in voices]


class EdgeTTSBackend(TTSBackend):
    """Online, neural-quality backend using Microsoft Edge's TTS service."""

    name = "edge"

    def __init__(self):
        import edge_tts  # pip install edge-tts
        self._edge_tts = edge_tts

    def synth(self, text: str, out_wav_path: str,
              voice_id: str = "en-US-AriaNeural", rate: str = "+0%",
              volume: str = "+0%") -> None:
        import asyncio

        async def _run():
            communicate = self._edge_tts.Communicate(
                text, voice=voice_id, rate=rate, volume=volume
            )
            # edge-tts natively writes mp3; we ask it to write directly
            # to out_wav_path's mp3 sibling, then let audio_utils convert.
            mp3_path = out_wav_path.replace(".wav", ".mp3")
            await communicate.save(mp3_path)
            from pydub import AudioSegment
            AudioSegment.from_file(mp3_path).export(out_wav_path, format="wav")
            os.remove(mp3_path)

        asyncio.run(_run())


class GTTSBackend(TTSBackend):
    """Online backend using Google Translate's TTS endpoint."""

    name = "gtts"

    def __init__(self):
        from gtts import gTTS  # pip install gTTS
        self._gTTS = gTTS

    def synth(self, text: str, out_wav_path: str, lang: str = "en",
              slow: bool = False, **_ignored) -> None:
        mp3_path = out_wav_path.replace(".wav", ".mp3")
        self._gTTS(text=text, lang=lang, slow=slow).save(mp3_path)
        from pydub import AudioSegment
        AudioSegment.from_file(mp3_path).export(out_wav_path, format="wav")
        os.remove(mp3_path)


_BACKENDS = {
    "pyttsx3": Pyttsx3Backend,
    "edge": EdgeTTSBackend,
    "gtts": GTTSBackend,
}


def get_backend(name: str) -> TTSBackend:
    if name not in _BACKENDS:
        raise ValueError(
            f"Unknown backend '{name}'. Available: {list(_BACKENDS)}"
        )
    return _BACKENDS[name]()
