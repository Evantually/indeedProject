from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import pickle

class JobResult(object):
    def __init__(self, s, t, c, l, h, p, i):
        self.searchedTitle = s
        self.title = t
        self.company = c
        self.location = l
        self.href = h
        self.posted = p
        self.ID = i
    def getSearch(self):
        return self.searchedTitle
    def getTitle(self):
        return self.title
    def getCompany(self):
        return self.company
    def getLocation(self):
        return self.location
    def getHref(self):
        return self.Href
    def getPosted(self):
        return self.posted
    def getID(self):
        return self.ID

def initialize():
    option = webdriver.ChromeOptions()
    option.add_argument("--incognito")
    browser = webdriver.Chrome(executable_path='C:/Users/taylor/PythonCourse/chromedriver.exe', chrome_options=option)
    browser.set_window_size(1920,1080)
    for link in links:    
        main(browser, link, startNum)

def main(browser, link, startNum):
    for jobTitle in jobTitles:
        startNum = 0
        browser.get(link)
        WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.NAME, "q")))
        searchJob(browser, jobTitle)
        checkPopup(browser)
        checkSort(browser)
        gatherResults(browser, startNum, jobTitle)
        
def searchJob(browser, jobTitle):
    modJobTitle = editJobTitle(jobTitle)
    searchBoxElems = browser.find_elements_by_tag_name('input')
    for searchBoxElem in searchBoxElems:
        if searchBoxElem.get_attribute('name') == 'q':
            searchBoxElem.send_keys(jobTitle)
    checkLocationBlank(browser)
    submitButtons = browser.find_elements_by_tag_name('button')
    for button in submitButtons:
        if button.text == 'Find Jobs':
            button.click()
            break
    WebDriverWait(browser, delay).until(EC.url_contains(modJobTitle))
    
def gatherResults(browser, startNum, jobTitle):
    resultBoxes = browser.find_elements_by_xpath("//div[@class='row result clickcard']")
    lastResultBoxID = browser.find_element_by_xpath("//div[@class='lastRow row result clickcard']").get_attribute('data-jk')
    numResults = len(resultBoxes)
    counter = 0
    for resultBox in resultBoxes:
        title, company, location, href, timePosted, jobID = '', '', '', '', '', ''
        jobID = resultBox.get_attribute('data-jk')
        print(jobID)
        if any(JobResult.ID == jobID for JobResult in results):
            continue
        if jobID == lastResultBoxID:
            #I do not currently know what the issue is with the last result erroring here.
            continue
        titleAndHref = resultBox.find_element_by_tag_name('h2')
        title = titleAndHref.text
        title = title.replace('-new','')
        print(title)
        href = titleAndHref.find_element_by_tag_name('a').get_attribute('href')
        print(href)
        company = resultBox.find_element_by_class_name('company').text
        print(company)
        location = resultBox.find_element_by_class_name('location').text
        print(location)
        timePosted = resultBox.find_element_by_class_name('date').text
        print(timePosted)
        buildResult(jobTitle, title, company, location, href, timePosted, jobID)
        if counter == numResults:
            browser.get(browser.current_url + '&start=' + startNum)
            startNum += 10
            gatherResults(browser, startNum, jobTitle)
        
def checkLocationBlank(browser):
    inputElems = browser.find_elements_by_tag_name('input')
    for locationElem in inputElems:
        if locationElem.get_attribute('name') == 'l':
            locationElem.send_keys(Keys.CONTROL + 'a')
            locationElem.send_keys(Keys.DELETE)

def checkPopup(browser):
    popupElems = browser.find_elements_by_tag_name('button')
    for popupElem in popupElems:
        if popupElem.get_attribute('id') == 'prime-popover-close-button':
            popupElem.click()            
            
def checkSort(browser):
    try: 
        WebDriverWait(browser, delay).until(EC.url_contains('sort=date'))
    except: 
        browser.get(browser.current_url + '&sort=date')
            
def editJobTitle(jobTitle):
    jobTitleSplit = jobTitle.split()
    numWordsJobTitle = len(jobTitleSplit)
    newJobTitle = ''
    for wordNum in range(numWordsJobTitle):
        if wordNum == numWordsJobTitle:
            newJobTitle = newJobTitle + jobTitleSplit[wordNum]
        elif wordNum == 0:
            newJobTitle = jobTitleSplit[wordNum]
        else:
            newJobTitle = newJobTitle + '+' + jobTitleSplit[wordNum]
    return newJobTitle

def buildResult(jobTitle, title, company, location, href, timePosted, jobID):
    results.append(JobResult(jobTitle, title, company, location, href, timePosted, jobID))
    print(results)

links = ['https://www.indeed.com']
jobTitles = ['data scientist','machine learning engineer','data analyst','researcher','software developer','software engineer']
titles = []
companies = []
locations = []
results = []
delay = 5
startNum = 0
initialize()

""" TODO
Fix last result issue
Compile all results into database
Set up machine learning algorithm to parse job summary
Generate cover letter text
"""