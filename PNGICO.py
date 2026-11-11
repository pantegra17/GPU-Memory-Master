import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import requests
from io import BytesIO
import os

class PNGICOApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PNGICO - Yüksek Kaliteli ICO Dönüştürücü")
        self.root.geometry("500x350")
        self.root.resizable(False, False)

        self.img_path = None
        self.img_data = None

        # Arayüz Elemanları
        tk.Label(root, text="PNGICO", font=("Arial", 20, "bold")).pack(pady=10)
        
        # URL Girişi
        tk.Label(root, text="Resim URL'si (Opsiyonel):").pack()
        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.pack(pady=5)

        # Butonlar
        tk.Button(root, text="Bilgisayardan PNG Seç", command=self.load_from_pc, bg="#3498db", fg="white", width=25).pack(pady=5)
        tk.Button(root, text="URL'den Resmi Getir", command=self.load_from_url, bg="#9b59b6", fg="white", width=25).pack(pady=5)
        
        self.status_label = tk.Label(root, text="Lütfen bir dosya seçin veya URL girin", fg="gray")
        self.status_label.pack(pady=20)

        tk.Button(root, text="ICO Olarak Kaydet", command=self.save_as_ico, bg="#2ecc71", fg="white", font=("Arial", 10, "bold"), width=30).pack(pady=10)

    def load_from_pc(self):
        file_path = filedialog.askopenfilename(filetypes=[("PNG Dosyaları", "*.png")])
        if file_path:
            self.img_path = file_path
            self.img_data = Image.open(file_path)
            self.status_label.config(text=f"Seçildi: {os.path.basename(file_path)}", fg="green")
            self.url_entry.delete(0, tk.END)

    def load_from_url(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Hata", "Lütfen geçerli bir URL girin.")
            return
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            self.img_data = Image.open(BytesIO(response.content))
            self.status_label.config(text="URL'deki resim başarıyla yüklendi!", fg="green")
            self.img_path = "url_image.png"
        except Exception as e:
            messagebox.showerror("Hata", f"Resim indirilemedi: {e}")

    def save_as_ico(self):
        if self.img_data is None:
            messagebox.showwarning("Uyarı", "Önce bir resim seçmelisiniz!")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".ico", filetypes=[("ICO Dosyası", "*.ico")])
        
        if save_path:
            try:
                # Çözünürlük bozulmaması için orijinal boyutu koruyarak kaydetme
                # ICO formatı standart olarak 256x256 boyuta kadar destekler.
                icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
                
                # Resim RGBA değilse dönüştür (şeffaflık koruması için)
                if self.img_data.mode != 'RGBA':
                    self.img_data = self.img_data.convert('RGBA')
                
                self.img_data.save(save_path, format='ICO', sizes=icon_sizes)
                messagebox.showinfo("Başarılı", f"Dosya başarıyla kaydedildi:\n{save_path}")
            except Exception as e:
                messagebox.showerror("Hata", f"Kaydedilirken bir sorun oluştu: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PNGICOApp(root)
    root.mainloop()