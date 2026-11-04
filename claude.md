# Claude için proje notları

## Proje

Jarvis, Python 3.10 veya üzeriyle çalışan, Türkçe komut satırı asistanıdır.
Şu an yalnızca Python standart kütüphanesini kullanır.

## Mimari

- `jarvis/assistant.py`: Komut normalleştirme ve asistan davranışı
- `jarvis/calculator.py`: Güvenli, temel aritmetik değerlendirmesi
- `jarvis/cli.py`: Terminal etkileşimi ve ana döngü
- `jarvis/__main__.py`: `python3 -m jarvis` giriş noktası
- `tests/`: `unittest` testleri

Modül sorumluluklarını ayrı tut. Yeni bir komut eklerken davranışı
`JarvisAssistant.handle_command` içinde tanımla ve `tests/` altında test et.
Terminal girdisi/çıktısıyla ilgili değişiklikleri `cli.py` içinde tut.

## Geliştirme

- Çalıştır: `python3 -m jarvis`
- Test et: `python3 -m unittest discover -s tests -v`
- Harici bağımlılık eklemeden önce gerekçesini değerlendir.
- Kullanıcıya görünen yanıtları Türkçe tut.
