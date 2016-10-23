import json
import requests
import time
import sys
import os


def authenticate_client(client_id, client_secret):
    payload = {}
    # payload = {'grant_type': 'client_credentials', 'client_id': 'I4lgSBkRb99Sj6O4jx2Y_A','client_secret':'9IXdh84mzhEOdAg5x5NcWav2mSki4FvPvoBp0WO6RLdBxsQLemMNZPV1EBEtOTMj'}
    start_time=time.time()
    payload = {'grant_type': 'client_credentials', 'client_id': client_id, 'client_secret': client_secret}
    r = requests.post("https://api.yelp.com/oauth2/token", data=payload)
    print(r.text)
    json_output = r.json()
    # print(json_output["access_token"])
    return json_output["access_token"],start_time

def set_output_directory():
    cwd = os.getcwd()
    newdir = cwd + '/output'
    if os.path.isdir(newdir) == False:
        os.mkdir(newdir)
    return (newdir)

def check_file_consistency(file,total_main):
    print('Filename-->'+file)
    f=open(file,'r')
    lines=len(f.readlines())
    diff=lines-total_main
    return diff,lines

def set_radius_range(yelp_client, city, yelp_file,lat,lon):

    total = 0
    radius = 800
    check = False
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
        except:
            print("Oops!", sys.exc_info()[0], "occured.")
        else:

            try:
                json_output = r.json()

            except:
                print("Oops!", sys.exc_info()[0], "occured.")
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
    return radius,total,r

def search_data(yelp_client, city, yelp_file,client_id, client_secret,start_time):
    newdir=set_output_directory()

    with open(yelp_file) as data_file:
        data = json.load(data_file)
        os.chdir(newdir)

        for a in range(0, len(data)):
            current_time=time.time()
            if current_time-start_time>7200:
                print("2 Hours Elapsed..Sleeping for Sometime")
                time.sleep(300)
                print("Waking Back")
                yelp_client,start_time=authenticate_client(client_id,client_secret)
            if data[a]["city"] == city:
                lat = data[a]["lat"]
                lon = data[a]["lon"]
                offset = 0
                turn = 1

                print('Search City ' + city + ' with Latitude ' + str(lat) + ' Longitude ' + str(lon))


                filestr = 'output_lat_' + str(lat) + 'long_' + str(lon) + '.json'

                check_file=os.path.isfile('./'+filestr)
                radius, total, r = set_radius_range(yelp_client, city, yelp_file, lat, lon)
                skip_file=False
                if check_file==False:
                    fh = open(filestr, 'a+')
                else:
                    diff,file_lines=check_file_consistency(filestr,total)

                    if diff>=(-20):
                        print("File Already Exist..Skip")
                        skip_file=True
                    elif diff<(-20):
                        print('Length of File-->'+str(file_lines))

                        print('File Exist but not consistent..Removing')
                        print('Filename-->'+filestr)
                        os.remove('./'+filestr)
                        fh = open(filestr, 'a+')

                if skip_file==False:
                    city_ptr = open('city_out.txt', 'a+')
                    city_ptr.write('Latitude-' + str(data[a]["lat"]) + 'Longitude-' + str(data[a]["lon"]) + '\n')
                    city_ptr.close()
                while offset <= total and offset < 1000 and skip_file==False:

                    fh = open(filestr, 'a+')
                    print("Fetching Dataset in Turn-->" + str(turn))
                    turn = turn + 1
                    url = 'https://api.yelp.com/v3/businesses/search?location='
                    url = url + city + '&limit=1&offset=' + str(offset)
                    url = url + '&latitude=' + str(lat) + '&longitude=' + str(lon) + '&radius=' + str(radius)

                    br = 'Bearer ' + yelp_client
                    headers = {'Authorization': br}
                    try:
                        r = requests.get(url, headers=headers)
                        print(r.text)
                    except requests.exceptions.ConnectionError:
                        print("requests.exceptions.ConnectionError")
                    except:
                        print("Oops!", sys.exc_info()[0], "occured.")
                    else:

                        try:
                            json_output = r.json()


                        except:
                            print("Oops!", sys.exc_info()[0], "occured.")
                        else:

                            json.dump(json_output, fh)
                            fh.write('\n')
                            # fh.close()
                            offset = offset + 1

                    time.sleep(.2)

                print(r.text)
        fh.close()



def main():
    city = str(sys.argv[1])
    file_name = str(sys.argv[2])
    client_id = str(sys.argv[3])
    client_secret = str(sys.argv[4])
    yelp_client,start_time = authenticate_client(client_id, client_secret)
    print(start_time)
    search_data(yelp_client, city, file_name,client_id, client_secret,start_time)


if __name__ == '__main__': main()
