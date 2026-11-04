import unittest
from datetime import datetime, timedelta
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from jarvis.assistant import JarvisAssistant


class AssistantTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.assistant = JarvisAssistant(
            Path(self.temp_dir.name) / "jarvis.sqlite3"
        )

    def test_help_is_available_with_turkish_characters(self):
        response, keep_running = self.assistant.handle_command("YARDIM")
        self.assertIn("hesapla", response)
        self.assertIn("not ekle", response)
        self.assertIn("yapılacak ekle", response)
        self.assertIn("hatırlatıcı ekle", response)
        self.assertTrue(keep_running)
        self.assertFalse(self.assistant.notes.database_path.exists())

    def test_calculator_command(self):
        self.assertEqual(
            self.assistant.handle_command("Hesapla: 6 / 2"),
            ("Sonuç: 3.0", True),
        )

    def test_time_and_date_commands(self):
        fixed_time = datetime(2026, 11, 3, 14, 5).astimezone()
        with patch("jarvis.assistant.datetime") as mocked_datetime:
            mocked_datetime.now.return_value.astimezone.return_value = fixed_time
            self.assertEqual(
                self.assistant.handle_command("saat"),
                ("Saat: 14:05", True),
            )
            self.assertEqual(
                self.assistant.handle_command("tarih"),
                ("Tarih: 03.11.2026", True),
            )

    def test_exit_command_stops_assistant(self):
        self.assertEqual(
            self.assistant.handle_command("Çıkış"),
            ("Görüşürüz!", False),
        )

    def test_notes_can_be_added_listed_and_deleted(self):
        self.assertEqual(
            self.assistant.handle_command("not ekle Bugün süt al"),
            ("Not kaydedildi (#1).", True),
        )
        self.assertEqual(
            self.assistant.handle_command("notlar"),
            ("Notların:\n  1. Bugün süt al", True),
        )
        self.assertEqual(
            self.assistant.handle_command("not sil 1"),
            ("Not #1 silindi.", True),
        )
        self.assertEqual(
            self.assistant.handle_command("notlar"),
            ("Henüz kayıtlı notun yok.", True),
        )

    def test_notes_persist_across_assistant_instances(self):
        database_path = Path(self.temp_dir.name) / "jarvis.sqlite3"
        self.assistant.handle_command("not ekle Türkçe karakterler")

        another_assistant = JarvisAssistant(database_path)

        self.assertEqual(
            another_assistant.handle_command("notlar"),
            ("Notların:\n  1. Türkçe karakterler", True),
        )

    def test_note_commands_validate_arguments(self):
        self.assertEqual(
            self.assistant.handle_command("not ekle"),
            ("Kullanım: not ekle <not metni>", True),
        )
        self.assertEqual(
            self.assistant.handle_command("not sil abc"),
            ("Not numarası pozitif bir tam sayı olmalı.", True),
        )
        self.assertEqual(
            self.assistant.handle_command("not sil 42"),
            ("#42 numaralı not bulunamadı.", True),
        )

    def test_tasks_can_be_added_listed_completed_and_deleted(self):
        self.assertEqual(
            self.assistant.handle_command(
                "yapılacak ekle E-postayı yanıtla"
            ),
            ("Yapılacak eklendi (#1).", True),
        )
        self.assertEqual(
            self.assistant.handle_command("yapılacaklar"),
            ("Yapılacakların:\n  1. [ ] E-postayı yanıtla", True),
        )
        self.assertEqual(
            self.assistant.handle_command("yapılacak tamamla 1"),
            ("Yapılacak #1 tamamlandı.", True),
        )
        self.assertEqual(
            self.assistant.handle_command("görevler"),
            ("Yapılacakların:\n  1. [x] E-postayı yanıtla", True),
        )
        self.assertEqual(
            self.assistant.handle_command("yapılacak sil 1"),
            ("Yapılacak #1 silindi.", True),
        )
        self.assertEqual(
            self.assistant.handle_command("yapılacaklar"),
            ("Henüz yapılacak bir işin yok.", True),
        )

    def test_tasks_persist_across_assistant_instances(self):
        database_path = Path(self.temp_dir.name) / "jarvis.sqlite3"
        self.assistant.handle_command("yapılacak ekle Raporu hazırla")

        another_assistant = JarvisAssistant(database_path)

        self.assertEqual(
            another_assistant.handle_command("yapılacaklar"),
            ("Yapılacakların:\n  1. [ ] Raporu hazırla", True),
        )

    def test_task_commands_validate_arguments(self):
        self.assertEqual(
            self.assistant.handle_command("yapılacak ekle"),
            ("Kullanım: yapılacak ekle <görev>", True),
        )
        self.assertEqual(
            self.assistant.handle_command("yapılacak tamamla abc"),
            ("Görev numarası pozitif bir tam sayı olmalı.", True),
        )

    def test_reminders_can_be_added_listed_deleted_and_notified_once(self):
        due_at = (datetime.now() + timedelta(days=1)).replace(
            second=0, microsecond=0
        )
        self.assertEqual(
            self.assistant.handle_command(
                f"hatırlatıcı ekle {due_at:%Y-%m-%d %H:%M} Diş hekimi"
            ),
            ("Hatırlatıcı kaydedildi (#1).", True),
        )
        self.assertEqual(
            self.assistant.handle_command("hatırlatıcılar"),
            (
                "Hatırlatıcıların:\n"
                f"  1. {due_at:%Y-%m-%d %H:%M} [bekliyor] Diş hekimi",
                True,
            ),
        )

        self.assertEqual(
            self.assistant.check_due_reminders(due_at),
            "Hatırlatıcı zamanı geldi:\n  #1: Diş hekimi",
        )
        self.assertEqual(self.assistant.check_due_reminders(due_at), "")
        self.assertEqual(
            self.assistant.handle_command("hatırlatıcılar"),
            (
                "Hatırlatıcıların:\n"
                f"  1. {due_at:%Y-%m-%d %H:%M} [bildirildi] Diş hekimi",
                True,
            ),
        )
        self.assertEqual(
            self.assistant.handle_command("hatırlatıcı sil 1"),
            ("Hatırlatıcı #1 silindi.", True),
        )

    def test_due_reminders_are_added_to_command_responses(self):
        due_at = datetime(2026, 11, 5, 10, 30)
        self.assistant.reminders.add("Toplantıya katıl", due_at)

        with (
            patch("jarvis.assistant.datetime") as mocked_assistant_datetime,
            patch("jarvis.reminders.datetime") as mocked_reminder_datetime,
        ):
            mocked_assistant_datetime.now.return_value = datetime(
                2026, 11, 5, 10, 31
            )
            mocked_reminder_datetime.now.return_value = datetime(
                2026, 11, 5, 10, 31
            )
            mocked_reminder_datetime.fromisoformat.side_effect = (
                datetime.fromisoformat
            )
            response, keep_running = self.assistant.handle_command("saat")

        self.assertTrue(response.startswith("Hatırlatıcı zamanı geldi:"))
        self.assertTrue(response.endswith("Saat: 10:31"))
        self.assertTrue(keep_running)

    def test_reminder_commands_validate_arguments(self):
        self.assertEqual(
            self.assistant.handle_command("hatırlatıcı ekle"),
            (
                "Kullanım: hatırlatıcı ekle YYYY-AA-GG SS:DD <açıklama>",
                True,
            ),
        )
        self.assertEqual(
            self.assistant.handle_command(
                "hatırlatıcı ekle 2026-13-40 25:61 Açıklama"
            ),
            ("Tarih ve saat YYYY-AA-GG SS:DD biçiminde olmalı.", True),
        )
        self.assertEqual(
            self.assistant.handle_command(
                "hatırlatıcı ekle 2026-1-5 10:30 Açıklama"
            ),
            ("Tarih ve saat YYYY-AA-GG SS:DD biçiminde olmalı.", True),
        )
        self.assertEqual(
            self.assistant.handle_command("hatırlatıcı sil abc"),
            ("Hatırlatıcı numarası pozitif bir tam sayı olmalı.", True),
        )

    def test_reminders_persist_across_assistant_instances(self):
        due_at = (datetime.now() + timedelta(days=1)).replace(
            second=0, microsecond=0
        )
        self.assistant.handle_command(
            f"hatırlatıcı ekle {due_at:%Y-%m-%d %H:%M} Faturayı öde"
        )

        another_assistant = JarvisAssistant(self.assistant.notes.database_path)

        self.assertIn(
            f"{due_at:%Y-%m-%d %H:%M} [bekliyor] Faturayı öde",
            another_assistant.handle_command("hatırlatıcılar")[0],
        )

    def test_reminder_date_must_be_in_the_future(self):
        with patch("jarvis.assistant.datetime") as mocked_datetime:
            mocked_datetime.now.return_value = datetime(2026, 11, 5, 10, 30)
            mocked_datetime.strptime.side_effect = datetime.strptime
            self.assertEqual(
                self.assistant.handle_command(
                    "hatırlatıcı ekle 2026-11-05 10:30 Açıklama"
                ),
                ("Hatırlatıcı zamanı gelecekte olmalı.", True),
            )

    def test_reminder_time_format_must_be_valid(self):
        fixed_now = datetime.now().replace(second=0, microsecond=0)
        future_time = fixed_now + timedelta(days=1)
        with patch("jarvis.assistant.datetime") as mocked_datetime:
            mocked_datetime.now.return_value = fixed_now
            mocked_datetime.strptime.side_effect = datetime.strptime
            self.assertEqual(
                self.assistant.handle_command(
                    f"hatırlatıcı ekle {future_time:%Y-%m-%d %H:%M} Açıklama"
                ),
                ("Hatırlatıcı kaydedildi (#1).", True),
            )
