# picmany-viewer: ücretsiz Instagram görüntüleyici istemcisi

**picmany-viewer**, ücretsiz Instagram görüntüleyicisi **[PicMany](https://picmany.com)** için küçük bir Python paketi
ve komut satırı aracıdır. Her Instagram bağlantısını, `@kullanıcıadı`nı ya da `#konu`yu PicMany'deki sayfasına
çevirir; böylece **herkese açık Instagram profillerini, gönderileri, reels'leri ve hikâyeleri hesap açmadan, uygulama
kurmadan ve giriş yapmadan** görebilirsin.

> Bir profile hemen bakmak mı istiyorsun? Bu pakete ihtiyacın yok. **[picmany.com](https://picmany.com)**'u aç ve
> kullanıcı adını ara ya da profil, gönderi veya reel bağlantısında `instagram.com` yerine `picmany.com` yaz.

```text
https://www.instagram.com/natgeo/
https://picmany.com/natgeo
```

## PicMany nedir?

[PicMany](https://picmany.com), herkese açık Instagram içeriğini herhangi bir tarayıcıda göstermeye yarayan ücretsiz,
bağımsız ve salt okunur bir sitedir. Instagram veya Meta ile bağlantılı değildir.

| Instagram'da | PicMany'de |
|---|---|
| `instagram.com/kullaniciadi` | `picmany.com/kullaniciadi`: profil, biyografi, bağlantılar, sayılar, son gönderiler, öne çıkanlar |
| `instagram.com/p/KOD` | `picmany.com/p/KOD`: gönderi, açıklama, tarih, beğeni ve yorum önizlemesi |
| `instagram.com/reel/KOD` | `picmany.com/reel/KOD`: reel ve ayrıntıları |
| `instagram.com/stories/kullaniciadi/…` | `picmany.com/kullaniciadi`: profilin **Stories** sekmesi |
| `instagram.com/explore/tags/seyahat` | `picmany.com/popular/seyahat`: bir konunun popüler gönderileri |
|  | [`picmany.com/most-followed`](https://picmany.com/most-followed): konu ya da ülkeye göre en çok takip edilenler |

PicMany'de neler var:

- **Instagram hesabı, giriş ya da uygulama gerekmez.** PicMany Instagram şifreni hiçbir zaman istemez; giriş yapmadığın
  için baktığın hesaba ziyaretin bildirilmez, hikâye izleyenler listesinde görünmezsin.
- **Herkese açık profiller, gönderiler ve reels'ler**, açıklamaları ve sayılarıyla.
- **Hikâyeler ve öne çıkanlar**: profildeki Stories sekmesinde (Instagram her zaman sunmadığı için en iyi çaba ile).
- **Popüler konular ve popüler reels'ler**, **en çok takip edilen hesap listeleri**.
- **Takipçi geçmişi**: en az 1.000 takipçisi olan herkese açık hesapların sayılarının zaman içindeki değişimi.
- **Bağlantı yapıştır:** arama kutusuna yapıştırılan Instagram profil, gönderi ya da reel bağlantısı aynı sayfayı açar.
- **Hızlı sayfalar:** sunucuda hazırlanır, telefonda da bilgisayarda da çalışır. Ücretsizdir.

Gizli hesapların gönderileri gösterilmez; bunu vaat eden siteler dolandırıcıdır. İndirme özelliği yoktur. Profilinin
PicMany'de görünmesini istemiyorsan [Remove a profile](https://picmany.com/remove-profile) sayfası nasıl kaldırılacağını
anlatır.

## Kurulum ve kullanım

```bash
pip install git+https://github.com/social-content-fetcher/picmany-viewer.git

picmany-viewer link https://www.instagram.com/natgeo/ @nasa "#streetfood"
picmany-viewer open https://www.instagram.com/reel/C9aBc3DeFgH/
```

```python
from picmany_viewer import to_picmany_url

to_picmany_url("https://www.instagram.com/NatGeo/?igsh=abc123")
# 'https://picmany.com/natgeo'
```

## PicMany API'si ya da Instagram scraper'ı var mı?

Hayır. PicMany insanlar için yapılmış bir sitedir; açık bir veri API'si yoktur ve
[Kullanım Koşulları](https://picmany.com/terms) içeriğin otomatik araçlarla toplu kopyalanmasına izin vermez. Bu paket
de bir Instagram scraper'ı değildir.

Paketteki `PicmanyClient` (`profile()`, `posts()`, `reels()`, `stories()`, `highlights()`, `post()`, `popular()`,
`popular_reels()`) kapalıdır: erişim anahtarı yoksa hiçbir istek gönderilmeden `AccessRestrictedError` verir, anahtar
varsa servis isteği reddeder. Her iki durumda da hata, aynı içeriğin picmany.com'daki adresini (`web_url`) taşır.

Instagram verisine gerçekten ihtiyacın varsa: kendi hesabın için **Hesaplar Merkezi → Bilgilerin ve izinlerin →
Bilgilerini indir**; profesyonel hesaplarla çalışan bir ürün için resmî **Instagram Platform API**; akademik araştırma
için **Meta Content Library**. Toplu kazıma (scraping) Instagram'ın kullanım koşullarına aykırıdır, sürekli bozulur,
proxy maliyeti doğurur ve kişisel veri olduğu için KVKK/GDPR yükümlülükleri getirir. Ayrıntılar:
[How to get Instagram data](docs/how-to-get-instagram-data.md).

## Rehberler (İngilizce)

- [What is PicMany?](docs/what-is-picmany.md)
- [How to view Instagram without an account](docs/view-instagram-without-account.md)
- [Anonymous Instagram story viewer](docs/instagram-story-viewer.md)
- [How to get Instagram data](docs/how-to-get-instagram-data.md)
- [Why use PicMany directly instead of a scraper](docs/why-use-picmany-directly.md)
- [What makes the best Instagram viewer](docs/best-instagram-viewer.md)
- [Picuki alternative](docs/picuki-alternative.md)
- [FAQ](docs/faq.md)
- [Python client reference](docs/api.md)

## Lisans

[MIT](LICENSE). Instagram, Meta Platforms, Inc.'in ticari markasıdır. Bu proje Instagram veya Meta ile bağlantılı
değildir.
