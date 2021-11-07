# Bebther
> Simple weather app made with Python and QtDesigner.

## Features
* Shows weather info for different regions from different weather providers
* Get and compare weather info between two days or regions
* Save current weather info to the DataBase to compare it with the next day's weather
* Open a screenshot-ready window containing weather info to share it with your friends 
* Add your own weather providers using a unique modular system

## Known Issues
* General unstability  
  
## Installing a new parser
The bebther application has a unique modular system allowing users to install or create their own parsers.
1. Download the parser file from any resource you **trust**
   > Be advised that the Python language allows the parser's developer do any operations they want with your OS
   > Parser file's name should end with `Parser.py`. *example: [owmParser.py](Parsers/owmParser.py)*
2. Put the file in the `./Parsers/` folder
3. Update the application's parsers list either using the UI button or by restarting the application
4. Your new parser should show up in the parsers list in the application
## Creating a new parser guide
The bebther application has a unique modular system allowing users to install or create their own parsers.
1. Create a python file in a `./Parsers/` directory
    > **IMPORTANT**: the file's name should end with `Parser.py`, *example: [owmParser.py](Parsers/owmParser.py)*
2. Create a class called `Parser` and inherit [baseParser](Parsers/baseParser.py) so it would be easier to follow the data type
3. Create a parser information fields in your parser class
    > **Bold** are neccessary
    >* **name** - parsed resource's name, **will be shown in the UI**
    >* *description* - short description of the parser or the parsed resource
    >* *url* - link to the parsed resource's website 
    >* *apikey* - parsed resource's API key if needed
4. Create a `getCity` method that will take a city name and return a location ID that suits for your parser
5. Create a `getData` method that will return a formatted dictionary of weather data
    > **PLEASE FOLLOW THE DATA FORMAT**
    >* Temperature
    >* Humidity
    >* WindSpeed
    >* Pressure
    >* UVIndex
    >* DayTemperature
    >* NightTemperature
    >* SunriseTime
    >* SunsetTime
6. Update the application's parsers list either using the UI button or by restarting the application
7. Your parser should show up in the parsers list in application's UI  
Feel free to share your parser in any possible way
## Used Materials
### Icons
> All icons belong to [flaticon](https://flaticon.com)  
![Barometer icon](ui/images/barometer.png) [Barometer](https://www.flaticon.com/free-icon/barometer_481430) by **Those Icons**  
![Drop icon](ui/images/drop.png) [Drop](https://www.flaticon.com/free-icon/drop_606797) by **Good Ware**  
![Night-mode icon](ui/images/night-mode.png) [Night-mode](https://www.flaticon.com/premium-icon/night-mode_2182323) by **rsetiawan**  
![Sunny icon](ui/images/sunny.png) [Sunny](https://www.flaticon.com/premium-icon/sunny_3222672) by **kosonicon**  
![Sunrise icon](ui/images/sunrise.png) [Sunrise](https://www.flaticon.com/premium-icon/sunrise_4398453) by **Secret Studio**  
![Sunset icon](ui/images/sunset.png) [Sunset](https://www.flaticon.com/free-icon/sunset_287668) by **Nikita Golubev**  
![Ultraviolet icon](ui/images/ultraviolet.png) [Ultraviolet](https://www.flaticon.com/premium-icon/ultraviolet_3512031) by **Freepik**  
![Wind icon](ui/images/wind.png) [Wind](https://www.flaticon.com/premium-icon/wind_2057945) by **Freepik**  
![Diskette icon](ui/images/save.png) [Diskette](https://www.flaticon.com/premium-icon/diskette_2874091) by **Yogi Aprelliyanto**  
![Reset icon](ui/images/reload.png) [Reset](https://www.flaticon.com/premium-icon/reset_2618245) by **inkubators**  
Thanks to all creators listed above for their work and letting us use their materials free of charge

## Authors
> Created in terms of [Yandex Lyceum](https://lyceum.yandex.ru) pyQt project
* **Vsevolod Levitan** *(@1ffycat/@Iffycat)* [GitHub](https://github.com/1ffycat) [VK](https://vk.com/1ffycat)
* **Leonid Pashnin** *(@Sm4rtSt1ck)* [GitHub](https://github.com/Sm4rtSt1ck) [VK](https://vk.com/sex.maker)