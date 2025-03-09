# Dashboard Streamlit - Bike Sharing Analysis
# Nama: Farhan Maulana Pangestu
# ID Dicoding: mc487d5y1426

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime


st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"
)


@st.cache_data
def load_data():
    day_df = pd.read_csv('data/day.csv')
    hour_df = pd.read_csv('data/hour.csv')
    

    day_df['datetime'] = pd.to_datetime(day_df['dteday'])
    hour_df['datetime'] = pd.to_datetime(hour_df['dteday'])
    hour_df['time'] = hour_df['hr'].apply(lambda x: f"{x:02d}:00")
    

    season_dict = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    day_df['season_label'] = day_df['season'].map(season_dict)
    hour_df['season_label'] = hour_df['season'].map(season_dict)
    

    weather_dict = {1: 'Clear', 2: 'Mist', 3: 'Light Rain/Snow', 4: 'Heavy Rain/Snow'}
    day_df['weather_label'] = day_df['weathersit'].map(weather_dict)
    hour_df['weather_label'] = hour_df['weathersit'].map(weather_dict)
    

    workingday_dict = {0: 'Weekend/Holiday', 1: 'Workingday'}
    day_df['workingday_label'] = day_df['workingday'].map(workingday_dict)
    hour_df['workingday_label'] = hour_df['workingday'].map(workingday_dict)
    

    month_dict = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 
                  7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    day_df['month_label'] = day_df['mnth'].map(month_dict)
    hour_df['month_label'] = hour_df['mnth'].map(month_dict)
    
    return day_df, hour_df

day_df, hour_df = load_data()


st.sidebar.title("Bike Sharing Dashboard")
st.sidebar.image("https://img.freepik.com/free-vector/bike-sharing-abstract-concept-illustration_335657-3891.jpg", width=200)


st.sidebar.subheader("Filter Data")
min_date = day_df['datetime'].min().date()
max_date = day_df['datetime'].max().date()

start_date = st.sidebar.date_input("Start Date", min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("End Date", max_date, min_value=min_date, max_value=max_date)


filtered_day_df = day_df[(day_df['datetime'].dt.date >= start_date) & (day_df['datetime'].dt.date <= end_date)]
filtered_hour_df = hour_df[(hour_df['datetime'].dt.date >= start_date) & (hour_df['datetime'].dt.date <= end_date)]


st.sidebar.markdown("---")
st.sidebar.subheader("About")
st.sidebar.info("Dashboard ini dibuat untuk proyek akhir Dicoding - Belajar Analisis Data dengan Python.")
st.sidebar.markdown("---")


st.title("🚲 Bike Sharing Analysis Dashboard")
st.markdown("Analisis pola penggunaan layanan bike sharing berdasarkan berbagai faktor.")


st.header("Overview")
col1, col2, col3, col4 = st.columns(4)

total_rentals = filtered_day_df['cnt'].sum()
avg_daily_rentals = filtered_day_df['cnt'].mean()
max_daily_rentals = filtered_day_df['cnt'].max()
peak_day = filtered_day_df.loc[filtered_day_df['cnt'].idxmax()]['datetime'].strftime('%Y-%m-%d')

col1.metric("Total Rentals", f"{total_rentals:,}")
col2.metric("Avg. Daily Rentals", f"{avg_daily_rentals:.2f}")
col3.metric("Max Daily Rentals", f"{max_daily_rentals:,}")
col4.metric("Peak Day", peak_day)

st.markdown("---")


st.header("Analisis Berdasarkan Musim")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Total Peminjaman Sepeda per Musim")
    season_rentals = filtered_day_df.groupby('season_label')['cnt'].sum().reset_index()
    season_rentals = season_rentals.sort_values('cnt', ascending=False)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='season_label', y='cnt', data=season_rentals, palette='viridis', ax=ax)
    ax.set_xlabel('Musim')
    ax.set_ylabel('Total Peminjaman')
    ax.set_title('Total Peminjaman Sepeda per Musim')
    st.pyplot(fig)

with col2:
    st.subheader("Persentase Peminjaman Sepeda per Musim")
    season_rentals_pct = filtered_day_df.groupby('season_label')['cnt'].sum()
    total_rentals = season_rentals_pct.sum()
    season_rentals_pct = (season_rentals_pct / total_rentals * 100).round(2)
    
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(season_rentals_pct, labels=season_rentals_pct.index, autopct='%1.1f%%', 
           startangle=90, shadow=True, explode=[0.05]*len(season_rentals_pct))
    ax.set_title('Persentase Peminjaman Sepeda per Musim')
    st.pyplot(fig)

st.markdown("---")


st.header("Analisis Berdasarkan Kondisi Cuaca")

st.subheader("Distribusi Peminjaman Sepeda berdasarkan Kondisi Cuaca")
fig, ax = plt.subplots(figsize=(12, 6))
sns.boxplot(x='weather_label', y='cnt', data=filtered_day_df, palette='Set3', ax=ax)
ax.set_xlabel('Kondisi Cuaca')
ax.set_ylabel('Jumlah Peminjaman Harian')
ax.set_title('Distribusi Peminjaman Sepeda berdasarkan Kondisi Cuaca')
st.pyplot(fig)

weather_rentals = filtered_day_df.groupby('weather_label')['cnt'].agg(['mean', 'std', 'count']).reset_index()
weather_rentals.columns = ['Kondisi Cuaca', 'Rata-rata Peminjaman', 'Std Deviasi', 'Jumlah Hari']
weather_rentals = weather_rentals.sort_values('Rata-rata Peminjaman', ascending=False)

st.subheader("Rata-rata Peminjaman Sepeda berdasarkan Kondisi Cuaca")
st.dataframe(weather_rentals, use_container_width=True)

st.markdown("---")


st.header("Pola Peminjaman Berdasarkan Waktu")


workingday_hour_df = filtered_hour_df[filtered_hour_df['workingday'] == 1]
holiday_hour_df = filtered_hour_df[filtered_hour_df['workingday'] == 0]


workingday_hourly = workingday_hour_df.groupby('hr')['cnt'].mean().reset_index()
holiday_hourly = holiday_hour_df.groupby('hr')['cnt'].mean().reset_index()

st.subheader("Pola Peminjaman Sepeda per Jam")
fig, ax = plt.subplots(figsize=(14, 6))
sns.lineplot(x='hr', y='cnt', data=workingday_hourly, marker='o', label='Hari Kerja', ax=ax)
sns.lineplot(x='hr', y='cnt', data=holiday_hourly, marker='o', label='Hari Libur', ax=ax)
ax.set_xlabel('Jam')
ax.set_ylabel('Rata-rata Peminjaman')
ax.set_title('Pola Peminjaman Sepeda per Jam: Hari Kerja vs Hari Libur')
ax.set_xticks(range(0, 24))
ax.grid(True)
ax.legend()
st.pyplot(fig)

st.subheader("Jam-Jam Puncak Peminjaman Sepeda")
col1, col2 = st.columns(2)

with col1:
    st.write("Hari Kerja")
    peak_hours_workingday = workingday_hourly.sort_values('cnt', ascending=False).head(3)
    for _, row in peak_hours_workingday.iterrows():
        st.metric(f"Jam {int(row['hr'])}", f"{row['cnt']:.2f} peminjaman")

with col2:
    st.write("Hari Libur")
    peak_hours_holiday = holiday_hourly.sort_values('cnt', ascending=False).head(3)
    for _, row in peak_hours_holiday.iterrows():
        st.metric(f"Jam {int(row['hr'])}", f"{row['cnt']:.2f} peminjaman")

st.markdown("---")


st.header("Perbandingan Hari Kerja dan Hari Libur")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Rata-rata Peminjaman: Hari Kerja vs Hari Libur")
    day_type_mean = filtered_day_df.groupby('workingday_label')['cnt'].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x='workingday_label', y='cnt', data=day_type_mean, palette='Set2', ax=ax)
    ax.set_xlabel('Tipe Hari')
    ax.set_ylabel('Rata-rata Peminjaman')
    ax.set_title('Rata-rata Peminjaman Sepeda: Hari Kerja vs Hari Libur')
    st.pyplot(fig)

with col2:
    st.subheader("Total Peminjaman: Hari Kerja vs Hari Libur")
    day_type_sum = filtered_day_df.groupby('workingday_label')['cnt'].sum().reset_index()
    
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x='workingday_label', y='cnt', data=day_type_sum, palette='Set2', ax=ax)
    ax.set_xlabel('Tipe Hari')
    ax.set_ylabel('Total Peminjaman')
    ax.set_title('Total Peminjaman Sepeda: Hari Kerja vs Hari Libur')
    st.pyplot(fig)

st.markdown("---")


st.header("Kesimpulan")
st.markdown("""
Berdasarkan analisis yang telah dilakukan, dapat diambil beberapa kesimpulan:

1. **Pengaruh Musim**: Musim memiliki pengaruh signifikan terhadap jumlah peminjaman sepeda, dengan jumlah peminjaman tertinggi terjadi pada musim panas dan musim gugur. Hal ini menunjukkan bahwa faktor cuaca sangat mempengaruhi keputusan pengguna untuk meminjam sepeda.

2. **Pengaruh Cuaca**: Kondisi cuaca cerah menghasilkan rata-rata peminjaman sepeda yang jauh lebih tinggi dibandingkan saat kondisi hujan. Ini mengindikasikan bahwa pengguna cenderung menghindari bersepeda saat cuaca buruk.

3. **Pola Waktu**: Terdapat dua periode puncak peminjaman sepeda dalam sehari, yaitu pada pagi hari (sekitar jam 8) dan sore hari (sekitar jam 17-18). Pola ini mencerminkan waktu berangkat dan pulang kerja/sekolah, yang menunjukkan bahwa sepeda banyak digunakan untuk komuter harian.

4. **Hari Kerja vs Hari Libur**: Terdapat perbedaan pola penggunaan sepeda antara hari kerja dan hari libur. Pada hari kerja, puncak peminjaman terjadi pada jam berangkat dan pulang kerja, sedangkan pada hari libur, pola peminjaman lebih merata sepanjang hari dengan peningkatan pada siang hari.
""")

# Rekomendasi
st.header("Rekomendasi")
st.markdown("""
Berdasarkan hasil analisis, berikut adalah beberapa rekomendasi untuk layanan bike sharing:

1. **Penyesuaian Armada**: Meningkatkan jumlah sepeda yang tersedia pada musim panas dan musim gugur, serta pada jam-jam sibuk (pagi dan sore hari).

2. **Promosi Musiman**: Memberikan diskon atau promosi khusus pada musim dingin dan musim semi untuk meningkatkan penggunaan sepeda pada musim tersebut.

3. **Program Cuaca Buruk**: Menyediakan insentif khusus untuk pengguna yang meminjam sepeda pada cuaca buruk, seperti poin reward tambahan atau diskon khusus.

4. **Optimasi Lokasi Stasiun**: Menempatkan lebih banyak sepeda di stasiun-stasiun yang dekat dengan pusat perkantoran dan sekolah untuk mengakomodasi kebutuhan komuter pada jam sibuk.

5. **Program Akhir Pekan**: Membuat program khusus untuk akhir pekan, seperti paket keluarga atau tur bersepeda, untuk meningkatkan penggunaan sepeda pada hari libur.
""")

# Footer
st.markdown("---")
st.caption("© 2025 Farhan maulana pangestu - Dicoding Indonesia")