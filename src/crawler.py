from bs4 import BeautifulSoup
import requests
from treelib import Node, Tree
from time import sleep
import json

baseURL = "https://texreg.sos.state.tx.us/public/"
testURL = baseURL+"readtac$ext.TacPage?sl=R&app=9&p_dir=&p_rloc=&p_tloc=&p_ploc=&pg=1&p_tac=&ti=40&pt=1&ch=46&rl=1"
startURL = "https://texreg.sos.state.tx.us/public/readtac$ext.ViewTAC?tac_view=5&ti=40&pt=1&ch=46&sch=A&rl=Y"
regDomain = "texreg.sos.state.tx.us"

tree = Tree()
linksQueue = []
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
        if regDomain in currentLink:
            traversableLink.append(currentLink)
            #tree.create_node(currentLink,currentLink)
    
    return traversableLink


def generateURLWithBaseURL(url:str) -> str:
    if("http" in url):
        return url
    else:
        return baseURL+url


def crawl(startURL:str):
    # get html from start url
    htmlStr:str = getHtmlFromWeb(startURL)
    linksFromCurrentURL = extractLinksFromHTML(htmlStr)
    linksNotVisited = []
    for link in linksFromCurrentURL:
        currentNode = tree.get_node(link)
        # check if the node has been visited
        if currentNode is None:
            tree.create_node(link,link,parent=startURL)
            linksNotVisited.append(link)
    
            
    return linksNotVisited

def saveTree():
    with open('tree.json', 'w') as f:
        
        json.dump(tree.to_dict(),f,ensure_ascii=True,indent=4)
        f.close()
def saveQueue():
    with open('queue.json', 'w') as q:
        data = {"queue": linksQueue}
        json.dump(data,q,ensure_ascii=True,indent=4)
        q.close()

def saveSnapshot():
    print("Saving tree")
    saveTree()
    print("Saving queue")
    saveQueue()


if __name__ == '__main__':
    print("Wayahead Texas Gov regulation site Assisted living Crawler")
    tree.create_node(startURL, startURL) # creates the root nodes
    linksQueue.append(startURL)
    iterationsToSave = 10
    currentItirations = 0
    while linksQueue.count != 0:
        print(f"Links left in queue {len(linksQueue)}")
        linksNotVisited = crawl(startURL=linksQueue.pop())
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
    tree.show()
    
    saveSnapshot()