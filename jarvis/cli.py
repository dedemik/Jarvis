from jarvis.assistant import JarvisAssistant


def main() -> None:
    assistant = JarvisAssistant()
    print("Jarvis hazır. Yardım için 'yardım' yaz, çıkmak için 'çıkış' yaz.")
    due_reminders = assistant.check_due_reminders()
    if due_reminders:
        print(f"Jarvis: {due_reminders}")

    while True:
        try:
            command = input("Sen: ")
        except (EOFError, KeyboardInterrupt):
            print("\nJarvis: Görüşürüz!")
            break

        response, keep_running = assistant.handle_command(command)
        print(f"Jarvis: {response}")
        if not keep_running:
            break
