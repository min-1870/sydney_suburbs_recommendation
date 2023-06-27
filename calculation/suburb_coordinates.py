import googlemap_api
import pandas as pd

def suburbCoordinates(suburbs):
    for i in range(10+):
        coordinates = googlemap_api.getCoordinates(suburbs.at[i, 'suburbs'])
        suburbs.at[i, 'latitude'] = coordinates[0]
        suburbs.at[i, 'longtidue'] = coordinates[1]

    return suburbs

res = suburbCoordinates(pd.read_csv('./original_data/sydney_suburbs.csv'))
res.to_csv('suburb_coordinates.csv', index=False)