import sys
import types
import unittest
from unittest.mock import MagicMock, Mock, patch

from jarvis.voice import VoiceDependencyError, VoiceIO


class VoiceIOTests(unittest.TestCase):
    def test_listen_records_and_transcribes_turkish(self):
        audio = object()
        recorded_audio = types.SimpleNamespace(
            reshape=Mock(return_value=audio)
        )
        sounddevice = types.ModuleType("sounddevice")
        sounddevice.query_devices = Mock(
            return_value={"default_samplerate": 16_000}
        )
        sounddevice.rec = Mock(return_value=recorded_audio)
        sounddevice.wait = Mock()

        model = Mock()
        model.transcribe.return_value = (
            [types.SimpleNamespace(text=" Saat kaç"), types.SimpleNamespace(text="?")],
            object(),
        )
        whisper = types.ModuleType("faster_whisper")
        whisper.WhisperModel = Mock(return_value=model)
        numpy = types.ModuleType("numpy")

        with patch.dict(
            sys.modules,
            {
                "numpy": numpy,
                "sounddevice": sounddevice,
                "faster_whisper": whisper,
            },
        ):
            voice = VoiceIO(recording_seconds=3)

            self.assertEqual(voice.listen(), "Saat kaç?")
            self.assertEqual(voice.listen(), "Saat kaç?")

        sounddevice.rec.assert_called_with(
            48_000,
            samplerate=16_000,
            channels=1,
            dtype="float32",
        )
        sounddevice.wait.assert_called()
        whisper.WhisperModel.assert_called_once_with(
            "base",
            device="cpu",
            compute_type="int8",
        )
        model.transcribe.assert_called_with(
            audio,
            language="tr",
            vad_filter=True,
        )

    def test_listen_resamples_the_microphone_rate(self):
        mono_audio = types.SimpleNamespace(shape=(144_000,))
        recording = types.SimpleNamespace(
            reshape=Mock(return_value=mono_audio)
        )
        sounddevice = types.ModuleType("sounddevice")
        sounddevice.query_devices = Mock(
            return_value={"default_samplerate": 48_000}
        )
        sounddevice.rec = Mock(return_value=recording)
        sounddevice.wait = Mock()

        resampled_audio = Mock()
        converted_audio = object()
        resampled_audio.astype.return_value = converted_audio
        numpy = types.ModuleType("numpy")
        numpy.float32 = "float32"
        numpy.float64 = "float64"
        numpy.arange = Mock(return_value=MagicMock())
        numpy.interp = Mock(return_value=resampled_audio)

        model = Mock()
        model.transcribe.return_value = ([], object())
        whisper = types.ModuleType("faster_whisper")
        whisper.WhisperModel = Mock(return_value=model)

        with patch.dict(
            sys.modules,
            {
                "numpy": numpy,
                "sounddevice": sounddevice,
                "faster_whisper": whisper,
            },
        ):
            VoiceIO(recording_seconds=3).listen()

        sounddevice.rec.assert_called_once_with(
            144_000,
            samplerate=48_000,
            channels=1,
            dtype="float32",
        )
        numpy.interp.assert_called_once()
        resampled_audio.astype.assert_called_once_with("float32")
        model.transcribe.assert_called_once_with(
            converted_audio,
            language="tr",
            vad_filter=True,
        )

    def test_speak_uses_an_installed_turkish_voice(self):
        engine = Mock()
        engine.getProperty.return_value = [
            types.SimpleNamespace(id="tr", name="Turkish", languages=[]),
        ]
        pyttsx3 = types.ModuleType("pyttsx3")
        pyttsx3.init = Mock(return_value=engine)

        with patch.dict(sys.modules, {"pyttsx3": pyttsx3}):
            voice = VoiceIO()
            voice.speak("Merhaba")

        engine.setProperty.assert_called_once_with("voice", "tr")
        engine.say.assert_called_once_with("Merhaba")
        engine.runAndWait.assert_called_once_with()

    def test_listen_reports_missing_optional_dependencies(self):
        with patch.dict(sys.modules, {"sounddevice": None}):
            with self.assertRaises(VoiceDependencyError):
                VoiceIO().listen()


if __name__ == "__main__":
    unittest.main()