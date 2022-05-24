import rezept_rest2
import json
import unittest

class TestCaseGet(unittest.TestCase):

    def setUp(self):
        rezept_rest2.app.testing = True
        self.app = rezept_rest2.app.test_client()

    def test_get_route(self):
        response = self.app.get('/rezepte')
        assert response.status_code == 200
        #print(response.get_data())
        assert len(response.get_json()) == 3
        
    
    def test_content(self):
        response = self.app.get('/rezepte')
        assert response.content_type== "application/json"

    def test_get_routeRezept(self):
        response = self.app.get('rezept/1')
        assert response.status_code == 200
        assert len(response.get_json()) == 4
        #assert response.content_type== "application/json"
        #assert response.get_data()==b'[1,"Risotto","Reis, Bouillon, Zwiebeln","Reis anduensten, abloeschen mit Bouillon, koecheln lassen"]\n'
        #assert json.loads(response.get_data()) == [1, 'Risotto', 'Reis, Bouillon, Zwiebeln', 'Reis anduensten, abloeschen mit Bouillon, koecheln lassen']


class TestCasePut(unittest.TestCase): 
    def setUp(self):
        rezept_rest2.app.testing = True
        self.app = rezept_rest2.app.test_client()

    def test_put_route(self):
        response = self.app.put('/rezept/2', data={"titel": "tete", "zutaten": "hdhd", "beschreibung": "jfhf", "id": 1}) 
        print(response.get_data())
        

class TestCasePost(unittest.TestCase): 
    def setUp(self):
        rezept_rest2.app.testing = True
        self.app = rezept_rest2.app.test_client()

    def test_post_route(self):
        response = self.app.post('/rezepte', data=dict(titel='test', zutaten='test', beschreibung='test'))  
        print(response.get_data()) #bad request
        
       
class TestCaseDelete(unittest.TestCase): 
    def setUp(self):
        rezept_rest2.app.testing = True
        self.app = rezept_rest2.app.test_client()

    def test_delete_route(self):
        response = self.app.delete('/rezept/2')  
        print(response.get_data())
        assert response.status_code == 200
        assert response.get_data() == b'Das Rezept mit der id: 2 wurde geloescht'


if __name__ == '__main__':
    unittest.main()




