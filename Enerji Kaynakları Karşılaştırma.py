import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class EnerjiKarsilastirmaUygulamasi:
    def __init__(self, master):
        self.master = master
        self.master.title("Enerji Kaynakları Karşılaştırma")
        self.master.geometry("800x600")

        self.enerji_kaynaklari = ["Güneş", "Rüzgar", "Fosil Yakıtlar"]
        self.veriler = {kaynak: {"maliyet": 0, "cevresel_etki": 0} for kaynak in self.enerji_kaynaklari}

        self.create_widgets()

    def create_widgets(self):
        # Veri Giriş Bölümü
        input_frame = ttk.LabelFrame(self.master, text="Veri Girişi")
        input_frame.pack(padx=10, pady=10, fill="x")

        for i, kaynak in enumerate(self.enerji_kaynaklari):
            ttk.Label(input_frame, text=f"{kaynak}:").grid(row=i, column=0, padx=5, pady=5)
            ttk.Label(input_frame, text="Maliyet (TL/kWh):").grid(row=i, column=1, padx=5, pady=5)
            maliyet_entry = ttk.Entry(input_frame)
            maliyet_entry.grid(row=i, column=2, padx=5, pady=5)
            ttk.Label(input_frame, text="Çevresel Etki (CO2 kg/kWh):").grid(row=i, column=3, padx=5, pady=5)
            etki_entry = ttk.Entry(input_frame)
            etki_entry.grid(row=i, column=4, padx=5, pady=5)

            self.veriler[kaynak]["maliyet_entry"] = maliyet_entry
            self.veriler[kaynak]["etki_entry"] = etki_entry

        ttk.Button(input_frame, text="Hesapla ve Göster", command=self.hesapla_ve_goster).grid(row=len(self.enerji_kaynaklari), column=0, columnspan=5, pady=10)

        # Grafik Bölümü
        self.graph_frame = ttk.LabelFrame(self.master, text="Grafikler")
        self.graph_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Sonuç Bölümü
        self.sonuc_label = ttk.Label(self.master, text="")
        self.sonuc_label.pack(padx=10, pady=10)

    def hesapla_ve_goster(self):
        for kaynak in self.enerji_kaynaklari:
            try:
                self.veriler[kaynak]["maliyet"] = float(self.veriler[kaynak]["maliyet_entry"].get())
                self.veriler[kaynak]["cevresel_etki"] = float(self.veriler[kaynak]["etki_entry"].get())
            except ValueError:
                self.sonuc_label.config(text="Hata: Lütfen tüm alanlara geçerli sayısal değerler girin.")
                return

        self.grafikleri_ciz()
        self.sonuclari_goster()

    def grafikleri_ciz(self):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
        
        # Maliyet Grafiği
        maliyetler = [self.veriler[kaynak]["maliyet"] for kaynak in self.enerji_kaynaklari]
        ax1.bar(self.enerji_kaynaklari, maliyetler)
        ax1.set_title("Maliyet Karşılaştırması")
        ax1.set_ylabel("TL/kWh")
        ax1.tick_params(axis='x', rotation=45)

        # Çevresel Etki Grafiği
        etkiler = [self.veriler[kaynak]["cevresel_etki"] for kaynak in self.enerji_kaynaklari]
        ax2.bar(self.enerji_kaynaklari, etkiler)
        ax2.set_title("Çevresel Etki Karşılaştırması")
        ax2.set_ylabel("CO2 kg/kWh")
        ax2.tick_params(axis='x', rotation=45)

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def sonuclari_goster(self):
        en_ucuz = min(self.veriler, key=lambda x: self.veriler[x]["maliyet"])
        en_cevreci = min(self.veriler, key=lambda x: self.veriler[x]["cevresel_etki"])
        
        sonuc_metni = f"En Ekonomik Kaynak: {en_ucuz}\n"
        sonuc_metni += f"En Çevre Dostu Kaynak: {en_cevreci}"
        
        self.sonuc_label.config(text=sonuc_metni)

if __name__ == "__main__":
    root = tk.Tk()
    app = EnerjiKarsilastirmaUygulamasi(root)
    root.mainloop()