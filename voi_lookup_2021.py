import json
import time
import datetime
import os
import requests
import webbrowser
import collections
from geopy import distance

class Voi:
    
    def openSession(self):
        self.currTime=time.time()
        if (self.currTime-os.path.getmtime("sessionToken.txt"))>780: # Checks if the file has been modified in the last 13 minutes, so that we can reduce the amount of API calls
            print("Requesting token from the API...")
            with open("authToken.txt","r") as f:            # Get your authentication token from a file. 
                s=f.read()                                  
                authToken=s.replace("\n","")

            headers = {                                     # to get the correct type of data from the request. Default data type returned is XML
            'Content-type': 'application/json',
            'Accept': 'application/json',
            }

            data={"authenticationToken": authToken}
            r=requests.post('https://api.voiapp.io/v1/auth/session',headers=headers,data=json.dumps(data)).json() # Request session tokens with your authentication token which expire after ~15 minutes
                
            with open("sessionToken.txt","w")as w:
                self.accessToken=r["accessToken"]
                authToken=r["authenticationToken"]
                w.write(self.accessToken)

        else:
            print("Getting token from file...")
            with open("sessionToken.txt","r")as f:
                self.accessToken=f.read()
                
        return self.accessToken
    
    def zoneSearch(self,lat,lng):                       # Used to lookup the zone corresponding to the user input and return the dict containing the scooters. 
        url="https://api.voiapp.io/v1/zones"            # The zone MUST be given or the request wont return anything
        headers={
            "x-access-token": self.openSession(),
            'Content-type': 'application/json',
            'Accept': 'application/json',
        }
        params={                                        # These values originate from getCoords which geocodes locations (address, stores, monuments) into coordinate values. 
            "lng":lng,
            "lat":lat
        }
        r=requests.get(url,headers=headers, params=params).json()
        voiCity=r["zones"][0]["zone_id"]                 # Returns the city or area which corresponds to the given coordinate values
        params["zone_id"]=voiCity
        
        print("I am getting useable scooters...\n")
        url=("https://api.voiapp.io/v2/rides/vehicles?")
        self.scooters=requests.get(url, headers=headers,params=params).json()   # The dict containing the scooter data
        with open("availableScooterInformation.txt","w") as w:   # Saving the scooter data to a text file. Is reset after each search
            w.write("The data was requested: " + datetime.datetime.fromtimestamp(self.currTime).strftime('%d-%m-%Y %H:%M:%S\n'))
            w.write(str(self.scooters))
                      
        return self.scooters

    def getOpenRouteKey(self):
        with open("accessTokens.txt","r") as json_file: # Again, gets the access token for the API from a file.
            data=json_file.read()                       
            obj=json.loads(data)
            openRouteKey=obj["tokens"]["openrouteservice"]["token"]
        return openRouteKey

    def getMapQuestKey(self):
        with open("accessTokens.txt","r") as json_file:
            data=json_file.read()
            obj=json.loads(data)
            mapQuestKey=obj["tokens"]["mapquest"]["token"]
        return mapQuestKey

    def getCoords(self,location):                       # Returns placeCoords which correspond to the location given by the user.
        key=self.getOpenRouteKey() 
        headers = {                                     
        'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8','Authorization':key
    }
            
        placeCoordsGet=requests.get('https://api.openrouteservice.org/geocode/search?api_key='+key+'&text='+location).json()
        placeCoords=placeCoordsGet["features"][0]["geometry"]["coordinates"]
        return placeCoords
        
    def scooterLookup(self):
        key=self.getMapQuestKey()
        radius=0.5
        while True:
            scootInfo={}
            locations_url=[]
            location=input("What is your current location?(e.g 'Eduskuntatalo,Helsinki'): ")
            if location=="q" or location=="quit":
                break
            
            placeCoords=self.getCoords(location)
            self.zoneSearch(placeCoords[1],placeCoords[0])
            placeCoords.reverse()

            placeCoords=str(placeCoords).replace("[","").replace("]","")
            for x in range(len(self.scooters['data']['vehicle_groups'][0]['vehicles'])):
                scootLocation=str(self.scooters['data']['vehicle_groups'][0]['vehicles'][x]['location']['lat'])+ ", " +str(self.scooters['data']['vehicle_groups'][0]['vehicles'][x]['location']['lng'])
                if distance.distance(placeCoords,scootLocation).km < float(radius):
                    if len(scootInfo)< 21:                   # Change the len(scootInfo)<"x" and "11" value here to match possible user defined amount
                        scootInfo[self.scooters['data']['vehicle_groups'][0]['vehicles'][x]["short"]]=[round(distance.distance(placeCoords,scootLocation).m,0),scootLocation]
                        scootInfo={k: v for k, v in sorted(scootInfo.items(), key=lambda item: item[1])}
                    else:
                        break
            
            if len(scootInfo)>0:
                print("The scooters within radius of ",radius,"km",len(scootInfo))
                print("the scooters near you: ")
                for x in scootInfo:
                    print(x,"approximately",scootInfo[x][0],"meters away.")

                for x in scootInfo:
                    scootCoords=scootInfo[x][1]

                    base_map_url="https://www.mapquestapi.com/staticmap/v5/map?locations="+placeCoords+"|flag-start|"
                    locations_url.append("|"+scootCoords+"|flag-"+x)
                    locations_url_str="|".join(str(location)for location in locations_url)
                    params="&size=1000,600@2x&key="+key
                    map_url=str(base_map_url+locations_url_str+params)
                    voiDistance=round(distance.distance(placeCoords,scootCoords).m,2)
                    print("The distance to the scooter is ",round(voiDistance,0),"meters.\n")
                    
                webbrowser.open(str(map_url))
                            
            else:
                print("There are no scooters nearby.\n")
   

voi=Voi()
voi.scooterLookup()
        



