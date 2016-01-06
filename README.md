# Sense Hat weather station

###Current weather outside (Cloudy day):
![img_0938](https://cloud.githubusercontent.com/assets/6000156/12142690/6ae4e69a-b47a-11e5-9653-fe9bfbc8411f.JPG)

###Rain probability for the next 7 days (One bar per day the higher the bar the higher the chance of rain):
![img_0940](https://cloud.githubusercontent.com/assets/6000156/12142693/712976c4-b47a-11e5-95b9-f5f7eb97479c.JPG)

### Prerequisite
- Rasperry pi model B+ (I haven't tested with other models)
- Sense Hat (https://www.raspberrypi.org/products/sense-hat/)
- Forecast.io API_Key

### Install guide
- Download all file to a location on your raspberry pi
- Install all packages that will need to be imported
- In temp.py Replace <CITY COUNTRY> by your own location 
  e.g location = geolocator.geocode("Delft Netherlands")
- In temp.py Replace <FORECAST.IO API_KEY> by your API key
  Keys can be generated on https://developer.forecast.io/
- to run in the terminal type: python temp.py 

### Usage
- If keyboard is connected use the arrows to access the different screens
- If no keyboard is connected when launching the app use the sense joystick


