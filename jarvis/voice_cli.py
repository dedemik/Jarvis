from __future__ import annotations

from jarvis.assistant import JarvisAssistant
from jarvis.voice import VoiceDependencyError, VoiceIO


def main() -> int:
    assistant = JarvisAssistant()
    voice = VoiceIO()
    print(
        "Jarvis sesli mod hazır. Her komut için 5 saniye kayıt yapılır. "
        "Çıkmak için 'çıkış' deyin."
    )
    print("İlk kullanımda Türkçe konuşma modeli indirilir ve yerel saklanır.")

    try:
        while True:
            print("Jarvis: Dinliyorum...")
            command = voice.listen()
            if not command:
                print("Jarvis: Konuşmanı anlayamadım.")
                voice.speak("Konuşmanı anlayamadım.")
                continue

            print(f"Sen: {command}")
            response, keep_running = assistant.handle_command(command)
            print(f"Jarvis: {response}")
            voice.speak(response)
            if not keep_running:
                return 0
    except KeyboardInterrupt:
        print("\nJarvis: Görüşürüz!")
        return 0
    except VoiceDependencyError as error:
        print(f"Jarvis: {error}")
        return 1
    except Exception as error:
        print(f"Jarvis: Sesli komut hatası: {error}")
        return 1