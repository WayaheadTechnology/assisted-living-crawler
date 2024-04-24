import sys
import yake
import json
from bs4 import BeautifulSoup
import requests
from time import sleep
from tqdm import tqdm


treeDic:dict = {}
indexedDic:dict = {}

def test():
    text = '''	(a) The DADS commissioner and the DSHS commissioner may appoint a manager or management team to manage and operate a community center in accordance with the Texas Health and Safety Code, §§534.038, 534.039, and 534.040. The DADS commissioner may delegate responsibility for appointing a manager or management team to the DSHS commissioner.
(b) A community center may request a hearing to appeal the commissioners' decision to appoint a manager or management team in accordance with 1 TAC Chapter 357, Subchapter I (relating to Hearings Under the Administrative Procedure Act). Requesting a hearing stays the appointment unless the commissioners based the appointment on a finding under §534.038(a)(2) or (4) of the Texas Health and Safety Code, which means the commissioners found that the community center or an officer or employee of the center misused state or federal money or endangers or may endanger the life, health, or safety of a person served by the center.'''
    language = "en"
    max_ngram_size = 3
    deduplication_thresold = 0.9
    deduplication_algo = 'seqm'
    windowSize = 1
    numOfKeywords = 20
    custom_kw_extractor = yake.KeywordExtractor()
    keywords = custom_kw_extractor.extract_keywords(text)

    for kw in keywords:
        print(kw)

    pass

def loadTreeDic(fName:str) -> dict:
    
    with open(fName,'r') as f:
        tempDic = json.load(f)
        f.close()
    return tempDic

def parseURL(urlStr:str):

    htmlStr:str = requests.get(urlStr).text
    parsedHTML = BeautifulSoup(htmlStr, 'html.parser')
    # finds the html tag that has
    readableText = ""
    if ".html" in urlStr:
        pass
    else:
        listOfRules = parsedHTML.find_all('ss')
        for item in listOfRules:
            readableText += item.getText()

    custom_kw_extractor = yake.KeywordExtractor()
    keyTerms = custom_kw_extractor.extract_keywords(readableText)
    indexedDic[urlStr] =  [i[0] for i in keyTerms] # gets first term in tuple

def saveIndexedURLS():
    with open('indexed.json', 'w') as f:
        json.dump(indexedDic, f,ensure_ascii=True,indent=4)
        f.close()
    

def indexURLs():
    saveIterations = 10
    currentIteration = 0
    for key,value in tqdm(treeDic.items()):
        if len(value) == 0:
            
            parseURL(key)
            currentIteration += 1
            if currentIteration%10 == 0:
                saveIndexedURLS()
        sleep(0.5)
    saveIndexedURLS()



if __name__ == '__main__':
    print("Wayahead Texas Gov regulation site Assisted living Scraper")
    if len(sys.argv) > 1:
        treeFileName = sys.argv[1]
        loadTreeDic(treeFileName)
    print("Scraper")
    # print("Test")
    # test()
    treeDic = loadTreeDic('tree.json')
    indexURLs()