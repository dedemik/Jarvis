# Kurulum ve çalıştırma

## Gereksinimler

- Python 3.10 veya üzeri
- Harici Python paketi gerekmez; notlar için Python ile gelen SQLite kullanılır

## Kurulum

Depoyu klonladıktan sonra proje dizinine gir:

```bash
cd Jarvis
```

Kurulum betiği `.venv` sanal ortamını oluşturur ve `requirements.txt`
dosyasındaki paketleri yükler:

```bash
./install.sh
```

## Asistanı başlatma

```bash
./run.sh
```

İstersen sanal ortamı etkinleştirip uygulamayı Python modülü olarak da
başlatabilirsin:

```bash
source .venv/bin/activate
python -m jarvis
```

`yardım` komutuyla komut listesini görebilir, `çıkış` yazarak
asistanı kapatabilirsin. Not eklemek için `not ekle <metin>`, listelemek için
`notlar`, bir notu silmek için `not sil <numara>` komutunu kullan.

Hatırlatıcı oluşturmak için `hatırlatıcı ekle YYYY-AA-GG SS:DD <açıklama>`
biçimini kullan; örneğin `hatırlatıcı ekle 2026-11-05 10:00 Doktor randevusu`.
Hatırlatıcılar bilgisayarın yerel saatini kullanır ve zamanı gelenler başlangıçta
ve sonraki komutlarda gösterilir. Komut beklerken anında uyarı verilmez.

Notlar, yapılacaklar ve hatırlatıcılar `~/.jarvis/jarvis.sqlite3` dosyasında
kalıcı olarak saklanır.

## Testleri çalıştırma

```bash
python3 -m unittest discover -s tests -v
```
