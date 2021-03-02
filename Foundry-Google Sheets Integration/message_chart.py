import foundry_socket

driver = foundry_socket.connect()

# Create username dict.
usernames = {}
users = driver.execute_script("return game.users._source")
for user in users:
    usernames[user["_id"]] = user["name"]

# Get and count messages.
messages = driver.execute_script("return game.messages._source.filter(message => message.type === 2);")
data = []
for message in messages:
    # Create data_point with the same message count as the last, or all 0.
    if len(data) == 0:
        data_point = {"time": message["timestamp"]}
        for user in usernames:
            data_point[usernames[user]] = 0
    else:
        data_point = data[-1]
        data_point["time"] = message["timestamp"]

    # Add one message to the sender of the current one (Unless it's Hayes :( )
    if message["user"] in usernames:
        data_point[usernames[message["user"]]] += 1

    data.append(data_point)

print(data)
