from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
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
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # He is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute(
            'placeholder'), 'Enter a to-do item')

        # He types "Buy three red apples" into a text box
        inputbox.send_keys('Buy three red apples')

        # When he hits enter, the page updates, and now the page lists:
        # "1: Buy three red apples" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = self.browser.find_elements_by_tag_name('tr')
        self.assertIn('1: Buy three red apples', [row.text for row in rows])
        self.assertIn('2: Make an apple pie', [row.text for row in rows])

        # There is still a text box inviting him to add another item.
        # He enters "Use an apple to make an apple-pie"
        self.fail('Finish the test!')

        # The page updates again, and now shows both items on his list

        # Cris wonders if the site will remember his list.
        # The he sees that the site has generated a unique URL for him.
        # There is some explanatory text to that effect

        # He visit that URL. His to-do list is still there

        # Satisfied, he goes back to his dinner


if __name__ == '__main__':
    unittest.main(warnings='ignore')
