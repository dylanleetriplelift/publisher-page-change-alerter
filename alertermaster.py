import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import sys
import smtplib
from bundles import *


print('Beginning alerter script...')

# https://stackoverflow.com/questions/18510576/find-an-element-by-text-and-get-xpath-selenium-webdriver-junit
# Gets and returns the XPath of a given element, child_element is the handle of the desired element
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

# Generates and returns a comma separated list of CSS attributes and their values
# element is the handle of the desired element
def generate_css(element):
    css = ""
    # Iterates through list of attributes we want tested which is found in css.py
    for attr in attrs:
        if attr == 'marker-offset':
            css = (css + attr + ": " + element.value_of_css_property(attr)).lower()
        else:
            css = (css + attr + ": " + element.value_of_css_property(attr) + ', ').lower()
    return css

# Generates XPath diagnosis message when all ads were found
def xpathsdiagnosis(xpathstracker, num):
    sentence = ''
    if xpathstracker == []:
        sentence = 'All ad XPaths are as expected.'
    elif len(xpathstracker) == num:
        sentence = 'All ad XPaths have changed.'
    else:
        if len(xpathstracker) == 1:
            sentence = 'The XPath of the following ad has changed: ' + 'Ad #' + str(xpathstracker[0]+1) + ". The rest are as expected."
        else:
            sentence = "The XPaths of the following ads have changed: "
            for marker in xpathstracker:
                if marker == xpathstracker[-1]:
                    sentence = sentence + "and Ad #" + str(marker+1) + ". The rest are as expected."
                elif len(xpathstracker) == 2:
                    sentence = sentence + "Ad #" + str(marker+1) + " "
                else:
                    sentence = sentence + "Ad #" + str(marker+1) + ", "
    return sentence

# Generates CSS diagnosis message when all ads were found
def cssdiagnosis(csstracker, num):
    sentence = ''
    if csstracker == []:
        sentence = 'All ad CSS is as expected.'
    elif len(csstracker) == num:
        sentence = 'All ad CSS has changed.'
    else:
        if len(csstracker) == 1:
            sentence = 'The CSS of the following ad has changed: ' + 'Ad #' + str(csstracker[0]+1) + ". The rest is as expected."
        else:
            sentence = "The CSS of the following ads have changed: "
            for marker in csstracker:
                if marker == csstracker[-1]:
                    sentence = sentence + "and Ad #" + str(marker+1) + ". The rest is as expected."
                elif len(csstracker) == 2:
                    sentence = sentence + "Ad #" + str(marker+1) + " "
                else:
                    sentence = sentence + "Ad #" + str(marker+1) + ", "
    return sentence

# Reporting for sites with correct # of ads
def reporter(report, xpathstracker, badxpaths, csstracker, badcss):
    for line in report:
        print(line)
        if line == report[1] and line != 'All ad XPaths are as expected.':
            xpathcount = 0
            if len(xpathstracker) == len(badxpaths):
                print('The following XPath change(s) took place:')
                for badxpath in xpathstracker:
                    print('Ad #' + str(badxpath+1) + ': ' + badxpaths[xpathcount])
                    xpathcount += 1
        if line == report[2] and line != 'All ad CSS is as expected.':
            csscount = 0
            if len(csstracker) == len(badcss):
                print('The following CSS change(s) took place:')
                for badstyle in csstracker:
                    print('Ad #' + str(badstyle+1) + ': ' + badcss[csscount])
                    csscount += 1

# Reporting for sites with wrong # of ads
def reporter2(ads, less, matches, miaads, csschanges, xpathmismatches, num):

    print(str(len(ads)) + ' ads appeared when ' + str(num) + ' were expected.')

    if less:
        if len(ads) > 0:
            if len(matches) > 0:
                miatext = ''
                for miaad in miaads:
                    if miaads[-1] == miaad:
                        miatext = miatext + str(miaad + 1)
                    else:
                        miatext = miatext + str(miaad + 1) + ', '
                print('Only ' + str(len(matches)) + ' out of the ' + str(num) + ' expected ads were found on the page.')
                print('The following expected ad(s) could not be found: ' + miatext)
                csschangetext = ''
                csschangesreport = []
                for csschange in csschanges:
                    if csschanges[-1] == csschange:
                        csschangetext = csschangetext + str(csschange + 1)
                    else:
                        csschangetext = csschangetext + str(csschange + 1) + ', '
                    csschangesreport.append('Ad #' + str(csschange + 1) + ': ' + csschanges[csschange])
                if len(matches) == len(ads):

                    print('No unrecognized ads were detected.')
                    print('All found ads had correct XPaths.')
                    if len(csschanges) == 0:
                        print('All found ads had correct CSS.')
                    else:
                        if len(csschanges < len(matches)):
                            print('The following found ad(s) had CSS changes: ' + csschangetext)
                            print('The following CSS change(s) occured:')
                            for report in csschangesreport:
                                print(report)
                        else:
                            print('All found ads had CSS changes.')
                            print('The following CSS change(s) occured:')
                            for report in csschangesreport:
                                print(report)
                else:
                    print(str(num - len(ads)) + ' unrecognized ads were detected but could not be identified. These are their XPaths:')
                    for xpath in xpathmismatches:
                        print(xpathmismatches[xpath])
                    print('All found, expected ads had correct XPaths.')
                    if len(csschanges) == 0:
                        print('All found, expected ads had correct CSS.')
                    else:
                        if len(csschanges < len(matches)):
                            print('The following found, expected ad(s) had CSS changes: ' + csschangetext)
                            print('The following CSS change(s) occured:')
                            for report in csschangesreport:
                                print(report)
                        else:
                            print('All found, expected ads had CSS changes.')
                            print('The following CSS change(s) occurred: ')
                            for report in csschangesreport:
                                print(report)
            else:
                print('None of the expected ads could be found.')
                print(str(len(ads)) + ' unrecognized ads were detected but could not be identified. These are their XPaths:')
                for xpath in xpathmismatches:
                    print(xpathmismatches[xpath])
        else:
            print('No ads were detected whatsoever.')
    else:
        if len(matches) > 0:
            csschangetext = ''
            csschangesreport = []
            for csschange in csschanges:
                if csschanges[-1] == csschange:
                    csschangetext = csschangetext + str(csschange + 1)
                else:
                    csschangetext = csschangetext + str(csschange + 1) + ', '
                csschangesreport.append('Ad #' + str(csschange + 1) + ': ' + csschanges[csschange])
            if len(matches) == num:
                print('All ' + str(num) + ' expected ads were found on the page.')
                print(str(len(ads) - num) + ' unrecognized ads were detected but could not be identified. These are their XPaths:')
                for xpath in xpathmismatches:
                    print(xpathmismatches[xpath])
                print('All found, expected ads had correct XPaths.')
                if len(csschanges) == 0:
                    print('All found, expected ads had correct CSS.')
                else:
                    if len(csschanges) < len(matches):
                        print('The following found, expected ad(s) had CSS changes: ' + csschangetext)
                        print('The following CSS change(s) occured:')
                        for report in csschangesreport:
                            print(report)
                    else:
                        print('All found, expected ads had CSS changes.')
                        print('The following CSS change(s) occurred:')
                        for report in csschangesreport:
                            print(report)
            else:
                miatext = ''
                for miaad in miaads:
                    if miaads[-1] == miaad:
                        miatext = miatext + str(miaad + 1)
                    else:
                        miatext = miatext + str(miaad + 1) + ', '
                print('Only ' + str(len(matches)) + ' out of the ' + str(num) + ' expected ads were found on the page.')
                print('The following expected ad(s) could not be found: ' + miatext)
                print(str(len(ads) - num) + ' unrecognized ads were detected but could not be identified. These are their XPaths:')
                for xpath in xpathmismatches:
                    print(xpathmismatches[xpath])
                print('All found, expected ads had correct XPaths.')
                if len(csschanges) == 0:
                    print('All found, expected ads had correct CSS.')
                else:
                    if len(csschanges) < len(matches):
                        print('The following found, expected ad(s) had CSS changes: ' + csschangetext)
                        print('The following CSS change(s) occured:')
                        for report in csschangesreport:
                            print(report)
                    else:
                        print('All found, expected ads had CSS changes.')
                        print('The following CSS change(s) occurred:')
                        for report in csschangesreport:
                            print(report)
        else:
            print('None of the expected ads could be found.')
            print(str(len(ads)) + ' unrecognized ads were detected but could not be identified. These are their XPaths:')
            for xpath in xpathmismatches:
                print(xpathmismatches[xpath])

master = [
bundletwentytwowords,
bundlefoxnews,
bundlelivingly,
bundlehowstuffworks,
bundleweather,
bundledailymail,
bundleusatoday,
bundlebuzzfeed,
bundlethesaurus,
bundlelegacy,
bundlehistory,
bundlemlb,
bundlenypost,
bundlefoodnetwork,
bundlepostfun,
bundlecitationmachine
bundlelivestly,
bundleguardian,
bundlepopulareverything
]

# Custom wait function used to encourage page to load all ads
class every_element_present(object):
  """An expectation for checking that all expected elements of a certain
  selector are present on page based on a provided expected number

  locator - used to find the elements
  total - expected number of elements associated with locator
  returns the list of WebElements once all are present on page
  """
  def __init__(self, locator, total):
    self.locator = locator
    self.total = total

  def __call__(self, driver):
    elements = driver.find_elements_by_css_selector(self.locator)
    if self.total == len(elements):
        return elements
    else:
        return False

class AlertTest(unittest.TestCase):

    def setUp(self):
        # Chrome is used as standard testing browser
        self.driver = webdriver.Chrome()

    def test_ads(self):
        driver = self.driver
        # Window dimensions are set to 1366 x 768 as dimensions affect ad slot detection
        # 1366 x 768 is the most commonly used non-mobile window size so it is used as the standard
        driver.set_window_size(1366, 768)

        # List holding final report
        final = []
        # List holding expected ad # report
        numsfinal = []
        # List holding sites that timeout during wait function
        # List is to be used later to retry with repetition and longer wait time
        timeouts = []

        for test in master:
            print('')
            print(test[0] + ' is currently testing.')
            timed = False

            try:
                # Cookies are deleted before each new site as they may affect ad rendering
                driver.delete_all_cookies()
                # Opening domain from the first entry in the bundle
                driver.execute_script("window.location.href='"+ test[0].lower() + "'")

                # Using a custom wait to wait for the correct number of ads within the bucket to load
                # Times out after 30 seconds and is delayed until end of script by appending to timeouts list
                try:
                    # Allowing Selenium 30 seconds for the correct number of ads to load
                    wait = WebDriverWait(driver, 30)
                    ads = wait.until(every_element_present('div[id*="google_ads_iframe"]',len(test[1])))
                except:
                    timeouts.append(test)
                    timed = True

                if timed == False:
                    try:
                        # List for compiling final results
                        report = []

                        # Counting variable used to follow position when iterating through ads list
                        count = 0

                        # Positions are added to these lists if there is a change
                        self.xpathstracker = []
                        self.csstracker = []

                        # Changed XPaths and CSS are added to these lists and are later reported
                        self.badxpaths = []
                        self.badcss = []

                        # Variable used to check if correct number of ads exists
                        self.num = len(test[1])

                        # Checking to see if proper amount of ads are on page
                        # Ad total diagnosis is added to report list
                        report.append("All " + str(self.num) + " ad slots exist on page.")

                        # Marking which ads have XPath or CSS changes
                        # Incorrect XPaths or CSS are appended to badxpaths or badcss respectively and their indices are appended to the tracker lists for later reporting
                        # If the expected number of ads appeared, ad XPaths and CSS are generated and checked against the expected values with the same indices in the xpaths and css lists respectively
                        for ad in ads:
                            if generate_xpath(ad,"") != test[1][count]:
                                self.xpathstracker.append(count)
                                self.badxpaths.append(generate_xpath(ad,""))
                            if generate_css(ad) != test[2][count]:
                                self.csstracker.append(count)
                                self.badcss.append(generate_css(ad))
                            count += 1

                        # Adding XPath diagnosis to report
                        report.append(xpathsdiagnosis(self.xpathstracker, self.num))
                        report.append(cssdiagnosis(self.csstracker, self.num))

                        # Printing final results
                        reporter(report, self.xpathstracker, self.badxpaths, self.csstracker, self.badcss)

                        if (len(self.badxpaths) > 0) or (len(self.badcss) > 0):
                            final.append(test[0])
                    except Exception as e:
                        print('An error occured when testing. Analysis cannot be made.')
                        print('The following error occured:')
                        print(e)
                else:
                    print('Site failed to load all expected ads. Will attempt to test again after testing remaining sites.')

            except Exception as e:
                print('The following error occured when attempting to load this site:')
                print(e)
                print('Will attempt to test again after testing other sites.')
                timeouts.append(test)

        if len(timeouts) > 0:
            for test in timeouts:
                print('')
                print('Retrying ' + test[0])
                retries = 0
                success = False
                # Attempting to reload 3 times before giving up
                while retries < 3 and success == False:
                    try:
                        driver.delete_all_cookies()
                        driver.execute_script("window.location.href='"+ test[0].lower() + "'")
                        print('Site reloaded properly.')
                        success = True
                    except:
                        print('Reloading failure #' + str(retries+1))
                        retries += 1
                if success == False:
                    print('After retrying 3 times, script was still unable to fully load the site. Analysis cannot be completed for ' + test[0])
                else:
                    ads = None
                    retries = 0
                    success = False
                    # Attempting to find expected number of ads 3 times before giving up
                    while retries < 3 and success == False:
                        try:
                            driver.delete_all_cookies()
                            driver.execute_script("window.location.href='"+ test[0].lower() + "'")
                            wait = WebDriverWait(driver, 60)
                            ads = wait.until(every_element_present('div[id*="google_ads_iframe"]',len(test[1])))
                            print('Ads reloaded properly.')
                            success = True
                        except:
                            print('Ad loading failure #' + (str(retries+1)))
                            retries += 1

                    if success == True:
                        report = []
                        report.append("All " + str(self.num) + " ad slots exist on page.")

                        # Positions are added to these lists if there is a change
                        self.xpathstracker = []
                        self.csstracker = []

                        # Changed XPaths and CSS are added to these lists and are later reported
                        self.badxpaths = []
                        self.badcss = []

                        # Variable representing the correct number of ads
                        self.num = len(test[1])

                        count = 0
                        for ad in ads:
                            if generate_xpath(ad,"") != test[1][count]:
                                self.xpathstracker.append(count)
                                self.badxpaths.append(generate_xpath(ad,""))
                            if generate_css(ad) != test[2][count]:
                                self.csstracker.append(count)
                                self.badcss.append(generate_css(ad))
                            count += 1

                        report.append(xpathsdiagnosis(self.xpathstracker, self.num))
                        report.append(cssdiagnosis(self.csstracker, self.num))

                        # Printing final results
                        reporter(report, self.xpathstracker, self.badxpaths, self.csstracker, self.badcss)

                        if (len(self.badxpaths) > 0) or (len(self.badcss) > 0):
                            final.append(test[0])
                    else:
                        print('Failed to locate expected number of ads. Moving on.')
                        ads = driver.find_elements_by_css_selector('div[id*="google_ads_iframe"]')

                        self.num = len(test[1])

                        # Identifying as many ads as possible by matching expected XPaths to XPaths of found ads
                        matches = {}
                        xpathmismatches = {}
                        for ad in ads:
                            xpath = generate_xpath(ad,"")
                            if xpath in test[1]:
                                matches[test[1].index(xpath)] = ads.index(ad)
                            else:
                                xpathmismatches[ads.index(ad)] = xpath

                        # Seeing if more or less ads appeared than expected
                        less = True
                        if len(ads) > self.num:
                            less = False

                        # Distinguishing present and absent ads based on their expected positions
                        miaads = []
                        foundads = matches.keys()
                        foundadsmapped = matches.values()
                        for check in range(len(test[1])):
                            if check not in foundads:
                                miaads.append(check)

                        # Checking CSS of identified ads
                        csschanges = {}
                        for adpos in foundads:
                            css = generate_css(ads[matches[adpos]])
                            if css != test[2][adpos]:
                                csschanges[adpos] = css

                        reporter2(ads, less, matches, miaads, csschanges, xpathmismatches, self.num)
                        if (len(matches) != self.num) or (len(csschanges) > 0):
                            final.append(test[0])
                        numsfinal.append(test[0])

        print('')
        if len(final) > 0:
            domains = ''
            for domain in final:
                if domain == final[-1]:
                    domains = domains + domain
                else:
                    domains = domains + domain + ', '
            if len(numsfinal) == 0:
                print('Format changes were detected for the following site(s): ' + domains)
            else:
                print('Format changes were detected for the following site(s) with expected numbers of ads: ' + domains)
        else:
            if len(numsfinal) == 0:
                print('No format changes detected for any sites.')
            else:
                print('No format changes detected for sites with expected numbers of ads.')

        if len(numsfinal) > 0:
            domains = ''
            for domain in numsfinal:
                if domain == numsfinal[-1]:
                    domains = domains + domain
                else:
                    domains = domains + domain + ', '
            print('The following site(s) contained unexpected numbers of ads: ' + domains)
        else:
            print('All sites contained expected numbers of ads.')

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
