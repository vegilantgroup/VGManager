import sqlite3
from getpass import getpass
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
import base64
import hashlib
import os
import sys

VERITABANI_ADI = "sifre_kayitlari.db"

# AES yardımcıları
def doldur(metin):
    return metin + (16 - len(metin) % 16) * chr(16 - len(metin) % 16)

def bosalt(metin):
    return metin[:-ord(metin[len(metin)-1:])]

def sifre_cozucu(anahtar, iv):
    return AES.new(anahtar, AES.MODE_CBC, iv)

def anahtar_hashle(parola):
    return hashlib.sha256(parola.encode()).digest()

def sifrele(metin, anahtar):
    metin = doldur(metin)
    iv = get_random_bytes(16)
    sifreleyici = sifre_cozucu(anahtar, iv)
    sifreli = sifreleyici.encrypt(metin.encode("utf-8", errors="ignore"))
    return base64.b64encode(iv + sifreli).decode()

def cozumle(sifreli_metin, anahtar):
    try:
        veriler = base64.b64decode(sifreli_metin)
        iv = veriler[:16]
        sifreleyici = sifre_cozucu(anahtar, iv)
        cozumlenmis = sifreleyici.decrypt(veriler[16:])
        return bosalt(cozumlenmis.decode("utf-8", errors="ignore"))
    except:
        return None  # AES anahtarı yanlışsa çözümleme başarısız olur

def veritabani_olustur():
    baglanti = sqlite3.connect(VERITABANI_ADI)
    imlec = baglanti.cursor()
    imlec.execute("""
        CREATE TABLE IF NOT EXISTS sifreler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            site TEXT NOT NULL,
            kullanici_adi TEXT NOT NULL,
            sifre TEXT NOT NULL
        )
    """)
    baglanti.commit()
    baglanti.close()

def aes_anahtari_al():
    print("🔐 AES şifrenizi giriniz (veri çözümleme için zorunlu!!):")
    parola = getpass("Parola: ")
    if not parola:
        print("❌ Şifre boş olamaz!")
        sys.exit(1)
    return anahtar_hashle(parola)

def sifre_ekle(anahtar):
    site = input("Site adı: ")
    kullanici_adi = input("Kullanıcı adı: ")
    sifre = getpass("Şifre: ")

    try:
        site_enc = sifrele(site, anahtar)
        kullanici_enc = sifrele(kullanici_adi, anahtar)
        sifre_enc = sifrele(sifre, anahtar)

        baglanti = sqlite3.connect(VERITABANI_ADI)
        imlec = baglanti.cursor()
        imlec.execute("INSERT INTO sifreler (site, kullanici_adi, sifre) VALUES (?, ?, ?)",
                      (site_enc, kullanici_enc, sifre_enc))
        baglanti.commit()
        baglanti.close()
        print("✔ Kayıt başarıyla eklendi.")
    except Exception as hata:
        print("❌ Hata:", hata)

def sifre_ara(anahtar):
    print("🔍 Arama: [1] Site adı ~ [2] Kullanıcı adı ~ [3] ID")
    secim = input("Seçim: ")

    baglanti = sqlite3.connect(VERITABANI_ADI)
    imlec = baglanti.cursor()

    try:
        if secim == "1":
            aranan = input("Site adı: ")
            imlec.execute("SELECT * FROM sifreler")
            for satir in imlec.fetchall():
                cozumlu_site = cozumle(satir[1], anahtar)
                if cozumlu_site and aranan.lower() in cozumlu_site.lower():
                    print(f"\nID: {satir[0]}")
                    print("Site:", cozumlu_site)
                    print("Kullanıcı:", cozumle(satir[2], anahtar))
                    print("Şifre:", cozumle(satir[3], anahtar))

        elif secim == "2":
            aranan = input("Kullanıcı adı: ")
            imlec.execute("SELECT * FROM sifreler")
            for satir in imlec.fetchall():
                cozumlu_kullanici = cozumle(satir[2], anahtar)
                if cozumlu_kullanici and aranan.lower() in cozumlu_kullanici.lower():
                    print(f"\nID: {satir[0]}")
                    print("Site:", cozumle(satir[1], anahtar))
                    print("Kullanıcı:", cozumlu_kullanici)
                    print("Şifre:", cozumle(satir[3], anahtar))

        elif secim == "3":
            try:
                aranan_id = int(input("ID: "))
                imlec.execute("SELECT * FROM sifreler WHERE id=?", (aranan_id,))
                satir = imlec.fetchone()
                if satir:
                    print("\n--- Kayıt ---")
                    print("Site:", cozumle(satir[1], anahtar))
                    print("Kullanıcı:", cozumle(satir[2], anahtar))
                    print("Şifre:", cozumle(satir[3], anahtar))
                else:
                    print("Kayıt bulunamadı.")
            except ValueError:
                print("❌ Geçersiz ID.")
        else:
            print("❌ Geçersiz seçim.")
    except Exception as hata:
        print("❌ AES anahtar hatalı olabilir veya veri bozuk.")
    finally:
        baglanti.close()

def ana_menu():
    veritabani_olustur()
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

    print("🛡️ VGManager v1.0 - Gelişmiş Şifre Yöneticisi")
    anahtar = aes_anahtari_al()

    while True:
        print("\n[1] Şifre Ekle")
        print("[2] Şifre Ara")
        print("[3] Çıkış")
        secim = input("Seçiminiz: ")

        if secim == "1":
            sifre_ekle(anahtar)
        elif secim == "2":
            sifre_ara(anahtar)
        elif secim == "3":
            print("Çıkılıyor...")
            break
        else:
            print("❌ Geçersiz seçim!")

if __name__ == "__main__":
    ana_menu()
