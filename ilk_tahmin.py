# İlk tahmin: Prophet ile önümüzdeki 3 günün sunucu kullanımını tahmin et
import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet

# 1) Veriyi oku
veri = pd.read_csv("sunucu_verisi.csv")

# 2) Prophet sütun adlarını "ds" (zaman) ve "y" (değer) olarak ister
veri = veri.rename(columns={"zaman": "ds", "cpu_kullanim": "y"})
veri["ds"] = pd.to_datetime(veri["ds"])

# 3) Modeli oluştur ve geçmiş veriyle eğit
model = Prophet(daily_seasonality=True, weekly_seasonality=True)
model.fit(veri)

# 4) Önümüzdeki 72 saati (3 gün) tahmin et
gelecek = model.make_future_dataframe(periods=72, freq="h")
tahmin = model.predict(gelecek)

# 5) Son tahminleri ekrana yaz
#    yhat = tahmin, yhat_lower / yhat_upper = alt ve üst sınır
print(tahmin[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(12).set_index("ds").round(1))

# 6) Grafiği çiz: son 7 gün gerçek veri + 3 günlük tahmin
son = tahmin.tail(72 + 7 * 24)
gercek = veri.tail(7 * 24)

plt.figure(figsize=(12, 5))
plt.plot(gercek["ds"], gercek["y"], label="Gerçek kullanım", color="black")
plt.plot(son["ds"], son["yhat"], label="Tahmin", color="tab:blue")
plt.fill_between(son["ds"], son["yhat_lower"], son["yhat_upper"],
                 color="tab:blue", alpha=0.2, label="Tahmin aralığı")
plt.axvline(veri["ds"].max(), color="red", linestyle="--", label="Bugün")
plt.title("Sunucu CPU Kullanımı: Geçmiş ve 3 Günlük Tahmin")
plt.ylabel("CPU kullanımı (%)")
plt.legend()
plt.tight_layout()
plt.savefig("ilk_tahmin.png")
print("Grafik kaydedildi: ilk_tahmin.png")