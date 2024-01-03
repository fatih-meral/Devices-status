from influxdb import InfluxDBClient
import ping3
import time

# InfluxDB bağlantı bilgileri
host = ''
port = 8086
user = ''
password = ''
dbname = ''

client = InfluxDBClient(host, port, user, password, dbname)
# InfluxDB bağlantı bilgileri

#agents
dosya_adi = "agents.txt"

try:
    dosya = open(dosya_adi, 'r')
    
    print("Dosya mevcut.")
    
except FileNotFoundError:
    dosya = open(dosya_adi, 'w')
    print("Dosya oluşturuldu.")
    dosya = open(dosya_adi, 'r')

icerik = dosya.readlines()
agents_list = [satir.strip() for satir in icerik] ##gereksiz boşluları atmak için
dosya.close()
#agents


while True:
    for agent in agents_list:
        response = ping3.ping(agent)
        if response:
            print(f"{agent}: UP")
            json_body = [
                {
                    "measurement": "ping_status",
                    "tags": {
                        "host": agent
                    },
                    "fields": {
                        "status": 2
                    }
                }
            ]
            client.write_points(json_body)
        else:
            print(f"{agent}: DOWN")
            json_body = [
                {
                    "measurement": "ping_status",
                    "tags": {
                        "host": agent
                    },
                    "fields": {
                        "status": 1
                    }
                }
            ]
            client.write_points(json_body)
    print("--------------")
    time.sleep(3) 