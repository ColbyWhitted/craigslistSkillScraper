
import requests
from bs4 import BeautifulSoup

# This function returns a dictionary of word/word-count pairs

def countMultipleWordsInString(words, string):
    wordDictionary = {}
    for word in words:
        wordDictionary[word] = string.count(word)
    return wordDictionary


def craigslistSpider(url, words):

    sourceCode = requests.get(url)
    plainText = sourceCode.text
    soup = BeautifulSoup(plainText, 'html.parser')
    jobResults = soup.find(id="sortable-results")
    stringToSearch = ""
    for resultRow in jobResults.find_all('li', {"class": "result-row"}):
        link = resultRow.find('a')
        jobPostingUrl = link.get('href')
        jobPostingSourceCode = requests.get(jobPostingUrl)
        jobPostingPlainText = jobPostingSourceCode.text
        jobPostingSoup = BeautifulSoup(jobPostingPlainText, 'html.parser')
        jobPostingBodySoup = jobPostingSoup.find(id="postingbody")
        stringToSearch += jobPostingBodySoup.get_text().lower()
        print('Just grabbed ', jobPostingUrl)

    # The below creates a list of tuples (list of imutable lists) like this: [('thing', 'thing2')('etc')]
    wordOccurencesDictionary = countMultipleWordsInString(words, stringToSearch).items()
    wordOccurencesSortedDict = {}

    # for every tuple in wordOccurencesDictionary lets run the tuple through this Lambda which reverses the order of the tuple
    for key, value in sorted(wordOccurencesDictionary, key=lambda kv: (kv[1], kv[0]), reverse = True ):
        #everytime we do this lets add the new tuple to a dictionary as a key value pair
        wordOccurencesSortedDict[key] = value
    print(wordOccurencesSortedDict)


url = "https://sfbay.craigslist.org/d/software-qa-dba-etc/search/sof"
words = [' javascript ', ' ubuntu ', ' apache', ' nginx ', ' sql ', 'mysql', '.net ', ' laravel ', ' django ', ' php ', ' java ', ' python ', ' linux ', ' wordpress ', ' drupal ', ' c ', ' c# ', ' c++ ', ' react', ' js ', ' redux ', ' rust ', ' objective-c ', 'swift', 'angular', ' ruby ', ' scala ', ' r ', ' ror ']


craigslistSpider(url, words)