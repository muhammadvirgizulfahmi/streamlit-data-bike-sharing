import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/main_data.csv")
    df['yr'] = df['yr'].astype(str)
    month_order = ['Jan','Feb','Mar','Apr','Mei','Jun','Jul','Agu','Sep','Okt','Nov','Des']
    df['mnth'] = pd.Categorical(df['mnth'], categories=month_order, ordered=True)
    return df, month_order

df, month_order = load_data()

st.title("Dashboard Analisis Bike Sharing (2011–2012)")
st.markdown("---")

# ── Chart 1 ──────────────────────────────────────────────────────────────────
st.subheader("Pertanyaan 1: Rata-rata Peminjaman Sepeda per Musim")

seasonal_avg = df.groupby('season')['cnt'].mean().reset_index()
seasonal_avg.columns = ['Season', 'Avg_Rentals']
seasonal_avg = seasonal_avg.sort_values('Avg_Rentals', ascending=True)

fig1, ax1 = plt.subplots(figsize=(9, 5))
ax1.barh(seasonal_avg['Season'], seasonal_avg['Avg_Rentals'], edgecolor='white', height=0.6)
ax1.set_title('Rata-rata Peminjaman Sepeda Harian per Musim (2011–2012)')
ax1.set_xlabel('Rata-rata Jumlah Peminjaman per Hari')
ax1.set_ylabel('Musim')
ax1.spines[['top', 'right']].set_visible(False)
plt.tight_layout()
st.pyplot(fig1)

st.markdown("---")

# ── Chart 2 ──────────────────────────────────────────────────────────────────
st.subheader("Pertanyaan 2: Tren Peminjaman Bulanan 2011 vs 2012")

monthly = df.groupby(['yr', 'mnth'])['cnt'].sum().reset_index()
monthly.columns = ['Tahun', 'Bulan', 'Total']
monthly = monthly.sort_values(['Tahun', 'Bulan']).reset_index(drop=True)

df_2011 = monthly[monthly['Tahun'] == '2011'].reset_index(drop=True)
df_2012 = monthly[monthly['Tahun'] == '2012'].reset_index(drop=True)

x = range(len(month_order))

fig2, ax2 = plt.subplots(figsize=(11, 5))
ax2.plot(x, df_2011['Total'], marker='o', label='2011')
ax2.plot(x, df_2012['Total'], marker='s', label='2012')
ax2.set_xticks(list(x))
ax2.set_xticklabels(month_order)
ax2.set_title('Tren Total Peminjaman Sepeda Bulanan: 2011 vs 2012')
ax2.set_xlabel('Bulan')
ax2.set_ylabel('Total Peminjaman')
ax2.legend()
ax2.spines[['top', 'right']].set_visible(False)
plt.tight_layout()
st.pyplot(fig2)
