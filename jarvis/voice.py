from __future__ import annotations

from typing import Any


class VoiceDependencyError(RuntimeError):
    pass


class VoiceIO:
    def __init__(self, recording_seconds: int = 5) -> None:
        if recording_seconds < 1:
            raise ValueError("Kayıt süresi en az 1 saniye olmalı.")
        self.recording_seconds = recording_seconds
        self.sample_rate = 16_000
        self._model: Any | None = None
        self._engine: Any | None = None

    def listen(self) -> str:
        try:
            import numpy
            import sounddevice as sounddevice
            from faster_whisper import WhisperModel
        except (ImportError, OSError) as error:
            raise VoiceDependencyError(
                "Ses paketleri eksik. Kurulum için ./install-voice.sh çalıştır."
            ) from error

        if self._model is None:
            self._model = WhisperModel(
                "base",
                device="cpu",
                compute_type="int8",
            )

        recording_rate = int(
            sounddevice.query_devices(kind="input")["default_samplerate"]
        )
        audio = sounddevice.rec(
            int(self.recording_seconds * recording_rate),
            samplerate=recording_rate,
            channels=1,
            dtype="float32",
        )
        sounddevice.wait()
        audio = audio.reshape(-1)
        if recording_rate != self.sample_rate:
            target_count = round(
                audio.shape[0] * self.sample_rate / recording_rate
            )
            source_positions = numpy.arange(audio.shape[0], dtype=numpy.float64)
            target_positions = numpy.arange(
                target_count,
                dtype=numpy.float64,
            ) * recording_rate / self.sample_rate
            audio = numpy.interp(
                target_positions,
                source_positions,
                audio,
            ).astype(numpy.float32)
        segments, _ = self._model.transcribe(
            audio,
            language="tr",
            vad_filter=True,
        )
        return "".join(segment.text for segment in segments).strip()

    def speak(self, text: str) -> None:
        if not text.strip():
            return

        try:
            import pyttsx3
        except (ImportError, OSError) as error:
            raise VoiceDependencyError(
                "Seslendirme paketi eksik. Kurulum için ./install-voice.sh çalıştır."
            ) from error

        if self._engine is None:
            self._engine = pyttsx3.init()
            self._select_turkish_voice()

        self._engine.say(text)
        self._engine.runAndWait()

    def _select_turkish_voice(self) -> None:
        voices = self._engine.getProperty("voices")
        for voice in voices:
            languages = " ".join(str(language) for language in voice.languages)
            if "tr" in languages.casefold() or "turkish" in voice.name.casefold():
                self._engine.setProperty("voice", voice.id)
                return