import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import sys
import smtplib


print('Beginning finder script...')
print('Attempting to return XPaths and CSS rules of ad slots...')

def generate_xpath(child_element,current):
    child_tag = child_element.tag_name
    if child_tag == 'html':
        return "/html[1]"+current
    parent_element = child_element.find_element_by_xpath('..')
    children_elements = parent_element.find_elements_by_xpath("*")
    count = 0
    i = 0
    while i < len(children_elements):
        children_element = children_elements[i]
        children_element_tag = children_element.tag_name
        if child_tag == children_element_tag:
            count += 1
        if child_element == children_element:
            return generate_xpath(parent_element, "/" + child_tag + "[" + str(count) + "]" + current)
        i+=1
    return None

def generate_css(element):
    css = ""
    # Iterates through list of attributes we want tested which is found in css.py
    for attr in attrs:
        if attr == 'marker-offset':
            css = (css + attr + ": " + element.value_of_css_property(attr)).lower()
        else:
            css = (css + attr + ": " + element.value_of_css_property(attr) + ', ').lower()
    return css

attrs = ['font-family','font-size','font-weight','font-style','color',
'text-transform','text-decoration','letter-spacing','word-spacing',
'line-height','text-align','vertical-align','direction','background-color',
'background-image','background-repeat','background-position',
'background-attachment','opacity','top','right','bottom',
'left','margin-top','margin-bottom','padding-top','padding-right','padding-bottom','padding-left',
'border-top-width','border-right-width','border-bottom-width',
'border-left-width','border-top-color','border-right-color',
'border-bottom-color','border-left-color','border-top-style',
'border-right-style','border-bottom-style','border-left-style','position','visibility','z-index','overflow-x','overflow-y','white-space',
'clip','float','clear','cursor','list-style-image','list-style-position',
'list-style-type','marker-offset'];

domains = ['https://populareverything.com/can-you-guess-these-celebrities-based-off-their-throwback-photo/']

class AlertTest(unittest.TestCase):

    def setUp(self):
        # Chrome is used as standard testing browser
        self.driver = webdriver.Chrome()

    def test_ads(self):
        driver = self.driver
        # Window dimensions are set to 1366 x 768 as dimensions affect ad slot detection
        # 1366 x 768 is the most commonly used non-mobile window size so it is used as the standard
        driver.set_window_size(1366, 768)

        for domain in domains:
            print('Attempting to find XPaths and CSS from ' + domain)

            try:
                driver.delete_all_cookies()
                driver.execute_script("window.location.href='"+ domain.lower() + "'")

                try:
                    wait = WebDriverWait(driver, 30)
                    time.sleep(20)
                    ads = driver.find_elements_by_css_selector('div[id*="google_ads_iframe"]')

                    if len(ads) > 0:
                        print(str(len(ads)) + ' ad(s) detected.')

                        xpaths = ""
                        css = ""

                        for ad in ads:
                            if ads[-1] == ad:
                                xpaths = xpaths + "'" + generate_xpath(ad,"") + "'"
                                css = css + "'" + generate_css(ad) + "'"
                            else:
                                xpaths = xpaths + "'" + generate_xpath(ad,"") + "', "
                                css = css + "'" + generate_css(ad) + "', "

                        print('Below are the detected XPaths:')
                        print(xpaths)
                        print('Below is the detected CSS:')
                        print(css)

                    else:
                        print('No ads were located on the page.')

                except Exception as e:
                    print('The following error occured while attempting to find XPaths and CSS:')
                    print(e)

            except Exception as e:
                print('The following error occured when attempting to load this site:')
                print(e)

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
