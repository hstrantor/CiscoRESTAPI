### unit test script to test basic functionality
### of my REST API

import unittest
import json
import requests

#url = 'http://127.0.0.1:80/api/objects'
#url = 'http://ec2-52-32-119-107.us-west-2.compute.amazonaws.com:80/api/objects'
url = 'http://172.31.25.94/api/objects'

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
        self.assertFalse(self.curr_uid == r.json()['uid'])

    def testUIDUnique(self):
        new_obj = {'X': 5}
        post_data = {'data':json.dumps(new_obj)}
        r = requests.post(url, data=post_data)
        id1 = r.json()['uid']

        new_obj = {'Y': 6}
        post_data = {'data':json.dumps(new_obj)}
        r = requests.post(url, data=post_data)
        self.assertFalse(id1==r.json()['uid'])



class TestDELETE(unittest.TestCase):
    """Test for DELETE requests.
    DELETE requests send the site url with the appended uid
    of the object to delete. Must be indempotent.
    If exists: deleted, returns nothing
    else: return error msg
    """

    new_obj = None
    def setUp(self):
        self.new_obj = {'testing': 'DELETE', 'made_by': 'setup'}
        jnew_obj = json.dumps(self.new_obj)
        post_data = {'data': jnew_obj}
        r = requests.post(url, data=post_data)
        self.new_obj['uid'] = r.json()['uid']
       
    def testDeleteExisting(self):
        r = requests.delete(url+'/'+self.new_obj['uid'])
        # check nothing was returned
        self.assertEquals(len(r.text), 0)
        # check object was deleted
        r = requests.get(url+'/'+self.new_obj['uid'])
        self.assertEquals(r.json()['message'], "Object does not exist") 

    def testDeleteNonExisting(self):
        r = requests.delete(url+'/'+self.new_obj['uid'])
        r = requests.delete(url+'/'+self.new_obj['uid'])
        r = requests.delete(url+'/'+self.new_obj['uid'])
        r = requests.get(url+'/'+self.new_obj['uid'])
        self.assertEquals(r.json()['message'], "Object does not exist") 



class TestPUT(unittest.TestCase):

    uids = {}
    def setUp(self):
        a = {"a": 2, "aa":3, "aaa":[1,2,3]}
        b = {"b": 5}
        c = {}
        d = {"dee":'c', "school": "achds"}
        post_data = {'data': json.dumps(a)}
        r = requests.post(url, data=post_data)
        self.uids['a'] = r.json()['uid']
        post_data = {'data': json.dumps(b)}
        r = requests.post(url, data=post_data)
        self.uids['b'] = r.json()['uid']
        post_data = {'data': json.dumps(c)}
        r = requests.post(url, data=post_data)
        self.uids['c'] = r.json()['uid']
        post_data = {'data': json.dumps(d)}
        r = requests.post(url, data=post_data)
        self.uids['d'] = r.json()['uid']

    def testPut(self):
        # update obj uid a
        updated_obj = {'name':'johnson', 'age': 3, 'alive': True}
        j_obj = json.dumps(updated_obj)
        put_data = {'data': j_obj}
        r = requests.put(url+'/'+self.uids['a'], data=put_data)
        # make sure returned obj has uid
        self.assertTrue( "uid" in r.json())
        # make sure returned obj has same uid
        self.assertEquals(self.uids['a'], r.json()['uid'])
        # updated obj shouldn't have any of the old data
        self.assertFalse( 'a' in r.json())
        self.assertFalse( 'aa' in r.json())
        self.assertFalse( 'aaa' in r.json())
        # updated obj should have all the new data
        self.assertTrue( r.json()['name'] == updated_obj['name'])
        self.assertTrue( r.json()['age'] == updated_obj['age'])
        self.assertTrue( r.json()['alive'] == updated_obj['alive'])


class TestGET(unittest.TestCase):

    uids = {}
    def setUp(self):
        a = {"a": 2, "aa":3, "aaa":[1,2,3]}
        b = {"b": 5}
        c = {}
        d = {"dee":'c', "school": "achds"}
        post_data = {'data': json.dumps(a)}
        r = requests.post(url, data=post_data)
        self.uids['a'] = r.json()['uid']
        post_data = {'data': json.dumps(b)}
        r = requests.post(url, data=post_data)
        self.uids['b'] = r.json()['uid']
        post_data = {'data': json.dumps(c)}
        r = requests.post(url, data=post_data)
        self.uids['c'] = r.json()['uid']
        post_data = {'data': json.dumps(d)}
        r = requests.post(url, data=post_data)
        self.uids['d'] = r.json()['uid']
    
    # TODO need delete or start script to test this
    #def testGETall(self):
    #    r = requests.get(url)
    #    # test returns list of correct number of urls
    #    self.assertTrue( len(r.json()) == 10)

    def testGET(self):
        r = requests.get(url+'/'+self.uids['a'])
        print r
        print r.text
        print r.json()
        
        self.assertEquals(r.json()['uid'], self.uids['a'])
        self.assertEquals(r.json()['a'], 2)
        self.assertEquals(r.json()['aa'], 3)
        self.assertEquals(r.json()['aaa'],[1,2,3])





if __name__ == '__main__':
    unittest.main()
