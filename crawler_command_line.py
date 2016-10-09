import json
import requests
import time
import sys


def authenticate_client(client_id, client_secret):
    payload = {}
    # payload = {'grant_type': 'client_credentials', 'client_id': 'I4lgSBkRb99Sj6O4jx2Y_A','client_secret':'9IXdh84mzhEOdAg5x5NcWav2mSki4FvPvoBp0WO6RLdBxsQLemMNZPV1EBEtOTMj'}
    payload = {'grant_type': 'client_credentials', 'client_id': client_id, 'client_secret': client_secret}
    r = requests.post("https://api.yelp.com/oauth2/token", data=payload)
    # print(r.text)
    json_output = r.json()
    # print(json_output["access_token"])
    return json_output["access_token"]


def search_data(yelp_client, city, yelp_file):
    with open(yelp_file) as data_file:
        data = json.load(data_file)

        fh = open('city_out.txt', 'a+')
        for a in range(0, len(data)):
            if data[a]["city"] == city:
                lat = data[a]["lat"]
                lon = data[a]["lon"]
                offset = 0
                turn = 1
                # fh.write('Latitude-'+str(data[a]["lat"])+'Longitude-'+str(data[a]["lon"])+'\n')
                print('Search City ' + city + ' with Latitude ' + str(lat) + ' Longitude ' + str(lon))
                total = 0
                radius = 800
                check = False
                filestr = 'output_lat_' + str(lat) + 'long_' + str(lon) + '.json'
                fh = open(filestr, 'a+')
                while (total <= 0 or check == True):
                    url = 'https://api.yelp.com/v3/businesses/search?location='
                    url = url + city + '&limit=1'
                    url = url + '&latitude=' + str(lat) + '&longitude=' + str(lon) + '&radius=' + str(radius)
                    br = 'Bearer ' + yelp_client
                    headers = {'Authorization': br}
                    try:
                        r = requests.get(url, headers=headers)
                        print(r.text)
                    except requests.exceptions.ConnectionError:
                        print("requests.exceptions.ConnectionError")
                    else:

                        try:
                            json_output = r.json()
                        except json.decoder.JSONDecodeError:
                            print(r.text)

                        else:
                            if 'total' in json_output:
                                total_temp = json_output['total']
                                total_temp = int(total_temp)
                                if total_temp > 0:
                                    total = total_temp
                                    print('Total Set to-->' + str(total))
                                    if total > 1000 and radius > 300:
                                        radius = radius - 100
                                        check = True
                                    else:
                                        check = False
                print('Radius Set To-->' + str(radius))

                while offset <= total and offset<1000:

                    print("Fetching Dataset in Turn-->" + str(turn))
                    turn = turn + 1
                    url = 'https://api.yelp.com/v3/businesses/search?location='
                    url = url + city + '&limit=1&offset=' + str(offset)
                    url = url + '&latitude=' + str(lat) + '&longitude=' + str(lon) + '&radius='+str(radius)

                    br = 'Bearer ' + yelp_client
                    headers = {'Authorization': br}
                    try:
                        r = requests.get(url, headers=headers)
                        print(r.text)
                    except requests.exceptions.ConnectionError:
                        print("requests.exceptions.ConnectionError")
                    else:

                        try:
                            json_output = r.json()
                        except json.decoder.JSONDecodeError:
                            print(r.text)

                        else:

                            json.dump(json_output, fh)
                            fh.write('\n')
                            # fh.close()
                            offset = offset + 1

                    time.sleep(.5)


                print(r.text)
        fh.close()


def main():
    city = str(sys.argv[1])
    file_name = str(sys.argv[2])
    client_id = str(sys.argv[3])
    client_secret = str(sys.argv[4])
    yelp_client = authenticate_client(client_id, client_secret)
    search_data(yelp_client, city, file_name)


if __name__ == '__main__': main()
