import random
import time
import sqlite3
import csv

# Ensure the table exists before starting the loop
conn = sqlite3.connect('env_data.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        temperature REAL,
        humidity REAL,
        air_quality REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''') 
conn.commit()
conn.close()

for _ in range(10):  # Change 10 to any number of readings you want
    temperature = random.uniform(20, 35)
    humidity = random.uniform(30, 70)
    gas_ppm = random.uniform(200, 400)

    print(f"Temp={temperature:.1f}C Humidity={humidity:.1f}% AirQuality={gas_ppm:.1f}ppm")

    conn = sqlite3.connect('env_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO readings (temperature, humidity, air_quality) VALUES (?, ?, ?)",
              (temperature, humidity, gas_ppm))
    conn.commit()
    conn.close()

    time.sleep(5)

# Display all readings after collection
conn = sqlite3.connect('env_data.db')
c = conn.cursor()
c.execute("SELECT * FROM readings ORDER BY id DESC LIMIT 10")
rows = c.fetchall()
print("\nAll Recorded Readings (latest 10):")
for row in rows:
    print(row)

# Calculate and display averages
c.execute("SELECT AVG(temperature), AVG(humidity), AVG(air_quality) FROM readings")
avg_temp, avg_hum, avg_air = c.fetchone()
print(f"\nAverage Temperature: {avg_temp:.2f}C")
print(f"Average Humidity: {avg_hum:.2f}%")
print(f"Average Air Quality: {avg_air:.2f}ppm")

# Export to CSV
c.execute("SELECT * FROM readings")
all_rows = c.fetchall()
with open('readings.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['ID', 'Temperature', 'Humidity', 'Air Quality', 'Timestamp'])
    writer.writerows(all_rows)
print("\nData exported to readings.csv")

conn.close()