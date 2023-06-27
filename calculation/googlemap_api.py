import googlemaps
from datetime import datetime, timedelta

api_key = ''
gmaps = googlemaps.Client(key=api_key)

SYDNEY_ADDRESS = ', Sydney, NSW, Australia'

def toSydneyAddress(address):
    '''
    input: address(string)
    output: address(string)
    '''
    return address+SYDNEY_ADDRESS

def getPostcode(address):
    result = None
    geocode_result = gmaps.geocode(toSydneyAddress(address), region='AU')
    #print(geocode_result)
    # Extract the postcode from the Geocoding result
    if geocode_result:
        for component in geocode_result[0]['address_components']:
            if 'postal_code' in component['types']:
                result = component['long_name']
                break
    return result

def getCoordinates(address):
    '''
    input: address(string)
    output: tuple(latitude, longtidue)
    '''
    result = None
    geocode_result = gmaps.geocode(toSydneyAddress(address))
    if geocode_result:
        address = geocode_result[0]['geometry']['location']
        result = address['lat'], address['lng']
    return result

def getInfraInTheRange(infra, range, coordinate):
    '''
    input: infra(string), range in meter(float), tuple(latitude, longtidue)
    output: boolean
    '''
    result = None
    infras = gmaps.places_nearby(location=(coordinate[0], coordinate[1]), radius=range, type=infra)['results']   
    result = len(infras) > 0
    return result

def getTravelTime(departure, destination):
    '''
    input: tuple(latitude, longtidue), tuple(latitude, longtidue)
    output: integer(mins)
    '''
    DEPARTURE_TIME = datetime(2023, 6, 26, 12, 00, 0)
    result = None
    directions_result = []
    while len(directions_result) == 0:
        directions_result = gmaps.directions(departure, destination, departure_time=DEPARTURE_TIME, mode="transit")
        DEPARTURE_TIME = DEPARTURE_TIME - timedelta(days=1)
    time_string = directions_result[0]['legs'][0]['duration']['text']
    time_parts = time_string.split()
    if len(time_parts) == 4:
        result = int(time_parts[0]) * 60 + int(time_parts[2])
    elif len(time_parts) == 2:
        result = int(time_parts[0])
    else:
        result = None
    return result

#print(getInfraInTheRange('zoo', 2500, getCoordinates('Kensington , Sydney, Australia')))
#print(getTravelTime(getCoordinates('Abbotsford'), getCoordinates('Abbotsbury')))
#print(getCoordinates('Sydney , Sydney, Australia'))
#print(getCoordinates('Kensington , Sydney, Australia'))

#print(getCoordinates('2012'))
