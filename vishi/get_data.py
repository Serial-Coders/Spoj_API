from bs4 import BeautifulSoup as bsoup
import requests
user_name=input("Enter the user_name : ")
url="http://www.spoj.com/users/"+user_name
r=requests.get(url)
soup=bsoup(r.text,'lxml')
dds=soup.find_all('dd')
print("Problems solved : "+dds[0].contents[0])
print("Total Submission : "+dds[1].contents[0])
