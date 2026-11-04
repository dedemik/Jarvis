import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import Mock, patch

from jarvis.voice import VoiceDependencyError
from jarvis.voice_cli import main


class VoiceCliTests(unittest.TestCase):
    @patch("jarvis.voice_cli.VoiceIO")
    @patch("jarvis.voice_cli.JarvisAssistant")
    def test_voice_commands_use_assistant_and_speech_output(
        self,
        assistant_factory,
        voice_factory,
    ):
        assistant = assistant_factory.return_value
        assistant.handle_command.side_effect = [
            ("Saat: 10:30", True),
            ("Görüşürüz!", False),
        ]
        voice = voice_factory.return_value
        voice.listen.side_effect = ["saat", "çıkış"]

        with redirect_stdout(io.StringIO()):
            result = main()

        self.assertEqual(result, 0)
        assistant.handle_command.assert_any_call("saat")
        assistant.handle_command.assert_any_call("çıkış")
        voice.speak.assert_any_call("Saat: 10:30")
        voice.speak.assert_any_call("Görüşürüz!")

    @patch("jarvis.voice_cli.VoiceIO")
    @patch("jarvis.voice_cli.JarvisAssistant")
    def test_missing_voice_dependencies_are_reported(
        self,
        assistant_factory,
        voice_factory,
    ):
        voice_factory.return_value.listen.side_effect = VoiceDependencyError(
            "Ses paketleri eksik."
        )

        output = io.StringIO()
        with redirect_stdout(output):
            result = main()

        self.assertEqual(result, 1)
        self.assertIn("Ses paketleri eksik.", output.getvalue())
        assistant_factory.return_value.handle_command.assert_not_called()


if __name__ == "__main__":
    unittest.main()