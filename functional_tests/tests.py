from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_for_one_user(self):
        # Cris has heard about a cool new online ToDo App.
        # He checks out its homepage
        self.browser.get(self.live_server_url)

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
        self.wait_for_row_in_list_table('1: Buy three red apples')

        # There is still a text box inviting him to add another item.
        # He enters "Use an apple to make an apple-pie"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use an apple to make an apple-pie')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on his list
        self.wait_for_row_in_list_table('2: Use an apple to make an apple-pie')
        self.wait_for_row_in_list_table('1: Buy three red apples')

        # Satisfied, he goes back to his dinner

    def test_multiple_users_can_starts_lists_at_different_urls(self):
        # Cris starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy three red apples')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy three red apples')

        # He notices that his list has a unique URL
        cris_list_url = self.browser.current_url
        self.assertRegex(cris_list_url, '/lists/.+')

        # Now a new user, Alessia, comes along to the site.

        # We use a new browser session to make sure that no information
        # of Cris is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Alessia visits the home page. There is no sign of Cris's
        # list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy three red apples', page_text)
        self.assertNotIn('make an apple-pie', page_text)

        # Alessia starts a new list by entering a new item. She
        # is less interesting than Cris...
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy some bread')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy some bread')

        # Alessia gets hers own unique URL
        alessia_list_url = self.browser.current_url
        self.assertRegex(alessia_list_url, '/lists/.+')
        self.assertNotEqual(alessia_list_url, cris_list_url)

        # Again, there is no trace of Cris's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy three red apples', page_text)
        self.assertIn('Buy some bread', page_text)

        # Satisfied, they both go back to sleep
