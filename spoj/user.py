import requests
import bs4

from os import environ

try:
    from . import exception
except:
    import exception

class User(object):
    def __init__(self, uname):
        '''
            Constructor for the User class taking the username
        '''
        self.userName = uname
        self.isLoggedIn = False

        try:
            self.proxyDict = {
                    'http_proxy'  : environ['http_proxy'],
                    'https_proxy' : environ['https_proxy'],
                    'ftp_proxy'   : environ['ftp_proxy'],
                    }
        except KeyError:
            self.proxyDict = None

        userURL = 'http://www.spoj.com/users/' + uname
        resp = requests.get(userURL, proxies = self.proxyDict)

        soup = bs4.BeautifulSoup(resp.text, 'lxml')
        self._fetchData(soup)

    def _authenticator(func):
        def wrapper(self, *args, **kargs):
            if not self.isLoggedIn:
                raise exception.NotLoggedIn('Function only available when logged in')
            return func(self, *args, **kargs)
        return wrapper

    def _fetchData(self, soup):
        if self.userName not in str(soup):
            raise exception.UserNotAvailable('{} is not a valid user'.format(self.userName))

        self.name     = soup.find('div', {'id': 'user-profile-left'}).find('h3').get_text()

        pVec = soup.find('div', {'id': 'user-profile-left'}).findAll('p')
        self.location = pVec[0].get_text().lstrip()
        self.joinDate = pVec[1].get_text().lstrip(' Joined')
        self.worldRank = int(pVec[2].get_text().lstrip(' World Rank: #').split()[0])
        self.points = float(pVec[2].get_text().lstrip(' World Rank: #').split()[1][1:])
        self.school = pVec[3].get_text().lstrip(' Institution: ')
        self.aboutMe = pVec[4].get_text().lstrip()

        tg = soup.find('dl', {'class': 'dl-horizontal profile-info-data profile-info-data-stats'}).findAll('dd')
        self.attemptCount = int(tg[1].get_text())
        self.solveCount = int(tg[0].get_text())

        self.solvedProblems = []
        tg = soup.findAll('table')[0]
        for tr in tg.findAll('tr'):
            for element in tr.findAll('td'):
                if(len(str(element.get_text()))!=0):
                    self.solvedProblems.append(element.get_text())

        self.todoProblems = []
        tg = soup.findAll('table')[1]
        for tr in tg.findAll('tr'):
            for element in tr.findAll('td'):
                self.todoProblems.append(element.get_text())
                if self.todoProblems[-1] == '':
                    self.todoProblems.pop()

    def _generageProfileDict(self, soup):
        userDict = {}
        userDict['login']         = soup.find('input', {'name': 'login'})['value']
        userDict['email']         = soup.find('input', {'name': 'email'})['value']
        userDict['name']          = soup.find('input', {'name': 'name'})['value']
        userDict['firstname']     = soup.find('input', {'name': 'firstname'})['value']
        userDict['lastname']      = soup.find('input', {'name': 'lastname'})['value']
        userDict['gravatar_same'] = 'on'
        userDict['phone']         = soup.find('input', {'name': 'phone'})['value']
        userDict['skype']         = soup.find('input', {'name': 'skype'})['value']
        userDict['birthyear']     = soup.find('input', {'name': 'birthyear'})['value']
        userDict['aboutme']       = soup.find('textarea', {'name': 'aboutme'}).get_text()
        userDict['website']       = soup.find('input', {'name': 'website'})['value']
        userDict['facebook']      = soup.find('input', {'name': 'facebook'})['value']
        userDict['google']        = soup.find('input', {'name': 'google'})['value']
        userDict['twitter']       = soup.find('input', {'name': 'twitter'})['value']
        userDict['github']        = soup.find('input', {'name': 'github'})['value']
        userDict['bitbucket']     = soup.find('input', {'name': 'bitbucket'})['value']
        userDict['stackoverflow'] = soup.find('input', {'name': 'stackoverflow'})['value']
        userDict['linkedin']      = soup.find('input', {'name': 'linkedin'})['value']

        tg = soup.find('select', {'name': 'country'})
        for country in tg:
            if 'selected' in str(country):
                userDict['country'] = country['value']
                break
        userDict['city']          = soup.find('input', {'name': 'city'})['value']
        userDict['school']        = soup.find('input', {'name': 'school'})['value']
        userDict['conf']          = soup.find('input', {'name': 'conf'})['value']
        userDict['notify']        = soup.find('input', {'name': 'notify'})['value']
        userDict['notify_com']    = soup.find('input', {'name': 'notify_com'})['value']
        userDict['rem_from_rank'] = soup.find('input', {'name': 'rem_from_rank'})['value']
        userDict['dis_source_win']= soup.find('input', {'name': 'dis_source_win'})['value']
        userDict['dis_probl_body']= soup.find('input', {'name': 'dis_probl_body'})['value']
        userDict['opt_dis_probl_tags'] = soup.find('input', {'name': 'opt_dis_probl_tags'})['value']

        return userDict

    def login(self, passW):
        '''
            Used to login to the Spoj,
            its necessary for submitting the problem
        '''
        self.__session = requests.Session()

        loginDat = {'login_user': self.userName, 'password': passW}
        resp = self.__session.post('http://www.spoj.com/login', data=loginDat)
        if 'Authentication failed!' in resp.text:
            self.__session.close()
            raise exception.LoginFalied('The password provided is not correct')
        self.isLoggedIn = True

    @_authenticator
    def editNick(self, nick):
        resp = self.__session.get('http://www.spoj.com/manageaccount')
        soup = bs4.BeautifulSoup(resp.text, 'lxml')
        userDict = self._generageProfileDict(soup)
        userDict['name'] = nick
        resp = self.__session.post('http://www.spoj.com/editaccount/', data=userDict)

    @_authenticator
    def editFirstName(self, name):
        resp = self.__session.get('http://www.spoj.com/manageaccount')
        soup = bs4.BeautifulSoup(resp.text, 'lxml')
        userDict = self._generageProfileDict(soup)
        userDict['firstname'] = name
        resp = self.__session.post('http://www.spoj.com/editaccount/', data=userDict)

    @_authenticator
    def editLastName(self, name):
        resp = self.__session.get('http://www.spoj.com/manageaccount')
        soup = bs4.BeautifulSoup(resp.text, 'lxml')
        userDict = self._generageProfileDict(soup)
        userDict['lastname'] = name
        resp = self.__session.post('http://www.spoj.com/editaccount/', data=userDict)

    @_authenticator
    def editPhoneNumber(self, number):
        number = str(number)
        resp = self.__session.get('http://www.spoj.com/manageaccount')
        soup = bs4.BeautifulSoup(resp.text, 'lxml')
        userdict = self._generageprofiledict(soup)
        userdict['phone'] = number
        resp = self.__session.post('http://www.spoj.com/editaccount/', data=userdict)

    @_authenticator
    def editSkype(self, ID):
        resp = self.__session.get('http://www.spoj.com/manageaccount')
        soup = bs4.BeautifulSoup(resp.text, 'lxml')
        userDict = self._generageProfileDict(soup)
        userDict['skype'] = ID
        resp = self.__session.post('http://www.spoj.com/editaccount/', data=userDict)

    @_authenticator
    def editYearOfBirth(self, year):
        year = str(year)
        resp = self.__session.get('http://www.spoj.com/manageaccount')
        soup = bs4.BeautifulSoup(resp.text, 'lxml')
        userdict = self._generageProfileDict(soup)
        userdict['birthyear'] = year
        resp = self.__session.post('http://www.spoj.com/editaccount/', data=userdict)

    @_authenticator
    def editCountry(self, country):
        pass

    @_authenticator
    def editCity(self, city):
        resp = self.__session.get('http://www.spoj.com/manageaccount')
        soup = bs4.BeautifulSoup(resp.text, 'lxml')
        userdict = self._generageProfileDict(soup)
        userdict['city'] = city
        resp = self.__session.post('http://www.spoj.com/editaccount/', data=userdict)

    @_authenticator
    def editSchool(self, school):
        resp = self.__session.get('http://www.spoj.com/manageaccount')
        soup = bs4.BeautifulSoup(resp.text, 'lxml')
        userdict = self._generageProfileDict(soup)
        userdict['school'] = school
        resp = self.__session.post('http://www.spoj.com/editaccount/', data=userdict)

    @_authenticator
    def editAboutMe(self, text):
        resp = self.__session.get('http://www.spoj.com/manageaccount')
        soup = bs4.BeautifulSoup(resp.text, 'lxml')
        userDict = self._generageProfileDict(soup)
        userDict['aboutme'] = text
        resp = self.__session.post('http://www.spoj.com/editaccount/', data=userDict)

    @_authenticator
    def editWebsite(self, website):
        resp = self.__session.get('http://www.spoj.com/manageaccount')
        soup = bs4.BeautifulSoup(resp.text, 'lxml')
        userDict = self._generageProfileDict(soup)
        userDict['website'] = website
        resp = self.__session.post('http://www.spoj.com/editaccount/', data=userDict)

    @_authenticator
    def editFacebookID(self, ID):
        resp = self.__session.get('http://www.spoj.com/manageaccount')
        soup = bs4.BeautifulSoup(resp.text, 'lxml')
        userDict = self._generageProfileDict(soup)
        userDict['facebook'] = ID
        resp = self.__session.post('http://www.spoj.com/editaccount/', data=userDict)

    @_authenticator
    def editGoogleID(self, ID):
        resp = self.__session.get('http://www.spoj.com/manageaccount')
        soup = bs4.BeautifulSoup(resp.text, 'lxml')
        userDict = self._generageProfileDict(soup)
        userDict['google'] = ID
        resp = self.__session.post('http://www.spoj.com/editaccount/', data=userDict)

    @_authenticator
    def editTwitterID(self, ID):
        resp = self.__session.get('http://www.spoj.com/manageaccount')
        soup = bs4.BeautifulSoup(resp.text, 'lxml')
        userDict = self._generageProfileDict(soup)
        userDict['twitter'] = ID
        resp = self.__session.post('http://www.spoj.com/editaccount/', data=userDict)

    @_authenticator
    def editGithubID(self, ID):
        resp = self.__session.get('http://www.spoj.com/manageaccount')
        soup = bs4.BeautifulSoup(resp.text, 'lxml')
        userDict = self._generageProfileDict(soup)
        userDict['github'] = ID
        resp = self.__session.post('http://www.spoj.com/editaccount/', data=userDict)

    @_authenticator
    def editBitbucketID(self, ID):
        resp = self.__session.get('http://www.spoj.com/manageaccount')
        soup = bs4.BeautifulSoup(resp.text, 'lxml')
        userDict = self._generageProfileDict(soup)
        userDict['bitbucket'] = ID
        resp = self.__session.post('http://www.spoj.com/editaccount/', data=userDict)

    @_authenticator
    def editStackOverflowID(self, ID):
        resp = self.__session.get('http://www.spoj.com/manageaccount')
        soup = bs4.BeautifulSoup(resp.text, 'lxml')
        userDict = self._generageProfileDict(soup)
        userDict['stackoverflow'] = ID
        resp = self.__session.post('http://www.spoj.com/editaccount/', data=userDict)

    @_authenticator
    def editLinkedInID(self, ID):
        resp = self.__session.get('http://www.spoj.com/manageaccount')
        soup = bs4.BeautifulSoup(resp.text, 'lxml')
        userDict = self._generageProfileDict(soup)
        userDict['linkedin'] = ID
        resp = self.__session.post('http://www.spoj.com/editaccount/', data=userDict)

    def close(self):
        self.__session.close()
        self.isLoggedIn = False

