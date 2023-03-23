# Welcome to Cursor



# 1. Try generating with command K on a new line. Ask for a pytorch script of a feedforward neural network
# 2. Then, select the outputted code and hit chat. Ask if there's a bug. Ask how to improve.
# 3. Try selecting some code and hitting edit. Ask the bot to add residual layers.
# 4. To try out cursor on your own projects, go to the file menu (top left) and open a folder.

import paho.mqtt.client as mqtt
import mysql.connector
import json

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("ecgs")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    # Connect to the database
    cnx = mysql.connector.connect(user='root', password='yfzx.2021',
                                host='47.101.220.2',
                                database='aisense')
    cursor = cnx.cursor()

    # Insert some data into the table
    msgb = msg.payload
    msgstr = msgb.decode("utf-8")
    jsonobj = json.loads(msgstr)
    print(jsonobj)
    add_data = ("INSERT INTO `aisense`.`water`(`device_id`, `ec`, `o2`, `orp`, `ph`, `temp`, `tub`, `date1`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
    data = (jsonobj["id"], jsonobj["ec"], jsonobj["cl"], jsonobj["orp"], jsonobj["ph"], jsonobj["temp"], jsonobj["turb"], jsonobj["timestamp"])
    cursor.execute(add_data, data)

    # Make sure data is committed to the database
    cnx.commit()

    # Close the cursor and connection
    cursor.close()
    cnx.close()
    

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("47.101.220.2", 1883, 60)
client.loop_forever()
