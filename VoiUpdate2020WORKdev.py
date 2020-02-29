import json
import requests
import webbrowser
import collections
from geopy import distance

class Voi:
    
    def openSession(self):
        with open("authToken.txt","r") as f: # Get your authentication token from a file. You could've just set is as a variable or directly use it in the request.
            s=f.read()
            authToken=s.replace("\n","")

        headers = { # to get the correct type of data from the request. Default data type returned is XML
        'Content-type': 'application/json',
        'Accept': 'application/json',
        }

        data={"authenticationToken": authToken}
        r=requests.post('https://api.voiapp.io/v1/auth/session',headers=headers,data=json.dumps(data)).json() # Request session tokens with your authentication token
        self.accessToken=r["accessToken"]
        authToken=r["authenticationToken"]
        return self.accessToken
    
    def zoneSearch(self,lat,lng):# Used to lookup the zone corresponding to the user input and return the dict containing the scooters. The zone MUST be given or the request wont return anything
        url="https://api.voiapp.io/v1/zones"
        headers={
            "x-access-token": self.openSession()
        }
        params={ # These values originate from getCoords which geocodes locations (address, stores, monuments) into coordinate values. 
            "lat":lat,
            "lng":lng
        }
        r=requests.get(url,headers=headers, params=params).json()
        voiCity=r["zones"][0]["zone_id"] # Returns the city or area which corresponds to the given coordinate values
        url=("https://api.voiapp.io/v1/vehicles/zone/"+str(voiCity)+"/ready")
        
        self.scooters=requests.get(url, headers=headers,params=params).json()
        return self.scooters # The dict containing the scooter data

    def getOpenRouteKey(self):
        with open("accessTokens.txt","r") as json_file: # Again, gets the access token for the API from a file. Easy to save space by just assigning the key to a variable instead of this mess
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

    def getCoords(self,location):# Returns placeCoords which correspond to the location given by the user.
        key=self.getOpenRouteKey() 
        headers = { # Propably could remove some of these but too lazy
        'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8','Authorization':key
    }
            
        placeCoordsGet=requests.get('https://api.openrouteservice.org/geocode/search?api_key='+key+'&text='+location).json()
        placeCoords=placeCoordsGet["features"][0]["geometry"]["coordinates"]
        return placeCoords
        
    def scooterLookup(self):
        key=self.getMapQuestKey()
        while True:
            scootInfo={}
            locations_url=[]
            location=input("What is your current location?(e.g 'Lemminkäisenkatu 30, Turku'): ")
            if location=="q" or location=="quit":
                break
            radius=input("In what radius do you want to search scooters in?(500 corresponds to 500 meters): ")
            try:
                radius=float(radius)*0.001
            except ValueError:
                print("Present a valid numeric value.")
                continue
            
            placeCoords=self.getCoords(location)
            self.zoneSearch(placeCoords[1],placeCoords[0])

            placeCoords.reverse()
            placeCoords=str(placeCoords).replace("[","").replace("]","")

            for x in range(len(self.scooters)):
                if distance.distance(placeCoords,self.scooters[x]["location"]).km < float(radius):
                    scootInfo[self.scooters[x]["short"]]=[round(distance.distance(placeCoords,self.scooters[x]["location"]).m,0),self.scooters[x]["location"]]
                    scootInfo={k: v for k, v in sorted(scootInfo.items(), key=lambda item: item[1])}

            
            if len(scootInfo)>0:
                print("The scooters within radius of ",radius,"km",len(scootInfo))
                print("the scooters near you: ")
                for x in scootInfo:
                    print(x,"approximately",scootInfo[x][0],"meters away.")

                while True:
                    scoot=input("Which scooter do you want to find? Or press 'q' to return to location search: ")
                    if scoot=="q" or scoot=="quit":
                        break
                    for x in scootInfo:
                        scootCoord=scootInfo[x][1]
                        scootCoords=str(scootCoord).strip('[]').replace(",","")

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
        



