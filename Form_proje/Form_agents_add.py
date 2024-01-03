import tkinter as tk
from datetime import datetime
import ipaddress

def ip_adresini_ekle():
    ip_adresi = ip_textbox.get()
    if ip_adresi:
        try:
            # Giriş kutusundan alınan değeri bir IP adresi olarak kontrol et
            ipaddress.IPv4Address(ip_adresi)

            # agents.txt dosyasını oku
            with open("agents.txt", "r") as dosya:
                # Dosyadaki mevcut IP adreslerini bir liste olarak al
                mevcut_ip_adresleri = dosya.read().splitlines()

            # Yeni IP adresini listeye ekle
            mevcut_ip_adresleri.append(ip_adresi)

            # Listeyi dosyaya yaz
            with open("agents.txt", "w") as dosya:
                dosya.write("\n".join(mevcut_ip_adresleri))

            # Başarılı ekleme mesajını göster
            sonuc_label.config(text=f"IP adresi eklendi: {ip_adresi}")

            # Listbox'ı güncelle
            guncelle_listbox()
        except ipaddress.AddressValueError:
            # IP adresi değilse hata mesajı göster
            sonuc_label.config(text="Geçerli bir IP adresi girin.")
        except Exception as hata:
            # Diğer hatalar için genel hata mesajı göster
            sonuc_label.config(text=f"Hata oluştu: {hata}")
    else:
        sonuc_label.config(text="Lütfen bir IP adresi girin.")

def guncelle_listbox():
    # Listbox'ı temizle
    listbox.delete(0, tk.END)
    
    try:
        # agents.txt dosyasını oku ve Listbox'a ekle
        with open("agents.txt", "r") as dosya:
            for line in dosya:
                listbox.insert(tk.END, line.strip())
    except FileNotFoundError:
        dosya = open("agents.txt", 'w')
        print("Dosya oluşturuldu.")
        
    

def sil_secilen():
    # Seçilen IP adresini Listbox'tan kaldır
    secilen_index = listbox.curselection()
    if secilen_index:
        secilen_index = int(secilen_index[0])
        with open("agents.txt", "r") as dosya:
            mevcut_ip_adresleri = dosya.read().splitlines()

        # Seçilen IP adresini listeden kaldır
        silinecek_ip = mevcut_ip_adresleri.pop(secilen_index)

        # Listeyi dosyaya yaz
        with open("agents.txt", "w") as dosya:
            dosya.write("\n".join(mevcut_ip_adresleri))

        sonuc_label.config(text=f"IP adresi silindi: {silinecek_ip}")

        # Listbox'ı güncelle
        guncelle_listbox()

# Ana pencereyi oluştur
pencere = tk.Tk()
pencere.title("IP Adresi Kaydedici")
window_height = 530
window_width = 800

def center_screen():
    """ gets the coordinates of the center of the screen """
    global screen_height, screen_width, x_cordinate, y_cordinate
    screen_width = pencere.winfo_screenwidth()
    screen_height = pencere.winfo_screenheight()
        # Coordinates of the upper left corner of the window to make the window appear in the center
    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))
    pencere.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

center_screen()

# IP adresi için metin kutusu
ip_textbox = tk.Entry(pencere)
ip_textbox.pack(pady=10)

# Buton
ekle_button = tk.Button(pencere, text="IP Adresini Ekle", command=ip_adresini_ekle)
ekle_button.pack(pady=10)

# Sil butonu
sil_button = tk.Button(pencere, text="Seçileni Sil", command=sil_secilen)
sil_button.pack(pady=10)

# Sonuçları gösteren etiket
sonuc_label = tk.Label(pencere, text="")
sonuc_label.pack(pady=10)

# Listbox
listbox = tk.Listbox(pencere)
listbox.pack(pady=10)

# agents.txt dosyasındaki IP adreslerini Listbox'a ekle
guncelle_listbox()

# Pencereyi başlat
pencere.mainloop()
