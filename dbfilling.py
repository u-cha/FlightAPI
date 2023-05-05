# import requests
# import sqlite3
# import random
#
# airports_json = requests.get("https://api.travelpayouts.com/data/ru/airports.json").json()
# airlines_json = requests.get("https://api.travelpayouts.com/data/ru/airlines.json").json()
#
# counter = 0


# airports
# buffer = []
# with sqlite3.connect('./database/airports.sqlite3') as db_connection:
#     cursor = db_connection.cursor()
#     for airport in airports_json:
#         if airport['iata_type'] == 'airport':
#
#             if airport["code"] not in buffer:
#                 print(f'code={airport["code"]}, name={airport["name_translations"]["en"]}')
#                 query = f'INSERT INTO Airports (code, name) VALUES ("{airport["code"]}", "{airport["name_translations"]["en"]}")'
#                 cursor.execute(query)
#                 db_connection.commit()
#                 buffer.append(airport["code"])
#             counter += 1
# print(counter, len(buffer))

#airlines
# buffer = []
# with sqlite3.connect('./database/airports.sqlite3') as db_connection:
#     cursor = db_connection.cursor()
#     for airline in airlines_json:
#
#         if airline["code"] not in buffer and airline["code"] != "1H":
#
#             query = f'INSERT INTO Airlines (code, name) VALUES ("{airline["code"]}", "{airline["name_translations"]["en"]}")'
#             cursor.execute(query)
#             db_connection.commit()
#             buffer.append(airline["code"])
#         counter += 1
# print(counter, len(buffer))


# #flights
# buffer = []
# with sqlite3.connect('./database/airports.sqlite3') as db_connection:
#     cursor = db_connection.cursor()
#     for _ in range(1000):
#         from_airport_id = random.randint(1, 3260)
#         to_airport_id = random.randint(1, 3260)
#         airline_id = random.randint(1, 1078)
#         price = round(random.random() * 1000 * random.randint(1, 5), 2)
#         if (from_airport_id, to_airport_id, airline_id, price) not in buffer:
#
#             query = f'INSERT INTO Flights (from_airport_id, to_airport_id, airline_id, price) ' \
#                     f'VALUES ({from_airport_id}, {to_airport_id}, {airline_id}, {price})'
#             cursor.execute(query)
#             db_connection.commit()
#             buffer.append((from_airport_id, to_airport_id, airline_id, price))
#         counter += 1
# print(counter, len(buffer))
