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

# ── Sidebar Filter ────────────────────────────────────────────────────────────
st.sidebar.title("🔍 Filter Data")

tahun_options = ['Semua'] + sorted(df['yr'].unique().tolist())
selected_tahun = st.sidebar.selectbox("Pilih Tahun", tahun_options)

musim_options = ['Semua'] + sorted(df['season'].unique().tolist())
selected_musim = st.sidebar.selectbox("Pilih Musim", musim_options)

bulan_options = ['Semua'] + month_order
selected_bulan = st.sidebar.selectbox("Pilih Bulan", bulan_options)

# ── Terapkan filter ───────────────────────────────────────────────────────────
filtered_df = df.copy()
if selected_tahun != 'Semua':
    filtered_df = filtered_df[filtered_df['yr'] == selected_tahun]
if selected_musim != 'Semua':
    filtered_df = filtered_df[filtered_df['season'] == selected_musim]
if selected_bulan != 'Semua':
    filtered_df = filtered_df[filtered_df['mnth'] == selected_bulan]

# ── Header ────────────────────────────────────────────────────────────────────
st.title("Dashboard Analisis Bike Sharing (2011–2012)")
st.markdown("---")

# ── Metric cards ──────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)
col1.metric("Total Peminjaman", f"{filtered_df['cnt'].sum():,}")
col2.metric("Rata-rata Harian", f"{filtered_df['cnt'].mean():,.0f}")
col3.metric("Total Hari", f"{len(filtered_df):,}")

st.markdown("---")

# ── Chart 1 ───────────────────────────────────────────────────────────────────
st.subheader("Pertanyaan 1: Rata-rata Peminjaman Sepeda per Musim")

seasonal_avg = filtered_df.groupby('season')['cnt'].mean().reset_index()
seasonal_avg.columns = ['Season', 'Avg_Rentals']
seasonal_avg = seasonal_avg.sort_values('Avg_Rentals', ascending=True)

if seasonal_avg.empty:
    st.warning("Tidak ada data untuk filter yang dipilih.")
else:
    fig1, ax1 = plt.subplots(figsize=(9, 5))
    ax1.barh(seasonal_avg['Season'], seasonal_avg['Avg_Rentals'], edgecolor='white', height=0.6)
    ax1.set_title('Rata-rata Peminjaman Sepeda Harian per Musim (2011–2012)')
    ax1.set_xlabel('Rata-rata Jumlah Peminjaman per Hari')
    ax1.set_ylabel('Musim')
    ax1.spines[['top', 'right']].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig1)

st.markdown("---")

# ── Chart 2 ───────────────────────────────────────────────────────────────────
st.subheader("Pertanyaan 2: Tren Peminjaman Bulanan 2011 vs 2012")

# Chart 2 selalu pakai full data agar kedua garis selalu tampil,
# tapi filter tahun tetap diterapkan bila dipilih
df_chart2 = df.copy()
if selected_tahun != 'Semua':
    df_chart2 = df_chart2[df_chart2['yr'] == selected_tahun]

monthly = df_chart2.groupby(['yr', 'mnth'])['cnt'].sum().reset_index()
monthly.columns = ['Tahun', 'Bulan', 'Total']
monthly = monthly.sort_values(['Tahun', 'Bulan']).reset_index(drop=True)

years_available = sorted(monthly['Tahun'].unique().tolist())

fig2, ax2 = plt.subplots(figsize=(11, 5))
markers = ['o', 's', '^']
for i, year in enumerate(years_available):
    data_year = monthly[monthly['Tahun'] == year].reset_index(drop=True)
    x = [month_order.index(b) for b in data_year['Bulan']]
    ax2.plot(x, data_year['Total'], marker=markers[i], label=year)

ax2.set_xticks(range(len(month_order)))
ax2.set_xticklabels(month_order)
ax2.set_title('Tren Total Peminjaman Sepeda Bulanan: 2011 vs 2012')
ax2.set_xlabel('Bulan')
ax2.set_ylabel('Total Peminjaman')
ax2.legend()
ax2.spines[['top', 'right']].set_visible(False)
plt.tight_layout()
st.pyplot(fig2)
