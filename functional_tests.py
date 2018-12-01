from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Cris has heard about a cool online ToDo App.
        # He checks out its homepage
        self.browser.get('http://localhost:8000')
        
        # He notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')
        
        # He is invited to enter a to-do item straight away
        
        # He types "Buy three red apples" into a text box

        # When he hits enter, the page updates, and now the page lists:
        # "1: Buy three red apples" as an item in a to-do list

        # There is still a text box inviting him to add another item.
        # He enters "Use an apple to make an apple-pie"

        # The page updates again, and now shows both items on his list

        # Cris wonders if the site will remember his list.
        # The he sees that the site has generated a unique URL for him.
        # There is some explanatory text to that effect

        # He visit that URL. His to-do list is still there

        # Satisfied, he goes back to his dinner

if __name__ == '__main__':
    unittest.main(warnings = 'ignore')
