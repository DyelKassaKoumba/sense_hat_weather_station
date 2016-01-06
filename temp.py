from evdev import InputDevice, ecodes,list_devices
from select import select
from geopy.geocoders import Nominatim
import forecastio
from sense_hat import SenseHat
from espeak import espeak
import os
import time

#Initialize Sense Hat
sense = SenseHat()
tFromHumidity = sense.get_temperature_from_humidity()
tFromPressure = sense.get_temperature_from_pressure()

print tFromHumidity*0.67
print tFromPressure
print sense.get_temperature()
print sense.get_pressure()

#Get latitude and longitude based on city and country
geolocator = Nominatim()
location = geolocator.geocode("<CITY COUNTRY>")

#Forcastio settings
api_key = "<FORECAST.IO API KEY>"
lat = location.latitude
lng = location.longitude

#Load forcast
forecast = forecastio.load_forecast(api_key, lat, lng, units="si")
currently = forecast.currently()
hourly = forecast.hourly()
daily = forecast.daily()

#Set up shower matrix
a = [0,0,0]
b = [0,0,255]
hasRained = 0
count = 0
counter = 0
matrix    = [0,0,0,0,0,0,0,0]
viz_matrix = [[0 for x in range(8)] for y in range(8)]
viz_image =  [  a,a,a,a,a,a,a,a,
                a,a,a,a,a,a,a,a,
                a,a,a,a,a,a,a,a,
                a,a,a,a,a,a,a,a,
                a,a,a,a,a,a,a,a,
                a,a,a,a,a,a,a,a,
                a,a,a,a,a,a,a,a,
                a,a,a,a,a,a,a,a
              ]


devices = [InputDevice(fn) for fn in list_devices()]
for dev in devices:
    if dev.name == "Raspberry Pi Sense HAT Joystick":
        js = dev

while True:
    sense.set_rotation(r=180)
    if currently.icon == "partly-cloudy-day":
        sense.load_image("icn_cloudysun_color.png")
    elif currently.icon == "partly-cloudy-night":
        sense.load_image("icn_cloudynight_color.png")
    elif currently.icon == "clear-day":
        sense.load_image("icn_sun_color.png")
    elif currently.icon == "clear-night":
        sense.load_image("icn_moon_color.png")
    elif currently.icon == "fog":
        sense.load_image("icn_fog_color.png")
    elif currently.icon == "wind":
        sense.load_image("icn_wind_color.png")
    elif currently.icon == "rain":
        sense.load_image("icn_rain_color.png")
    elif currently.icon == "sleet":
        sense.load_image("icn_sleet_color.png")
    elif currently.icon == "snow":
        sense.load_image("icn_snow_color.png")
    elif currently.icon == "fog":
        sense.load_image("icn_fog_color.png")
    else:
        sense.load_image("icn_cloud_color.png")
    r, w, x = select([dev.fd], [], [])
    for fd in r:
        for event in dev.read():
            if event.type == ecodes.EV_KEY and event.value == 1:
                if event.code == ecodes.KEY_UP:
                    forecast = forecastio.load_forecast(api_key, lat, lng, units="si")
                    currently = forecast.currently()
                    sense.set_rotation(r=180)
                    sense.show_message(str(currently.temperature))
                elif event.code == ecodes.KEY_LEFT:
                    forecast = forecastio.load_forecast(api_key, lat, lng, units="si")
                    hourly = forecast.hourly()
                    sense.set_rotation(r=90)
                    for hourlyData in hourly.data:
                        if hourlyData.time > currently.time:
                            if hourlyData.precipProbability > 0.5 and hasRained == 0:
                                hasRained = 1
                                timeToNextRain = hourlyData.time-currently.time
                                s = timeToNextRain.seconds
                                h, s = divmod(s,3600)
                                m, s = divmod(s, 60)
                    for hourlyData in hourly.data:
                        if hourlyData.time > currently.time and count < 8:
                            matrix[count] = int(hourlyData.precipProbability*8)
                            count = count+1
                            print matrix
                    for i in range (0,8):
                        if(matrix[i]>0):   
                            for j in range(0,8):
                                if(j<matrix[i]):
                                    viz_matrix[i][j] = b
                                else:
                                    viz_matrix[i][j] = a
                        else:
                            for k in range(0,8):
                                viz_matrix[i][k] = a
                    for i in range (0,8):
                        for j in range (0,8):
                             viz_image[counter] = viz_matrix[i][j]
                             counter = counter+1
                    counter = 0
                    count = 0
                    sense.set_pixels(viz_image)
                    time.sleep(5)
                elif event.code == ecodes.KEY_RIGHT:
                    forecast = forecastio.load_forecast(api_key, lat, lng, units="si")
                    daily = forecast.daily()
                    sense.set_rotation(r=90)
                    for dailyData in daily.data:
                        if dailyData.time > currently.time:
                            if dailyData.precipProbability > 0.5 and hasRained == 0:
                                hasRained = 1
                                timeToNextRain = dailyData.time-currently.time
                                s = timeToNextRain.seconds
                                h, s = divmod(s,3600)
                                m, s = divmod(s, 60)
                    for dailyData in daily.data:
                        if dailyData.time > currently.time and count < 8:
                            matrix[count] = int(dailyData.precipProbability*8)
                            count = count+1
                            print matrix
                    for i in range (0,8):
                        if(matrix[i]>0):   
                            for j in range(0,8):
                                if(j<matrix[i]):
                                    viz_matrix[i][j] = b
                                else:
                                    viz_matrix[i][j] = a
                        else:
                            for k in range(0,8):
                                viz_matrix[i][k] = a
                    for i in range (0,8):
                        for j in range (0,8):
                             viz_image[counter] = viz_matrix[i][j]
                             counter = counter+1
                    counter = 0
                    count = 0
                    sense.set_pixels(viz_image)
                    time.sleep(5)
                elif event.code == ecodes.KEY_DOWN:
                    sense.set_rotation(r=180)
                    t = sense.get_temperature()*0.67
                    t = round(t,1)
                    msg = "%s" % (t)
                    sense.show_message(msg)
                else:
                    forecast = forecastio.load_forecast(api_key, lat, lng, units="si")
                    hourly = forecast.hourly()
                    summ = hourly.summary.encode('utf-8')
                    sense.show_message(str(summ))
