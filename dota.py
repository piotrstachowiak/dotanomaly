import requests
import json
import mysql.connector as my
import time

steam_32_id = '87545847'

url0 = f'https://api.opendota.com/api/players/{steam_32_id}/refresh'
url1 = f'https://api.opendota.com/api/players/{steam_32_id}'
url2 = 'https://api.opendota.com/api/heroStats'
url3 = f'https://api.opendota.com/api/players/{steam_32_id}/heroes'



# REFRESH
# resp0 = requests.post(url0)


# RANK
# resp1 = requests.get(url1)
# data1 = json.loads(resp1.text)
# rank = str(data1.get('rank_tier'))[:1]
# print(rank)
rank = 3

# GLOBAL WINRATE FOR MY RANK
# resp2 = requests.get(url2)
# data2 = json.loads(resp2.text)
# for x in data2:
#     print(
#         x.get('id'),
#         x.get('localized_name'),
#         x.get(f'{rank}_pick'),
#         x.get(f'{rank}_win'),
#         str(x.get(f'{rank}_win')/x.get(f'{rank}_pick') * 100)[:4] + '%'
#     )

# MY WINRATE
# resp3 = requests.get(url3)
# data3 = json.loads(resp3.text)
# for x in data3:
#     print(
#         x['hero_id'],
#         x['games'],
#         x['win'],
#         str(x['win']/x['games'] * 100)[:4] + '%' if x['games'] != 0 else 'didnt play that'
#     )

timestamp = [time.time_ns()]

mydb = my.connect(
    host="localhost",
    user="root",
    password="password",
    database="dota"
)


# GLOBAL WINRATE FOR MY RANK
resp2 = requests.get(url2)
data2 = json.loads(resp2.text)
# for x in data2:
#     print(
#         x.get('id'),
#         x.get('localized_name'),
#         x.get(f'{rank}_pick'),
#         x.get(f'{rank}_win'),
#         str(x.get(f'{rank}_win')/x.get(f'{rank}_pick') * 100)[:4] + '%'
#     )

print(timestamp)
mycursor = mydb.cursor()
query1 = 'CREATE TABLE global%s (id int, name varchar(255), picks int, wins int, winrate float)'
query2 = 'INSERT INTO global%s VALUES (%s, %s, %s, %s, %s)'
mycursor.execute(query1, timestamp)

for x in data2:
    query2_data = [
        *timestamp,
        x.get('id'),
        x.get('localized_name'),
        x.get(f'{rank}_pick'),
        x.get(f'{rank}_win'),
        round(x.get(f'{rank}_win')/x.get(f'{rank}_pick') * 100, 2)
    ]
    print(query2_data)
    mycursor.execute(query2, query2_data)

mydb.commit()
mycursor.close()
mydb.close()