import pandas as pd
import googlemap_api


#--------------------------------filter and calculate the rent fee
def calculateRent(fileName):
    data_frame = pd.read_csv(fileName)

    data_frame = data_frame[data_frame['dwelling types'] == 'Total']
    data_frame = data_frame.drop('dwelling types', axis=1)
    data_frame = data_frame[
        (data_frame['number of bedrooms'] != 'Not Specified') & 
        (data_frame['number of bedrooms'] != '4 or more Bedrooms')]
    data_frame = data_frame.dropna()
    data_frame = data_frame.reset_index(drop=True)

    #calculate new average Rent fee per person for each type of house, assume pay separetly for the house more than 1 bedroom.
    data_frame['rent(share)'] = ''
    for i in range(len(data_frame)):
        if data_frame.at[i, 'number of bedrooms'] == '2 Bedrooms':
            data_frame.at[i, 'rent'] = data_frame.at[i, 'rent'] / 2

        elif data_frame.at[i, 'number of bedrooms'] == '3 Bedrooms':
            data_frame.at[i, 'rent'] = data_frame.at[i, 'rent'] / 3
        elif data_frame.at[i, 'number of bedrooms'] == 'Bedsitter' or data_frame.at[i, 'number of bedrooms'] == '1 Bedroom':
            data_frame.at[i, 'rent(share)'] = data_frame.at[i, 'rent']

    #remove total of uknown type of house
    for i in range(len(data_frame)-1):
        if data_frame.at[i, 'number of bedrooms'] == 'Total' and data_frame.at[i+1, 'number of bedrooms'] == 'Total':
            data_frame = data_frame.drop(i)
    data_frame = data_frame.reset_index(drop=True)

    # #calcualte new average Rent fee per person
    rent = []
    rentShare = []
    index_of_last_total = None
    for i in range(len(data_frame)):
        if data_frame.at[i, 'number of bedrooms'] == 'Total' or i == len(data_frame)-1:
            if i == len(data_frame)-1:
                rent.append(data_frame.at[i, 'rent'])
            if index_of_last_total != None and len(rent) != 0:
                data_frame.at[index_of_last_total, 'rent'] = round(sum(rent)/len(rent))
                if len(rentShare) != 0:
                    data_frame.at[index_of_last_total, 'rent(share)'] = round(sum(rentShare)/len(rentShare))
                rent = []
                rentShare = []
            index_of_last_total = i
        else:
            if data_frame.at[i, 'number of bedrooms'] == 'Bedsitter' or data_frame.at[i, 'number of bedrooms'] == '1 Bedroom':
                rentShare.append(data_frame.at[i, 'rent(share)'])
            else:
                rent.append(data_frame.at[i, 'rent'])

    data_frame = data_frame[data_frame['number of bedrooms'] == 'Total']

    # #remove number of bedrooms column
    data_frame = data_frame.drop('number of bedrooms', axis=1)
    data_frame.columns = ['postcode', 'rent(share)', 'rent']
    data_frame = data_frame.reset_index(drop=True)
    return data_frame


#--------------------------------add postcode to each suburb
def addPostcode(fileName):
    ss_data_frame = pd.read_csv(fileName)

    for i in range(len(ss_data_frame)):
        if i % 20 == 0:
            print(str(round(i/len(ss_data_frame)*100)) + '%')
        ss_data_frame.at[i, 'postcode'] = googlemap_api.getPostcode(ss_data_frame.at[i, 'suburb'])
    return ss_data_frame


#--------------------------------suburbs rent
def suburbRent(ss_data_frame, wr_data_frame):
    data_frame = pd.DataFrame(columns=['suburb', 'postcode', 'rent', 'rent(share)'])
    for i in range(len(ss_data_frame)):
        postcode = None
        rent = None
        rentShare = None

        if not pd.isnull(ss_data_frame.at[i, 'postcode']):
            postcode = int(ss_data_frame.at[i, 'postcode'])

        try:
            rent = wr_data_frame.at[wr_data_frame['postcode'].tolist().index(postcode), 'rent']
            rentShare = wr_data_frame.at[wr_data_frame['postcode'].tolist().index(postcode), 'rent(share)']

        except ValueError:
            pass
        
        row = {'suburb': ss_data_frame.at[i, 'suburb'], 'postcode': postcode, 'rent': rent, 'rent(share)': rentShare}

        data_frame = pd.concat([data_frame, pd.DataFrame([row])], ignore_index=True)
    
    return(data_frame)



data_frame = suburbRent(addPostcode('sydney_suburbs.csv'), calculateRent('weekly_rent.csv'))

data_frame.to_csv("suburb_rent.csv", index=False)