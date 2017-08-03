import requests
import bs4
import exception
from re import sub

class Problem(object):
    def __init__(self, problem):
        self.problemCode = problem.upper()
        self.problemURL = 'https://www.spoj.com/problems/' + self.problemCode + '/'
        resp = requests.get(self.problemURL)
        soup = bs4.BeautifulSoup(resp.text, 'lxml')

        if 'In a few seconds you will be redirected' in resp.text:
            raise exception.InvalidProblem('The given problem is invalid')

        self.problemName = soup.find('h2', {'id': 'problem-name'}).get_text()
        self.problemName = sub(r'.*- ', '', self.problemName)

        self.tags = soup.find('div', {'id': 'problem-tags'}).get_text().lstrip().rstrip().split('\n')
        if self.tags[0] == 'no tags':
            self.tags = None

