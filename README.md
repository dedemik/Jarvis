# Jarvis

Türkçe komut satırı asistanı. Temel özellikler Python standart kütüphanesiyle
çalışır; sesli kullanım isteğe bağlı paketler gerektirir.

## Proje yapısı

```text
.
├── jarvis/
│   ├── __init__.py
│   ├── __main__.py
│   ├── assistant.py
│   ├── calculator.py
│   ├── gui.py
│   ├── notes.py
│   ├── reminders.py
│   ├── tasks.py
│   ├── cli.py
│   ├── voice.py
│   └── voice_cli.py
├── tests/
│   ├── __init__.py
│   ├── test_assistant.py
│   ├── test_calculator.py
│   ├── test_voice.py
│   └── test_voice_cli.py
├── install.sh
├── install-voice.sh
├── run.sh
├── run-gui.sh
├── run-voice.sh
├── claude.md
├── install.md
├── progress.md
└── README.md
```

- `assistant.py`: Türkçe komutların ayrıştırılması ve yanıtlanması
- `calculator.py`: Temel matematik işlemleri
- `notes.py`: SQLite ile kalıcı not saklama
- `reminders.py`: SQLite ile kalıcı hatırlatıcı saklama
- `tasks.py`: SQLite ile kalıcı yapılacaklar saklama
- `cli.py`: Terminal giriş/çıkış döngüsü
- `gui.py`: Tkinter ile masaüstü sohbet arayüzü
- `voice.py`: İsteğe bağlı mikrofon, Türkçe konuşma tanıma ve seslendirme
- `voice_cli.py`: Sesli komut çalışma döngüsü
- `__main__.py`: `python3 -m jarvis` çalıştırma noktası
- `tests/`: Asistan ve hesap makinesi testleri

## Başlatma ve kurulum

Python 3.10 veya üzeri yeterlidir; harici paket gerekmez. Ayrıntılar için
[install.md](./install.md) dosyasına bakın.

```bash
./install.sh
./run.sh
```

Masaüstü sohbet penceresini açmak için:

```bash
./run-gui.sh
```

Arch Linux'ta isteğe bağlı ses paketlerini kurup sesli modu başlatmak için:

```bash
sudo pacman -S --needed portaudio espeak-ng
./install-voice.sh
./run-voice.sh
```

Sesli mod komut başına 5 saniye kayıt alır. Konuşma tanıma yerel Whisper
modeliyle yapılır; model ilk çalıştırmada indirilir. Türkçe sesli yanıt için
sistemde Türkçe eSpeak sesi bulunması gerekir. Ayrıntılar için
[install.md](./install.md) dosyasına bakın.

Arayüz mevcut Jarvis komutlarını kullanır; LLM bağlantısı içermez. Tkinter
kurulu değilse işletim sisteminin Python Tk paketini yüklemek gerekebilir.

Komut örnekleri:

- `yardım` — kullanılabilir komutları gösterir
- `saat` — yerel saati gösterir
- `tarih` — bugünün tarihini gösterir
- `hesapla 12 * (3 + 2)` — temel matematik işlemlerini yapar
- `not ekle Alışveriş listesi` — yeni bir not kaydeder
- `notlar` — kayıtlı notları listeler
- `not sil 1` — numarası 1 olan notu siler
- `yapılacak ekle E-postayı yanıtla` — yeni bir yapılacak ekler
- `yapılacaklar` — yapılacakları ve durumlarını listeler
- `yapılacak tamamla 1` — numarası 1 olan işi tamamlandı işaretler
- `yapılacak sil 1` — numarası 1 olan işi siler
- `hatırlatıcı ekle 2026-11-05 10:00 Doktor randevusu` — yerel saatte hatırlatıcı kurar
- `hatırlatıcılar` — hatırlatıcıları ve bildirim durumlarını listeler
- `hatırlatıcı sil 1` — numarası 1 olan hatırlatıcıyı siler
- `çıkış` — asistanı kapatır

Notlar, yapılacaklar ve hatırlatıcılar `~/.jarvis/jarvis.sqlite3` SQLite
veritabanında saklanır. Zamanı gelen hatırlatıcılar Jarvis başlarken ve her
komut işlendiğinde bildirilir; Jarvis komut beklerken anında uyarı vermez.
Saat, bilgisayarın yerel saat dilimini kullanır.

## Testler

```bash
python3 -m unittest discover -s tests -v
```

Geliştirme notları [claude.md](./claude.md), ilerleme ve sonraki adımlar
[progress.md](./progress.md) içindedir.