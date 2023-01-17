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
resp1 = requests.get(url1)
data1 = json.loads(resp1.text)
rank = str(data1.get('rank_tier'))[:1]
# print(rank)
# rank = 3

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
resp3 = requests.get(url3)
data3 = json.loads(resp3.text)
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

# print(timestamp)
mycursor = mydb.cursor()
query1 = 'CREATE TABLE global (id int, name varchar(255), picks int, wins int, winrate float)'
query2 = 'INSERT INTO global VALUES (%s, %s, %s, %s, %s)'
query4 = 'CREATE TABLE my (id int, picks int, wins int, winrate float)'
query3 = 'INSERT INTO my VALUES (%s, %s, %s, %s)'
query5 = '''CREATE TABLE dotanomaly AS (
            SELECT my.id, global.name AS hero_name, my.winrate AS my_winrate, global.winrate AS global_winrate
            FROM my
            INNER JOIN global
            ON my.id = global.id
            WHERE my.picks > 2
            ORDER BY my.winrate-global.winrate DESC);'''
queryd = 'CREATE TABLE dotanomaly%s SELECT * FROM dotanomaly'
queryg = 'CREATE TABLE global%s SELECT * FROM global'
querym = 'CREATE TABLE my%s SELECT * FROM my'
queryx = 'DROP TABLE my'
queryy = 'DROP TABLE global'
queryz = 'DROP TABLE dotanomaly'



mycursor.execute(query1)
mycursor.execute(query4)

for x in data2:
    query2_data = [
        x.get('id'),
        x.get('localized_name'),
        x.get(f'{rank}_pick'),
        x.get(f'{rank}_win'),
        round(x.get(f'{rank}_win')/x.get(f'{rank}_pick') * 100, 2)
    ]
    mycursor.execute(query2, query2_data)

for y in data3:
    query3_data = [
        y.get('hero_id'),
        y.get('games'),
        y.get('win'),
        round(y.get('win') / y.get('games') * 100, 2) if y.get('games') != 0 else -1
    ]
    if y.get('games') != 0: mycursor.execute(query3, query3_data)

mycursor.execute(query5)

mycursor.execute(queryd, timestamp)
mycursor.execute(queryg, timestamp)
mycursor.execute(querym, timestamp)
mycursor.execute(queryx)
mycursor.execute(queryy)
mycursor.execute(queryz)

mydb.commit()
mycursor.close()
mydb.close()