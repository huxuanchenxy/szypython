import random
import string
import mysql.connector

# Connect to the database
cnx = mysql.connector.connect(user='root', password='yfzx.2021',
                              host='47.101.220.2',
                              database='aisense')
cursor = cnx.cursor()

# Generate random data
for i in range(1000):
    # name = ''.join(random.choices(string.ascii_uppercase, k=10))
    # age = random.randint(18, 65)
    # salary = round(random.uniform(20000, 100000), 2)

    
    imei = '355952096464725'
    ccid =  '355952096464725'
    vers = '1.0'
    devicetype = '123'
    rssi =  '123'
    snr =  '123'
    count =  '1'
    nh3 =  random.randint(0, 500)
    h2s =  random.randint(0, 200)
    tvoc =  ''
    ch2o =  ''
    co2 =  ''
    pm25 =  ''
    pm10 =  ''
    hum =  ''
    temp =  ''
    rnd = random.randint(10, 12)
    rnd1 = random.randint(1, 29)
    date1 = "2022-{}-{} 10:00:07".format(rnd,rnd1)
    # Insert data into the database
    

    query = "INSERT INTO `aisense`.`gas`( `imei`, `ccid`, `vers`, `devicetype`, `rssi`, `snr`, `count`, `nh3`, `h2s`, `tvoc`, `ch2o`, `co2`, `pm25`, `pm10`, `hum`, `temp`, `date1`) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (imei, ccid,  vers ,  devicetype ,  rssi ,  snr ,  count ,  nh3 ,  h2s ,  tvoc ,  ch2o ,  co2 ,  pm25 ,  pm10 ,  hum ,  temp ,  date1 )
    cursor.execute(query, values)

# Commit the changes
cnx.commit()

# Close the connection
cursor.close()
cnx.close()
