# Geliştirme ilerlemesi

## Kapsam

- [x] Hedef kullanım alanları belirlendi: temel çevrimdışı yardımcı, günlük
      üretkenlik, sesli komutlar, yapay zekâ ve web araması.
- [x] Temel CLI ve standart kütüphane ile çalışan özellikler korunacak; ek
      paketler yalnızca ilgili özellik seçilip uygulandığında eklenecek.
- [x] Üretkenlik özellikleri sıraya kondu: notlar, yapılacaklar, hatırlatıcılar.
- [x] Kalıcı veri saklama için Python standart kütüphanesindeki SQLite seçildi.
- [x] Hatırlatıcılar yerel `YYYY-AA-GG SS:DD` saatiyle tek seferlik olacak;
      başlangıçta ve komutlardan sonra kontrol edilecek.
- [x] İlk arayüz masaüstü Tkinter sohbet penceresi; LLM bağlantısı sonraya
      bırakıldı.

## Tamamlandı

- [x] Türkçe terminal arayüzü ve komut döngüsü
- [x] Yardım, saat, tarih ve çıkış komutları
- [x] Temel aritmetik için güvenli hesaplama
- [x] Asistan, hesap makinesi ve CLI modüllerinin ayrılması
- [x] `python3 -m jarvis` giriş noktası
- [x] Testlerin `tests/` dizininde gruplanması
- [x] Kurulum, mimari ve geliştirme belgeleri
- [x] Ses, yapay zekâ, web ve görsel özellikleri için kütüphane adaylarının
      ilk değerlendirmesi
- [x] SQLite ile not ekleme, listeleme ve silme komutları
- [x] SQLite ile yapılacak ekleme, listeleme, tamamlandı işaretleme ve silme
- [x] SQLite ile hatırlatıcı ekleme, listeleme, silme ve bir kez bildirim
- [x] Mevcut komutları kullanan ChatGPT tarzı Tkinter sohbet arayüzü

## Değerlendirme sonuçları

- Ses girişi: [sounddevice](https://python-sounddevice.readthedocs.io/) Linux,
  macOS ve Windows'u destekler; PortAudio/NumPy gereksinimleri nedeniyle
  isteğe bağlı kurulmalıdır. Alternatif: PyAudio.
- Konuşmayı yazıya çevirme: [faster-whisper](https://github.com/SYSTRAN/faster-whisper)
  yerel çalışabilir ve Python 3.10+ kapsamına uyar; model indirme, disk alanı
  ve CPU/GPU maliyeti vardır. Türkçe doğruluğu hedef cihazda denenmelidir.
- Metni seslendirme: [pyttsx3](https://pyttsx3.readthedocs.io/) çevrimdışı
  sistem konuşma motorlarını kullanır; Türkçe seslerin bulunması işletim
  sistemine bağlıdır. Sesli yanıt gereksinimi netleşince hedef sistemde
  doğrulanmalı.
- Bulut LLM: tek sağlayıcıyla başlamak için o sağlayıcının resmi SDK'sı daha
  yalın; [LiteLLM](https://docs.litellm.ai/docs/) birden fazla sağlayıcı
  gerçekten gerekirse değerlendirilmeli. [huggingface_hub](https://huggingface.co/docs/huggingface_hub/guides/inference)
  Hugging Face Inference Providers/Endpoints için uygun istemcidir.
- API anahtarı: entegrasyon yapılırsa sağlayıcıya ait anahtar ortam
  değişkeninden okunmalı; koda, test verisine veya depoya yazılmamalı. Sağlayıcı
  seçimi henüz yapılmadı.
- Yerel LLM: [llama.cpp](https://github.com/ggerganov/llama.cpp) ve
  [llama-cpp-python](https://github.com/abetlen/llama-cpp-python) mahremiyet ve
  çevrimdışı çalışma için seçeneklerdir; model boyutu, donanım ve derleme
  gereksinimleri nedeniyle temel kurulumdan ayrı tutulmalı.
- Ajan/çok adımlı görevler: [smolagents](https://github.com/huggingface/smolagents)
  daha hafif başlangıç, [LangGraph](https://docs.langchain.com/oss/python/langgraph/overview)
  durumlu iş akışları için adaydır. İlk sürümde gereksiz; araç çalıştırma
  kapsamı ve izinleri tasarlanmadan eklenmemeli.
- Web araması: [ddgs](https://github.com/deedy5/ddgs) hızlı bir istemci
  seçeneğidir; sorgular üçüncü taraf arama servislerine gidebilir ve servis
  davranışları değişebilir. [SearXNG](https://docs.searxng.org/) kendi
  sunucusunu işletme ve daha fazla kontrol karşılığında ek operasyon yükü getirir.
- Sayfa alma/çıkarma: basit istekler için standart kütüphanedeki `urllib`
  yeterli olabilir; zaman aşımı ve istemci ergonomisi gerektiğinde
  [httpx](https://www.python-httpx.org/) değerlendirilmeli.
  [trafilatura](https://github.com/adbar/trafilatura) ana metin ve metadata
  çıkarmada yararlı, fakat ek bağımlılıktır. Sayfa içeriği güvenilmeyen girdi
  sayılmalı.
- JavaScript sayfaları: [Playwright](https://playwright.dev/python/docs/intro)
  yalnızca normal HTTP alma yetersiz kaldığında kullanılmalı; tarayıcı
  ikilileri ve ek kurulum maliyeti vardır.
- Yerel model/görsel üretimi: [Transformers](https://huggingface.co/docs/transformers/index),
  PyTorch ve [Diffusers](https://huggingface.co/docs/diffusers/index) kapsamlı
  ML altyapısı ve ciddi disk/donanım maliyeti getirir; şimdilik ertelenmeli.
- Görsel işleme: [Pillow](https://pillow.readthedocs.io/en/stable/) temel
  görsel okuma/dönüştürme için uygun bir isteğe bağlı bağımlılıktır.
- HTTP API: [FastAPI](https://fastapi.tiangolo.com/) yalnızca Jarvis'in başka
  istemcilere HTTP üzerinden sunulması istenirse eklenmeli; mevcut CLI kapsamı
  için gerekli değil.

## Sonraki adımlar

- [ ] Sesli kullanımın hedef işletim sistemi, Türkçe konuşma girdisi ve yanıt
      beklentisini belirle; sonra isteğe bağlı paketleri seç
- [ ] Yapay zekâ sağlayıcısını ve bulut/yerel çalışma tercihini belirle
- [ ] Web araması için üçüncü taraf servis veya kendi SearXNG sunucusu tercihini
      belirle
- [ ] Seçilen özellikleri bağımsız modüller halinde uygula ve `tests/` altında
      test et

Bu değerlendirmeler teknoloji seçimine yardımcı olmak içindir; sesli kullanım,
yapay zekâ entegrasyonu, web araması, görsel işleme veya HTTP API henüz
uygulanmamıştır. SQLite Python standart kütüphanesinin parçasıdır; projeye yeni
harici bağımlılık eklenmemiştir.
