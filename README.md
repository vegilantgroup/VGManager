# 🔐 VGManager – AES Şifrelemeli Terminal Tabanlı Şifre Yöneticisi v1.0

**VGManager**, AES-256 şifrelemesiyle korunan SQLite tabanlı, güvenli ve hızlı çalışan bir şifre yöneticisidir. Terminal üzerinden site, kullanıcı adı ve parola bilgilerini AES anahtarınız ile şifreleyerek saklar, şifre çözme işlemlerini de sadece doğru AES anahtarı ile yapar.

---

## ✨ Özellikler

- 🔒 AES-256 (CBC) şifreleme ve çözme
- 🛡️ AES şifresi olmadan veri görüntüleme imkânsız
- 🔍 Site adı, kullanıcı adı veya ID ile şifre arama
- ➕ Şifre ekleme
- 💾 SQLite3 veritabanı kullanımı
- 👨‍💻 Tamamen terminal üzerinden çalışır
- 📚 Türkçe ve sade menü
- 🌱 Tamamen açık kaynaklı, herhangi bir veri gönderimi sağlamaz!

---

## 💽 Gereksinimler

- Python 3.6+
- `pycryptodome` kütüphanesi

## 🔧 Kurulum (Python Virtual Environment)

Bu proje, güvenli bir ortamda çalışması için sanal Python ortamı (`venv`) kullanır. Aşağıdaki adımları takip ederek `myvenv` adlı bir sanal ortam oluşturabilir ve bağımlılıkları yükleyebilirsiniz.

### 1. Python Sanal Ortam Oluşturma

```bash
python3 -m venv myvenv

    Eğer sisteminizde python3 komutu yoksa python olarak da çalışabilir.
```
2. Sanal Ortamı Aktif Etme

  ~ macOS / Linux:
```bash
source myvenv/bin/activate
```
  ~ Windows (CMD):
```bash
myvenv\Scripts\activate.bat
```

  ~ Windows (PowerShell):
```bash
    myvenv\Scripts\Activate.ps1
```

Aktifleştirildiğinde terminalde (myvenv) etiketi görünmelidir.
-------
### **3. Gerekli Paketleri Yükleme**

```bash
pip install -r requirements.txt
```
### **🛡️ Projeyi Çalıştırma**

Sanal ortam aktifken aşağıdaki komut ile uygulamayı başlatabilirsiniz:
```bash
python vgmanager.py
```
