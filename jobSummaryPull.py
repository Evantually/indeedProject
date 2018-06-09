from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

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
        return self.href
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
    pushToTable(results)
        
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
    prevUrl = ''
    while startNum <= 1000:
        countError = 0
        if startNum != 0:
            if startNum == 100:
                urlText = browser.current_url[:-2] + str(startNum)
            elif '&start=' in browser.current_url:
                urlText = browser.current_url[:-len(str(startNum))] + str(startNum)
            else:
                urlText = browser.current_url + '&start=' + str(startNum)
            browser.get(urlText)
        WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH,"//div[@class='lastRow row result clickcard']")))
        resultBoxes = browser.find_elements_by_xpath("//div[contains(@class,'row result clickcard')]")
        lastResultBoxID = browser.find_element_by_xpath("//div[@class='lastRow row result clickcard']").get_attribute('data-jk')
        for resultBox in resultBoxes:
            title, company, location, href, timePosted, jobID = '', '', '', '', '', ''
            jobID = resultBox.get_attribute('data-jk')
            try:
                if any(JobResult.ID == jobID for JobResult in results):
                    print('Continuing due to already being in list')
                    countError += 1
                    if countError >= 10:
                        startNum += 10
                        break
                    else:
                        continue
                titleAndHref = resultBox.find_element_by_tag_name('h2')
                title = titleAndHref.text
                title = title.replace('-new','')
                href = titleAndHref.find_element_by_tag_name('a').get_attribute('href')
                company = resultBox.find_element_by_class_name('company').text
                location = resultBox.find_element_by_class_name('location').text
                timePosted = resultBox.find_element_by_class_name('date').text
                if not any(post in timePosted for post in postTimes):
                    if 'days' in timePosted:
                        daysAgo = timePosted[:-9]
                    else:
                        print(timePosted)
                        daysAgo = timePosted[:1]
                    if int(daysAgo) >= 5:
                        startNum = 1001
                        print('Breaking due to days ago being 5')
                        break
                    print('We also made it through the int check')
                buildResult(jobTitle, title, company, location, href, timePosted, jobID)
                if jobID == lastResultBoxID:
                    startNum += 10
                    prevUrl = browser.current_url
                    print('Breaking due to last element')
                    break
            except:
                countError += 1
                print(countError)
                if countError >= 10:
                    startNum += 10
                    break
                print('Could not complete for this job ID', jobID)
        
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
    
def pushToTable(results):
    df = pd.DataFrame([[getattr(i,j) for j in columns] for i in results], columns=columns)
    print(df)
    df.to_hdf('joblistings.h5','df',mode='w',format='table',data_columns=True)

links = ['https://www.indeed.com']
jobTitles = ['data scientist','machine learning engineer','data analyst','researcher','software developer','software engineer']
postTimes = ['Just posted', 'Today']
columns=['searchedTitle','title','company','location','href','posted','ID']
titles = []
companies = []
locations = []
results = []
delay = 5
startNum = 0
initialize()

""" TODO
Set up machine learning algorithm to parse job summary
Generate cover letter text
"""