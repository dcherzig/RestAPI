from rezept_rest2 import delete_post, update_post, insert_post, get_id, get_post, delete_post
import unittest


class TestCaseUpdate(unittest.TestCase):
  def test_update_rezept(self):
    result = update_post('spaghetti','tomaten, pasta, zwiebeln', 'wasser kochen, zwiebeln anduensten, tomaten beigeben', '2')
    assert result == {'id': '2', 'titel': 'spaghetti', 'zutaten': 'tomaten, pasta, zwiebeln', 'beschreibung': 'wasser kochen, zwiebeln anduensten, tomaten beigeben'}


class TestCaseInsert(unittest.TestCase):
  def test_create_rezept(self):
    titel = "test1"
    zutaten = "test2"
    beschreibung = "test3"
    result = insert_post(titel, zutaten, beschreibung)
    assert result == True
   
class TestCaseGetID(unittest.TestCase):
  def test_get_rezept(self):
    result = get_id(2)
    assert result == (2, 'Pancakes', 'Eier, Milch, Mehl', 'Alles zusammenmischen, kurz stehen lassen und dann in die Pfanne geben')

  def test_get_rezept1(self):
    result = get_id(7)
    assert result == None


class TestCaseGetAll(unittest.TestCase):
  def test_get_all(self):
    result = get_post()
    print(len(result))


class TestCaseDelete(unittest.TestCase):
  def test_delete(self):
    result = delete_post(3)
    assert result == "Das Rezept mit der id: 3 wurde geloescht"





if __name__ == '__main__':
    unittest.main()
