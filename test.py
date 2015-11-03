import requests
import json

http_port = 'http://127.0.0.1:8080/'


def test(shouldbe, result, msg=None):
    if (result==shouldbe):
        print 'Success: was ', result
    else:
        print 'expected: ', shouldbe, '. was: ', result

j_obj = {'name':'barry', 'age': 21}
j_obj= json.dumps(j_obj)
obj1 = {'data': j_obj}
r = requests.post('http://localhost:8080/api/objects', data=obj1)
print r.text


r = requests.get('http://localhost:8080/api/objects/1')
print r.text
print r




#s = requests.Session()

# string of little tests
#r = s.get(http_port)
#test(500, r.status_code)

#r = s.post(http_port)
#print r.text
#test(200, r.status_code)

#r = s.get(http_port)
#print r.text
#test(200, r.status_code)

#r= s.get(http_port, headers={'Accept': 'application/json'})
#test (406, r.status_code)
