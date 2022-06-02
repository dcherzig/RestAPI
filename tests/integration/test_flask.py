import rezept_rest2
import unittest

class TestCaseGet(unittest.TestCase):

    def setUp(self):
        rezept_rest2.app.testing = True
        self.app = rezept_rest2.app.test_client()

    def test_get_route(self):
        response = self.app.get('/rezepte')
        assert response.status_code == 200
                    
    def test_content(self):
        response = self.app.get('/rezepte')
        assert response.content_type== "application/json"

    def test_get_routeRezept(self):
        response = self.app.get('/rezept/1')
        assert response.status_code == 200
        assert response.content_type== "application/json"
        assert response.get_data() == b'[1,"Risotto","Reis, Bouillon, Zwiebeln","Reis anduensten, abloeschen mit Bouillon, koecheln lassen"]\n'
        
    def test_get_routeRezept1(self):
        response = self.app.get('/rezept/500')
        assert response.status_code== 404

class TestCasePut(unittest.TestCase): 
    def setUp(self):
        rezept_rest2.app.testing = True
        self.app = rezept_rest2.app.test_client()

    def test_put_route(self):
        response = self.app.put('/rezept/2', data={"titel": "tete", "zutaten": "hdhd", "beschreibung": "jfhf", "id": 2}) 
        assert response.get_data() == b'Rezept wurde erfolgreich geaendert'

    def test_put_route1(self):
        response = self.app.put('/rezept/1', data={"zutaten": "hdhd", "beschreibung": "jfhf"}) 
        assert response.status_code == 400   

class TestCasePost(unittest.TestCase): 
    def setUp(self):
        rezept_rest2.app.testing = True
        self.app = rezept_rest2.app.test_client()

    def test_post_route(self):
        response = self.app.post('/rezepte', data=dict(titel='test', zutaten='test', beschreibung='test'))  
        assert response.get_data() == b'Rezept wurde erfolgreich kreiert'
        assert response.status_code == 201
    
    def test_post_route1(self):
        response = self.app.post('/rezepte', data=dict(titel='test', zutaten='test'))  
        assert response.get_data() == b'Fehler beim Hinzufuegen des Rezepts'
        assert response.status_code == 400
            
       
class TestCaseDelete(unittest.TestCase): 
    def setUp(self):
        rezept_rest2.app.testing = True
        self.app = rezept_rest2.app.test_client()

    def test_delete_route(self):
        response = self.app.delete('/rezept/2')  
        assert response.status_code == 200
        assert response.get_data() == b'Das Rezept mit der id: 2 wurde geloescht'
    
    def test_delete_route1(self):
        response = self.app.delete('/rezept/500')  
        assert response.status_code == 400
        assert response.get_data() == b'Fehler beim Loeschen des Rezepts'


if __name__ == '__main__':
    unittest.main()




