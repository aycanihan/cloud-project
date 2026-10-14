# Bu dosya, gerçek veriyi bulana kadar çalışmak için
# gerçeğe benzeyen bir sunucu kullanım verisi üretir.
import numpy as np
import pandas as pd

np.random.seed(42)  # Her çalıştırmada aynı veriyi üretmesi için

# 90 günlük, saat saat zaman listesi
zamanlar = pd.date_range(start="2026-01-01", periods=90 * 24, freq="h")

saat = np.array(zamanlar.hour)
hafta_gunu = np.array(zamanlar.dayofweek)  # 0 = Pazartesi, 6 = Pazar

# Günlük örüntü: gece düşük, öğlen ve akşam yüksek
gunluk = 25 + 30 * np.sin((saat - 6) / 24 * 2 * np.pi).clip(0) + 15 * ((saat >= 19) & (saat <= 22))

# Hafta sonu trafik biraz daha düşük
hafta_sonu = np.where(hafta_gunu >= 5, -8, 0)

# Şirket büyüdükçe kullanım yavaşça artıyor
trend = np.linspace(0, 8, len(zamanlar))

# Gerçek hayattaki gibi küçük rastgele dalgalanmalar
gurultu = np.random.normal(0, 4, len(zamanlar))

kullanim = (gunluk + hafta_sonu + trend + gurultu).clip(2, 100)

veri = pd.DataFrame({"zaman": zamanlar, "cpu_kullanim": kullanim.round(1)})
veri.to_csv("sunucu_verisi.csv", index=False)

print("Veri oluşturuldu:", len(veri), "satır")
print(veri.head(10))