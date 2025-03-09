# Proyek Analisis Data: Bike Sharing Dataset
# Nama: Farhan Maulana Pangestu
# ID Dicoding: mc487d5y1426


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

sns.set(style='darkgrid')
plt.style.use('ggplot')

day_df = pd.read_csv('data/day.csv')
hour_df = pd.read_csv('data/hour.csv')

print("Informasi Dataset Harian:")
print(day_df.info())
print("\nInformasi Dataset Per Jam:")
print(hour_df.info())


print("\nStatistik Deskriptif Dataset Harian:")
print(day_df.describe())


print("\nSampel Data Harian:")
print(day_df.head())
print("\nSampel Data Per Jam:")
print(hour_df.head())


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


plt.figure(figsize=(12, 6))
sns.barplot(x='season_label', y='cnt', data=day_df, estimator=np.sum, ci=None)
plt.title('Total Bike Rentals by Season')
plt.xlabel('Season')
plt.ylabel('Total Rentals')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('visualizations/rentals_by_season.png')
plt.show()

season_rentals = day_df.groupby('season_label')['cnt'].sum()
total_rentals = day_df['cnt'].sum()
season_percentage = (season_rentals / total_rentals * 100).round(2)

print("\nPersentase Penggunaan Sepeda berdasarkan Musim:")
for season, percentage in season_percentage.items():
    print(f"{season}: {percentage}%")


plt.figure(figsize=(12, 6))
sns.boxplot(x='weather_label', y='cnt', data=day_df)
plt.title('Bike Rentals Distribution by Weather Condition')
plt.xlabel('Weather Condition')
plt.ylabel('Daily Rentals')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('visualizations/rentals_by_weather.png')
plt.show()


weather_rentals = day_df.groupby('weather_label')['cnt'].agg(['mean', 'std', 'count'])
weather_rentals = weather_rentals.reset_index()
weather_rentals.columns = ['Weather Condition', 'Average Rentals', 'Standard Deviation', 'Count']

print("\nRata-rata Penggunaan Sepeda berdasarkan Kondisi Cuaca:")
print(weather_rentals)


hourly_rentals = hour_df.groupby('hr')['cnt'].mean().reset_index()

plt.figure(figsize=(14, 6))
sns.lineplot(x='hr', y='cnt', data=hourly_rentals, marker='o')
plt.title('Average Bike Rentals by Hour of Day')
plt.xlabel('Hour of Day')
plt.ylabel('Average Rentals')
plt.xticks(range(0, 24))
plt.grid(True)
plt.tight_layout()
plt.savefig('visualizations/rentals_by_hour.png')
plt.show()


peak_hours = hourly_rentals.sort_values('cnt', ascending=False).head(3)
print("\nJam-Jam Puncak Peminjaman Sepeda:")
for _, row in peak_hours.iterrows():
    print(f"Jam {int(row['hr'])}: Rata-rata {row['cnt']:.2f} peminjaman")


plt.figure(figsize=(10, 6))
sns.barplot(x='workingday_label', y='cnt', data=day_df, estimator=np.mean, ci=None)
plt.title('Average Bike Rentals: Working Days vs Weekends/Holidays')
plt.xlabel('Day Type')
plt.ylabel('Average Rentals')
plt.tight_layout()
plt.savefig('visualizations/rentals_workday_vs_holiday.png')
plt.show()

day_type_rentals = day_df.groupby('workingday_label')['cnt'].agg(['mean', 'std', 'sum'])
day_type_rentals = day_type_rentals.reset_index()
day_type_rentals.columns = ['Day Type', 'Average Rentals', 'Standard Deviation', 'Total Rentals']

print("\nPenggunaan Sepeda berdasarkan Tipe Hari:")
print(day_type_rentals)

