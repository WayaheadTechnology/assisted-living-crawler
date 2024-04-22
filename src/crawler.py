from bs4 import BeautifulSoup
import requests
from time import sleep
import json
import sys

baseURL = "https://texreg.sos.state.tx.us/public/"
testURL = baseURL+"readtac$ext.TacPage?sl=R&app=9&p_dir=&p_rloc=&p_tloc=&p_ploc=&pg=1&p_tac=&ti=40&pt=1&ch=46&rl=1"
startURL = "https://texreg.sos.state.tx.us/public/readtac$ext.ViewTAC?tac_view=5&ti=40&pt=1&ch=46&sch=A&rl=Y"
regDomain = "texreg.sos.state.tx.us"


dotNotGoPaths = ["https://texreg.sos.state.tx.us/public/readtac$ext.ViewTAC?tac_view=3&ti=40&pt=5",
                 "https://texreg.sos.state.tx.us/public/readtac$ext.ViewTAC?tac_view=3&ti=40&pt=12",
                 "https://texreg.sos.state.tx.us/public/readtac$ext.ViewTAC?tac_view=3&ti=40&pt=15",
                 "https://texreg.sos.state.tx.us/public/readtac$ext.ViewTAC?tac_view=3&ti=40&pt=17",
                 "https://texreg.sos.state.tx.us/public/readtac$ext.ViewTAC?tac_view=3&ti=40&pt=19",
                 "https://texreg.sos.state.tx.us/public/readtac$ext.ViewTAC?tac_view=3&ti=40&pt=20",
                 "https://texreg.sos.state.tx.us/public/readtac$ext.ViewTAC?tac_view=3&ti=40&pt=21",
                 "https://texreg.sos.state.tx.us/public/readtac$ext.ViewTAC?tac_view=3&ti=40&pt=22",
                 "https://texreg.sos.state.tx.us/public/readtac$ext.viewtac",
                 "http://www.sos.texas.gov/",
                 "http://www.sos.texas.gov/texreg/index.shtml",
                 "http://www.sos.texas.gov/tac/index.shtml",
                 "http://www.sos.texas.gov/open/index.shtml",
                 ""
                 ]
# tree = Tree()
linksQueue = []
# list of visited links
visitedList = []
# alternative to tree
linkDic = {}
def getHtmlFromWeb(inputURL:str) -> str:

    #print(f"Should get a document from url: {inputURL}")
    req = requests.get(inputURL)
    return req.text
    # print(req.text)
    
def extractLinksFromHTML(htmlStr:str):
    parsedHTML = BeautifulSoup(htmlStr, 'html.parser')    
    linksList = parsedHTML.find_all('a', href=True)
    #print(f"Number of links: {len(linksList)}")
    return getTraversableLinks(linkList=linksList)

def parseHTML(htmlStr: str, currentURL:str):
    #print("Parsing from obj")
    parsedHTML = BeautifulSoup(htmlStr, 'html.parser')
    
    linksList = parsedHTML.find_all('a', href=True)
    #print(f"Number of links: {len(linksList)}")
    getTraversableLinks(linkList=linksList)

def getTraversableLinks(linkList:list) -> list:
    traversableLink:list = []
    for link in linkList:
        currentLink = generateURLWithBaseURL(link['href'])
        try:
            textInTag = link['name']
        except:
            textInTag = ""
        if (regDomain in currentLink) and (currentLink not in linksQueue):
            if not((textInTag == "Prev Rule") or (textInTag == "Next Rule")):
                if(currentLink not in dotNotGoPaths):
                    traversableLink.append(currentLink)
            #tree.create_node(currentLink,currentLink)
    
    return traversableLink


def generateURLWithBaseURL(url:str) -> str:
    if("http" in url):
        return url
    else:
        if(url[0] == "/"):
            return baseURL+url[1:]
        else:
            return baseURL+url


def crawl(rootURL:str):
    # get html from root url
    htmlStr:str = getHtmlFromWeb(rootURL)
    linksFromCurrentURL = extractLinksFromHTML(htmlStr)
    visitedList.append(rootURL) # add visited url
    linksNotVisited = []
    # Check if the dic has that entry if not initilze it to an empty array
    try:
        linkDic[rootURL]
    except:
        linkDic[rootURL] = []
    
    for link in linksFromCurrentURL:
        # check if the link has been visited or is a banned link
        if (link not in visitedList) and (link not in dotNotGoPaths):
            # add the link to the dictionary
            linkDic[rootURL].append(link)
            linksNotVisited.append(link)
    
    return linksNotVisited

def saveTree():
    with open('tree.json', 'w') as f:
        json.dump(linkDic,f,ensure_ascii=True,indent=4)
        f.close()
def saveQueue():
    with open('queue.json', 'w') as q:
        data = {"queue": linksQueue}
        json.dump(data,q,ensure_ascii=True,indent=4)
        q.close()
def saveVisitedList():
    with open('visited.json', 'w') as v:
        data = {"visited": visitedList}
        json.dump(data,v,ensure_ascii=True,indent=4)
        v.close()

def saveSnapshot():
    print("Saving tree")
    saveTree()
    print("Saving queue")
    saveQueue()
    print("Sasving Visited list")
    saveVisitedList()

def getQueueFromFile(fName:str) -> list:
    # loads the queue from a file name
    print(f"Loading queue from file {fName}")
    data = {}
    newQueue = []
    with open(fName,'r') as queueFile:
        data = json.load(queueFile)
        queueFile.close()
    try:
        newQueue = data['queue']
    except:
        newQueue = []
    return newQueue

def getTreeFromFile(fName:str)-> dict:
    print(f"Loading tree from file {fName}")
    data = {}
    
    with open(fName,'r') as queueFile:
        data = json.load(queueFile)
        queueFile.close()
    return data

def getVisitedFromFile(fName:str) -> list:
    # loads the visited array from a file name
    print(f"Loading Visited from file {fName}")
    data = {}
    newVisited = []
    with open(fName,'r') as queueFile:
        data = json.load(queueFile)
        queueFile.close()
    try:
        newVisited = data['visited']
    except:
        newVisited = []
    return newVisited


if __name__ == '__main__':
    print("Wayahead Texas Gov regulation site Assisted living Crawler")
    if len(sys.argv) > 1:
        inFile = sys.argv[1]
        inFile2 = sys.argv[2]
        inFile3 = sys.argv[3]
        linksQueue = getQueueFromFile(inFile)
        linkDic = getTreeFromFile(inFile2)
        visitedList = getVisitedFromFile(inFile3)
    else:
        print("Starting from start URL since no queue file was loaded")
        linksQueue.append(startURL)
    iterationsToSave = 10
    currentItirations = 0
    while len(linksQueue) != 0:
        print(f"In queue {len(linksQueue)}, Visited: {len(visitedList)}")
        linksNotVisited = crawl(rootURL=linksQueue.pop(-1))
        linksQueue.extend(linksNotVisited) # addes links not visited to the queue
        sleep(1)
        if currentItirations == iterationsToSave:
            saveSnapshot()
            currentItirations = 0
        else:
            currentItirations += 1

    # htmlStr:str = getHtmlFromWeb(startURL)
    # parseHTML(htmlStr=htmlStr)
    print("Finished traverse")
    
    saveSnapshot()