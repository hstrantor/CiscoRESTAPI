### unit test script to test basic functionality
### of my REST API

import unittest
import json
import requests

url = 'http://127.0.0.1:8080/api/objects'

class TestPOST(unittest.TestCase):

    curr_uid = 0
    def setUp(self):
        pass        

    def testPostNewObj(self):
        new_obj = {'name': 'joe', 'age': 73}
        jnew_obj = json.dumps(new_obj)
        post_data = {'data': jnew_obj}
        r = requests.post(url, data=post_data)
        self.assertEquals(new_obj['name'], r.json()['name'])
        self.assertEquals(new_obj['age'], r.json()['age'])
        self.assertTrue(r.json()['uid'] != None)
        curr_uid = r.json()['uid']

    def testDuplicatePost(self):
        new_obj = {'name': 'joe', 'age': 73}
        jnew_obj = json.dumps(new_obj)
        post_data = {'data': jnew_obj}
        r = requests.post(url, data=post_data)
        self.assertEquals(new_obj['name'], r.json()['name'])
        self.assertEquals(new_obj['age'], r.json()['age'])
        self.assertTrue(r.json()['uid'] != None)
        self.assertFalse(curr_uid == r.json()['uid'])



if __name__ == '__main__':
    unittest.main()
