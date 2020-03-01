# projects

WHAT'S IT ALL ABOUT

*VoiUpdate2020WORKdev*      ! ! ! WORK IN PROGRESS ! ! !
Whats this? 
This is a little program which started as a school assingment that I've improved upon and attemped to make into a properly working thing.
**In short**, it searches for VOI (https://www.voiscooters.com/) scooters in a user specified place in a user specified radius. 

**At length**, this program uses VOI API (https://api.voiapp.io/v1) to provide us with lot's of data about the scooters. The API requires the user to authenticate with their phonenumber to receive an *authentication token* which is then used to request for *access tokens* with a POST request. The *WoBike* repository made by ubahnverleih has been a great resource and it made this possible (https://github.com/ubahnverleih/WoBike) See this page to understand the process how data is requested from the voiAPI.

The user provided location is translated into coordinates with the help of openrouteservice API (https://api.openrouteservice.org/geocode/search?) which also requires authentication. This API is an improvement of the previous one I used (http://www.mapquestapi.com/geocoding/v1/address?) which didn't recognize the addresses quite well and it was inaccurate. 

The coordinates provided by openroute API are then used to search for the zone where the coordinates are (https://api.voiapp.io/v1/zones). You can't search for scooters without a zone. The data of the scooters is then requested with (https://api.voiapp.io/v1/vehicles/zone/YOUR_ZONE/ready). The location of these scooters is then opened with mapquests static map (https://www.mapquestapi.com/staticmap/v5/map?)

Future goals for this program:
1. Decide how the finished program should work (e.g. what does the program return to the user)
2. Make a GUI (possibly with Pythons Tkinter as a starter)
3. Fix the issue where the static map does not have all the scooters it should.
???
