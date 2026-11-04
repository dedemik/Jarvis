import sqlite3
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

from jarvis.assistant import JarvisAssistant


class JarvisChatWindow:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Jarvis")
        self.root.geometry("1024x720")
        self.root.minsize(680, 500)
        self.root.configure(bg="#ffffff")
        self.assistant = JarvisAssistant()

        self._build_layout()
        self._show_welcome()

        try:
            due_reminders = self.assistant.check_due_reminders()
        except sqlite3.Error as error:
            self._append_message("Jarvis", f"Veritabanı hatası: {error}")
        else:
            if due_reminders:
                self._append_message("Jarvis", due_reminders)

    def _build_layout(self) -> None:
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        sidebar = tk.Frame(self.root, width=220, bg="#f5f5f5")
        sidebar.grid(row=0, column=0, sticky="ns")
        sidebar.grid_propagate(False)

        tk.Label(
            sidebar,
            text="Jarvis",
            font=("TkDefaultFont", 18, "bold"),
            bg="#f5f5f5",
            fg="#202123",
        ).pack(anchor="w", padx=18, pady=(22, 18))

        tk.Button(
            sidebar,
            text="+  Yeni sohbet",
            anchor="w",
            command=self._new_chat,
            relief="flat",
            bg="#e8e8e8",
            activebackground="#dddddd",
            padx=12,
            pady=9,
        ).pack(fill="x", padx=12, pady=(0, 20))

        tk.Label(
            sidebar,
            text="ÖRNEK KOMUTLAR",
            font=("TkDefaultFont", 9, "bold"),
            bg="#f5f5f5",
            fg="#777777",
        ).pack(anchor="w", padx=18, pady=(0, 8))

        for label, command in (
            ("Yardım", "yardım"),
            ("Saat", "saat"),
            ("Notlar", "notlar"),
            ("Yapılacaklar", "yapılacaklar"),
            ("Hatırlatıcılar", "hatırlatıcılar"),
        ):
            tk.Button(
                sidebar,
                text=label,
                anchor="w",
                command=lambda value=command: self._send_message(value),
                relief="flat",
                bg="#f5f5f5",
                activebackground="#e8e8e8",
                padx=12,
                pady=7,
            ).pack(fill="x", padx=12)

        chat = tk.Frame(self.root, bg="#ffffff")
        chat.grid(row=0, column=1, sticky="nsew")
        chat.grid_rowconfigure(1, weight=1)
        chat.grid_columnconfigure(0, weight=1)

        header = tk.Frame(chat, bg="#ffffff", height=58)
        header.grid(row=0, column=0, sticky="ew")
        tk.Label(
            header,
            text="Jarvis",
            font=("TkDefaultFont", 14, "bold"),
            bg="#ffffff",
            fg="#202123",
        ).pack(side="left", padx=24, pady=17)
        tk.Label(
            header,
            text="Yerel komut asistanı",
            font=("TkDefaultFont", 10),
            bg="#ffffff",
            fg="#777777",
        ).pack(side="right", padx=24)

        self.history = ScrolledText(
            chat,
            wrap="word",
            state="disabled",
            borderwidth=0,
            padx=24,
            pady=20,
            bg="#ffffff",
            fg="#202123",
            font=("TkDefaultFont", 11),
            spacing1=5,
            spacing3=14,
        )
        self.history.grid(row=1, column=0, sticky="nsew")
        self.history.tag_configure(
            "user",
            foreground="#202123",
            font=("TkDefaultFont", 11, "bold"),
        )
        self.history.tag_configure(
            "assistant",
            foreground="#16856b",
            font=("TkDefaultFont", 11, "bold"),
        )
        self.history.tag_configure("body", foreground="#202123")

        composer = tk.Frame(chat, bg="#ffffff", padx=24, pady=(10, 8))
        composer.grid(row=2, column=0, sticky="ew")
        composer.grid_columnconfigure(0, weight=1)

        self.message_input = tk.Text(
            composer,
            height=3,
            wrap="word",
            font=("TkDefaultFont", 11),
            padx=12,
            pady=10,
            relief="solid",
            borderwidth=1,
            undo=True,
        )
        self.message_input.grid(row=0, column=0, sticky="ew")
        self.message_input.bind("<Return>", self._on_return)

        tk.Button(
            composer,
            text="Gönder",
            command=self._send_message,
            relief="flat",
            bg="#202123",
            fg="#ffffff",
            activebackground="#343541",
            activeforeground="#ffffff",
            padx=18,
            pady=9,
        ).grid(row=0, column=1, padx=(10, 0), sticky="s")

        tk.Label(
            chat,
            text="Bu sürüm yerel komutlarla çalışır; yapay zekâ sohbeti henüz bağlı değil.",
            font=("TkDefaultFont", 9),
            bg="#ffffff",
            fg="#777777",
        ).grid(row=3, column=0, pady=(0, 12))

    def _new_chat(self) -> None:
        self.history.configure(state="normal")
        self.history.delete("1.0", "end")
        self.history.configure(state="disabled")
        self.message_input.delete("1.0", "end")
        self._show_welcome()
        self.message_input.focus_set()

    def _show_welcome(self) -> None:
        self._append_message(
            "Jarvis",
            "Merhaba! Sana nasıl yardımcı olabilirim?\n\n"
            "Saat için “saat”, notlarını görmek için “notlar”, "
            "yapılacaklarını görmek için “yapılacaklar” yazabilirsin. "
            "Tüm komutlar için “yardım” yaz.",
        )

    def _append_message(self, speaker: str, message: str) -> None:
        self.history.configure(state="normal")
        speaker_tag = "user" if speaker == "Sen" else "assistant"
        self.history.insert("end", f"{speaker}\n", speaker_tag)
        self.history.insert("end", f"{message}\n\n", "body")
        self.history.configure(state="disabled")
        self.history.see("end")

    def _on_return(self, event: tk.Event) -> str | None:
        if event.state & 0x0001:
            return None
        self._send_message()
        return "break"

    def _send_message(self, message: str | None = None) -> None:
        if message is None:
            message = self.message_input.get("1.0", "end-1c").strip()
            self.message_input.delete("1.0", "end")
        if not message.strip():
            return

        self._append_message("Sen", message)
        try:
            response, keep_running = self.assistant.handle_command(message)
        except sqlite3.Error as error:
            response, keep_running = f"Veritabanı hatası: {error}", True
        self._append_message("Jarvis", response)

        if not keep_running:
            self.root.after(500, self.root.destroy)

    def run(self) -> None:
        self.message_input.focus_set()
        self.root.mainloop()


def main() -> None:
    JarvisChatWindow().run()


if __name__ == "__main__":
    main()
