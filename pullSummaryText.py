from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import h5py

"""TODO
Pull the summary text and start parsing it into separate tables based on keywords
I want to separate out qualifications, required job skills, desired job skills, etc.
Keywords: Python, relational databases, non-relational databases, SQL, statistics, math, predictive modeling, machine learning
"""

class JobQual(object):
    def __init__(self, i, q):
        self.ID = i
        self.Qualification = q

class FullSummary(object):
    def __init__(self, i, s):
        self.ID = i
        self.Summary = s

def initialize():
    option = webdriver.ChromeOptions()
    option.add_argument("--incognito")
    browser = webdriver.Chrome(executable_path='C:/Users/taylor/PythonCourse/chromedriver.exe', chrome_options=option)
    browser.set_window_size(1920,1080)
    return browser
try:    
    browser = initialize()
    delay = 10
    jobSummaryTexts = []
    jobQuals = []
    columnsQual = ['ID','Qualification']
    columnsSumm = ['ID','Summary']
    fn = pd.read_hdf('C:/Users/taylor/PythonCourse/indeedProject/joblistings.h5')
    for i in range(len(fn['href'])):
        print('On item %i of %i' % (i,len(fn['href'])))
        browser.get(fn['href'][i])
        jobID = fn['ID'][i]
        try:
            WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID,'job_summary')))
        except TimeoutException:
            continue
        try:
            wholeTextElem = browser.find_element_by_id('job_summary')
            wholeText = wholeTextElem.text
        except TimeoutException:
            print('Errored on wholeText')
            continue
        try:
            listItems = wholeTextElem.find_elements_by_tag_name('li')
        except TimeoutException:
            print('Errored on listItems')
            continue
        for listItem in listItems:
            jobQuals.append(JobQual(jobID,listItem.text))
        jobSummaryTexts.append(FullSummary(jobID,wholeText))
except TimeoutException:
    print('For some reason this was unable to complete')
df = pd.DataFrame([[getattr(i,j) for j in columnsQual] for i in jobQuals], columns=columnsQual)
df.to_hdf('jobquals.h5','df',mode='w',format='table',data_columns=True)
df2 = pd.DataFrame([[getattr(i,j) for j in columnsSumm] for i in jobSummaryTexts], columns=columnsSumm)
df2.to_hdf('jobsummaries.h5','df2',mode='w',format='table',data_columns=True)