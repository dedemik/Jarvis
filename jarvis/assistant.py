import unicodedata
from datetime import datetime
from pathlib import Path

from jarvis.calculator import calculate
from jarvis.notes import NoteStore
from jarvis.reminders import ReminderStore
from jarvis.tasks import TaskStore


class JarvisAssistant:
    def __init__(self, notes_database_path: str | Path | None = None):
        self.notes = NoteStore(notes_database_path)
        self.tasks = TaskStore(self.notes.database_path)
        self.reminders = ReminderStore(self.notes.database_path)

    def handle_command(self, command: str) -> tuple[str, bool]:
        response, keep_running = self._handle_command(command)
        due_reminders = self.check_due_reminders()
        if due_reminders:
            response = f"{due_reminders}\n{response}"
        return response, keep_running

    def check_due_reminders(self, now: datetime | None = None) -> str:
        due_reminders = self.reminders.notify_due(now)
        if not due_reminders:
            return ""
        formatted_reminders = "\n".join(
            f"  #{reminder_id}: {content}"
            for reminder_id, content in due_reminders
        )
        return f"Hatırlatıcı zamanı geldi:\n{formatted_reminders}"

    def _handle_command(self, command: str) -> tuple[str, bool]:
        normalized = unicodedata.normalize("NFKC", command).strip().casefold()
        normalized = normalized.translate(str.maketrans("ıçşğüö", "icsguo"))

        if normalized in {"", "merhaba", "selam", "hey jarvis"}:
            return "Merhaba! Sana nasıl yardımcı olabilirim?", True
        if normalized in {"yardim", "komutlar", "ne yapabilirsin"}:
            return (
                "Kullanabileceğin komutlar:\n"
                "  saat       - Saati gösterir\n"
                "  tarih      - Tarihi gösterir\n"
                "  hesapla    - Örnek: hesapla 12 * (3 + 2)\n"
                "  not ekle   - Örnek: not ekle Alışveriş listesi\n"
                "  notlar     - Kayıtlı notları listeler\n"
                "  not sil    - Örnek: not sil 1\n"
                "  yapılacak ekle - Örnek: yapılacak ekle E-postayı yanıtla\n"
                "  yapılacaklar   - Yapılacakları listeler\n"
                "  yapılacak tamamla - Örnek: yapılacak tamamla 1\n"
                "  yapılacak sil - Örnek: yapılacak sil 1\n"
                "  hatırlatıcı ekle - Örnek: hatırlatıcı ekle 2026-11-05 10:00 Doktor\n"
                "  hatırlatıcılar - Hatırlatıcıları listeler\n"
                "  hatırlatıcı sil - Örnek: hatırlatıcı sil 1\n"
                "  yardım     - Bu komutları gösterir\n"
                "  çıkış      - Asistanı kapatır",
                True,
            )
        command_parts = normalized.split(maxsplit=2)
        if command_parts[:2] == ["hatirlatici", "ekle"]:
            raw_parts = command.strip().split(maxsplit=4)
            if len(raw_parts) < 5 or not raw_parts[4].strip():
                return (
                    "Kullanım: hatırlatıcı ekle YYYY-AA-GG SS:DD <açıklama>",
                    True,
                )
            try:
                due_text = f"{raw_parts[2]} {raw_parts[3]}"
                due_at = datetime.strptime(due_text, "%Y-%m-%d %H:%M")
                if due_at.strftime("%Y-%m-%d %H:%M") != due_text:
                    raise ValueError
            except ValueError:
                return (
                    "Tarih ve saat YYYY-AA-GG SS:DD biçiminde olmalı.",
                    True,
                )
            if due_at <= datetime.now().replace(second=0, microsecond=0):
                return "Hatırlatıcı zamanı gelecekte olmalı.", True
            reminder_id = self.reminders.add(raw_parts[4].strip(), due_at)
            return f"Hatırlatıcı kaydedildi (#{reminder_id}).", True
        if normalized in {"hatirlaticilar", "hatirlatici listele"}:
            reminders = self.reminders.list_all()
            if not reminders:
                return "Henüz kayıtlı hatırlatıcın yok.", True
            formatted_reminders = "\n".join(
                f"  {reminder_id}. {due_at:%Y-%m-%d %H:%M} "
                f"[{'bildirildi' if notified else 'bekliyor'}] {content}"
                for reminder_id, content, due_at, notified in reminders
            )
            return f"Hatırlatıcıların:\n{formatted_reminders}", True
        if command_parts[:2] == ["hatirlatici", "sil"]:
            if len(command_parts) != 3:
                return "Kullanım: hatırlatıcı sil <numara>", True
            try:
                reminder_id = int(command_parts[2])
            except ValueError:
                return "Hatırlatıcı numarası pozitif bir tam sayı olmalı.", True
            if reminder_id < 1:
                return "Hatırlatıcı numarası pozitif bir tam sayı olmalı.", True
            if self.reminders.delete(reminder_id):
                return f"Hatırlatıcı #{reminder_id} silindi.", True
            return f"#{reminder_id} numaralı hatırlatıcı bulunamadı.", True
        if command_parts[:2] == ["not", "ekle"]:
            raw_parts = command.strip().split(maxsplit=2)
            if len(raw_parts) < 3 or not raw_parts[2].strip():
                return "Kullanım: not ekle <not metni>", True
            note_id = self.notes.add(raw_parts[2].strip())
            return f"Not kaydedildi (#{note_id}).", True
        if normalized in {"notlar", "not listele"}:
            notes = self.notes.list_all()
            if not notes:
                return "Henüz kayıtlı notun yok.", True
            formatted_notes = "\n".join(
                f"  {note_id}. {content}" for note_id, content in notes
            )
            return f"Notların:\n{formatted_notes}", True
        if command_parts[:2] == ["not", "sil"]:
            if len(command_parts) != 3:
                return "Kullanım: not sil <not numarası>", True
            try:
                note_id = int(command_parts[2])
            except ValueError:
                return "Not numarası pozitif bir tam sayı olmalı.", True
            if note_id < 1:
                return "Not numarası pozitif bir tam sayı olmalı.", True
            if self.notes.delete(note_id):
                return f"Not #{note_id} silindi.", True
            return f"#{note_id} numaralı not bulunamadı.", True
        if command_parts[:2] == ["yapilacak", "ekle"]:
            raw_parts = command.strip().split(maxsplit=2)
            if len(raw_parts) < 3 or not raw_parts[2].strip():
                return "Kullanım: yapılacak ekle <görev>", True
            task_id = self.tasks.add(raw_parts[2].strip())
            return f"Yapılacak eklendi (#{task_id}).", True
        if normalized in {
            "yapilacaklar",
            "yapilacak listele",
            "gorevler",
            "gorev listele",
        }:
            tasks = self.tasks.list_all()
            if not tasks:
                return "Henüz yapılacak bir işin yok.", True
            formatted_tasks = "\n".join(
                f"  {task_id}. [{'x' if completed else ' '}] {content}"
                for task_id, content, completed in tasks
            )
            return f"Yapılacakların:\n{formatted_tasks}", True
        if command_parts[:2] in (
            ["yapilacak", "tamamla"],
            ["gorev", "tamamla"],
        ):
            if len(command_parts) != 3:
                return "Kullanım: yapılacak tamamla <numara>", True
            try:
                task_id = int(command_parts[2])
            except ValueError:
                return "Görev numarası pozitif bir tam sayı olmalı.", True
            if task_id < 1:
                return "Görev numarası pozitif bir tam sayı olmalı.", True
            if self.tasks.complete(task_id):
                return f"Yapılacak #{task_id} tamamlandı.", True
            return f"#{task_id} numaralı açık yapılacak bulunamadı.", True
        if command_parts[:2] in (
            ["yapilacak", "sil"],
            ["gorev", "sil"],
        ):
            if len(command_parts) != 3:
                return "Kullanım: yapılacak sil <numara>", True
            try:
                task_id = int(command_parts[2])
            except ValueError:
                return "Görev numarası pozitif bir tam sayı olmalı.", True
            if task_id < 1:
                return "Görev numarası pozitif bir tam sayı olmalı.", True
            if self.tasks.delete(task_id):
                return f"Yapılacak #{task_id} silindi.", True
            return f"#{task_id} numaralı yapılacak bulunamadı.", True
        if normalized in {"saat", "saat kac"}:
            return f"Saat: {datetime.now().astimezone().strftime('%H:%M')}", True
        if normalized in {"tarih", "bugun tarih ne", "bugunun tarihi"}:
            return f"Tarih: {datetime.now().astimezone().strftime('%d.%m.%Y')}", True
        if normalized.startswith("hesapla"):
            expression = normalized[len("hesapla"):].lstrip(" :")
            try:
                return f"Sonuç: {calculate(expression)}", True
            except ValueError as error:
                return str(error), True
        if normalized in {"cik", "cikis", "kapat", "gorusuruz"}:
            return "Görüşürüz!", False

        return (
            "Bu komutu tanıyamadım. Kullanılabilir komutları görmek için 'yardım' yaz.",
            True,
        )
