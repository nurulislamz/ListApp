from selenium import webdriver
import unittest

from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

# browser.get('http://localhost:8000')

# assert 'To-Do' in browser.title

class NewVistitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        self.browser.get('http://localhost:8000')

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')

        # She is invited to enter a to-do item straight away
    
if __name__ == '__main__':
    unittest.main(warnings='ignore') 