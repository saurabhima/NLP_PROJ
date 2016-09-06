import json
import pydot


def main():
    print('hello')
    # data=[]
    line = {}
    # fp = open('CH_venues.json', 'r')
    # for data in json.load(fp):
    #     if(data['city']=='Chicago'):
    #         lat=int(data['lat'])
    #         long=int(data['lon'])
    #         print(data['name'])
    fpbusiness = open('business.json', 'r')

    city_freq={}
    for line in fpbusiness.readlines():
        dict1 = json.loads(line.strip())
        if dict1['city'] in city_freq:
            #city_freq.has_key(dict1['city']) == True:
            city_freq[dict1['city']] = city_freq[dict1['city']] + 1
        else:
            city_freq[dict1['city']] = 1
    #self.graph = pydot.Dot(graph_type='')

    #print(city_freq)
    fh=open("City_freq_distribution.txt",'w')
    for ln in city_freq.keys():
        out=ln+'-'+str(city_freq[ln])
        print(out)
        fh.write(out+'\n')
    fh.close()



if __name__ == '__main__': main()
