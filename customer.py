import requests

url = 'http://130.127.133.105:8000/'
result = requests.get(url+'get_inventory_list')
Dict = dict(result.json())
for elem in Dict:
    print(elem)
    for stuff in Dict[elem]:
        print(stuff)
        tmpurl = url+'request_item_photo/'+str(stuff['pk'])+'/'
        print(tmpurl)
        tmp = requests.get(tmpurl)
        print(tmp)
r = requests.get(url+'request_item_photo/1/')
for i in range(100):
    s = requests.get(url+'request_item_photo/2/')
    if(s == r):
        break
print(i)

