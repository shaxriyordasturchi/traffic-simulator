import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Parametrlar
kanallar_soni = 4
kanal_sigimi = 10  # Gbps
ocdma_samaradorligi = 0.8
umumiy_sigim = kanallar_soni * kanal_sigimi
samarali_sigim = umumiy_sigim * ocdma_samaradorligi

kategoriya_traffic = {
    'Uy': (0.3, 1.2),
    'Ofis': (1.0, 2.5),
    'Korxona': (2.0, 4.0)
}

def prognoz_kunlik_oylik(trafik):
    kunlik = np.sum(trafik) * 24
    oylik = kunlik * 30
    return kunlik, oylik

def bugungi_trafik(trafik):
    soat = datetime.now().hour
    return np.sum(trafik) * soat

# --- Streamlit UI ---
st.set_page_config(layout="wide")
st.title("🔌 WDM/OCDMA PON Trafik Monitoring Paneli")

col1, col2 = st.columns(2)

with col1:
    kategoriya = st.radio("📶 Foydalanuvchi kategoriyasi", ['Uy', 'Ofis', 'Korxona'])
with col2:
    foydalanuvchi_soni = st.slider("👥 Foydalanuvchilar soni", 1, 20, 10)

min_t, max_t = kategoriya_traffic[kategoriya]
trafik = np.random.uniform(min_t, max_t, foydalanuvchi_soni)
umumiy = np.sum(trafik)
yuk = umumiy / samarali_sigim
bugun = bugungi_trafik(trafik)
kunlik, oylik = prognoz_kunlik_oylik(trafik)

# --- Grafiklar ---
fig, (ax_bar, ax_pie, ax_trend) = plt.subplots(1, 3, figsize=(18, 6))
plt.subplots_adjust(wspace=0.4)

# Bar chart
ax_bar.bar(range(1, foydalanuvchi_soni + 1), trafik, color='skyblue')
ax_bar.axhline(y=kanal_sigimi, color='red', linestyle='--', label='Kanal chegarasi')
ax_bar.set_title(f"{kategoriya} foydalanuvchilari trafik prognozi")
ax_bar.set_xlabel("Foydalanuvchilar")
ax_bar.set_ylabel("Soatlik trafik (Gbps)")
ax_bar.grid(True)
ax_bar.legend()

if foydalanuvchi_soni > 15:
    ax_bar.text(0.5, 0.97, "⚠️ Foydalanuvchi soni 20 dan oshgan!", transform=ax_bar.transAxes,
                fontsize=12, color='red', ha='center', bbox=dict(facecolor='white', alpha=0.8))
if yuk > 1.0:
    ax_bar.text(0.5, 0.92, "⚠️ Yuklama limitdan oshgan!", transform=ax_bar.transAxes,
                fontsize=12, color='darkred', ha='center', bbox=dict(facecolor='white', alpha=0.8))

ax_bar.text(0.98, 0.95, f"🕒 Bugungi: {bugun:.2f} Gbps", transform=ax_bar.transAxes,
            fontsize=10, va='top', ha='right', bbox=dict(facecolor='white', alpha=0.6))
ax_bar.text(0.98, 0.88, f"📅 Kunlik: {kunlik:.2f} Gbps", transform=ax_bar.transAxes,
            fontsize=10, va='top', ha='right', bbox=dict(facecolor='white', alpha=0.6))
ax_bar.text(0.98, 0.81, f"🗓 Oylik: {oylik:.2f} Gbps", transform=ax_bar.transAxes,
            fontsize=10, va='top', ha='right', bbox=dict(facecolor='white', alpha=0.6))

# Pie chart
labels = ['Trafik', 'Bo‘sh sig‘im']
values = [umumiy, max(samarali_sigim - umumiy, 0)]
colors = ['lightcoral', 'lightgreen'] if yuk <= 1 else ['red', 'grey']
ax_pie.pie(values, labels=labels, autopct='%.1f%%', colors=colors, startangle=140)
ax_pie.set_title("Tizim yuklanish holati")

# Trend chizma
foydalanuvchi_range = np.arange(1, 20)
trend_yuklama = []
for n in foydalanuvchi_range:
    t = np.random.uniform(min_t, max_t, n)
    trend_yuklama.append(np.sum(t) / samarali_sigim)
ax_trend.plot(foydalanuvchi_range, trend_yuklama, color='purple')
ax_trend.axhline(y=1.0, linestyle='--', color='red')
ax_trend.set_title("Yuklama tendensiyasi")
ax_trend.set_xlabel("Foydalanuvchilar soni")
ax_trend.set_ylabel("Yuklama (n/samarali sig‘im)")
ax_trend.grid(True)

# Grafikni chiqarish
st.pyplot(fig)
