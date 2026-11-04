# Jarvis

Python standart kütüphanesiyle çalışan, Türkçe komut satırı asistanı.

## Proje yapısı

```text
.
├── jarvis/
│   ├── __init__.py
│   ├── __main__.py
│   ├── assistant.py
│   ├── calculator.py
│   ├── notes.py
│   ├── reminders.py
│   ├── tasks.py
│   └── cli.py
├── tests/
│   ├── __init__.py
│   ├── test_assistant.py
│   └── test_calculator.py
├── install.sh
├── run.sh
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
- `__main__.py`: `python3 -m jarvis` çalıştırma noktası
- `tests/`: Asistan ve hesap makinesi testleri

## Başlatma ve kurulum

Python 3.10 veya üzeri yeterlidir; harici paket gerekmez. Ayrıntılar için
[install.md](./install.md) dosyasına bakın.

```bash
./install.sh
./run.sh
```

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