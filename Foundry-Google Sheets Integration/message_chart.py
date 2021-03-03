import os
import datetime as dt
import foundry_socket
import sheets_socket


def excel_date(tstamp):
    temp = dt.datetime(1899, 12, 30)
    delta = dt.datetime.fromtimestamp(tstamp / 1000) - temp
    return float(delta.days) + (float(delta.seconds) / 86400)


# Connect to Foundry and Google Sheets.
driver = foundry_socket.connect()
api = sheets_socket.connect()

# Get spreadsheet content.
values = api.spreadsheets().values().get(spreadsheetId=os.environ["SHEET_ID"], valueRenderOption="UNFORMATTED_VALUE", range="A1:G1000").execute()["values"]
last_row = values[-1]

# Create username dict.
usernames = {}
users = driver.execute_script("return game.users._source")
for user in users:
    usernames[user["_id"]] = user["name"]

# Get and count messages.
messages = driver.execute_script("return game.messages._source.filter(message => message.type === 2);")
data = []
for message in messages:
    # Skip messages before existing timestamp.
    serial = excel_date(message["timestamp"])
    if serial <= last_row[0]:
        continue

    data_point = None
    # Create data_point with the same message count as the last.
    if len(data) == 0:
        data_point = {"time": serial}
        i = 1
        for user in usernames:
            data_point[usernames[user]] = 0#last_row[i]
            i += 1
    else:
        data_point = data[-1].copy()
        data_point["time"] = serial

    # Add one message to the sender of the current one (Unless it's Hayes :( )
    if message["user"] in usernames:
        data_point[usernames[message["user"]]] += 1

    data.append(data_point)

# Convert data to 2D array for the Sheets API.
update = [None] * len(data)
for i in range(len(data)):
    update[i] = list(data[i].values())

update = {"values": update}

api.spreadsheets().values().append(
    spreadsheetId=os.environ["SHEET_ID"], range="A1:G1000", valueInputOption="USER_ENTERED", body=update
).execute()
