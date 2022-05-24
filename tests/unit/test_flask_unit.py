from rezept_rest2 import update_post, insert_post
import unittest
import rezept_rest2



class TestCaseUpdate(unittest.TestCase):
    
    def test_update_rezept(self):
        update_post('spaghetti','tomaten, pasta, zwiebeln', 'wasser kochen, zwiebeln anduensten, tomaten beigeben')
        


# class TestCaseInsert(unittest.TestCase):

#     def test_create_rezept(self):
#         titel = "test1"
#         zutaten = "test2"
#         beschreibung = "test3"
#         rezept= update_post(titel, zutaten, beschreibung)
#         print(rezept)
   

if __name__ == '__main__':
    unittest.main()
