from bs4 import BeautifulSoup
import requests
import html5lib

def DownloadPic(http_url):
    '''downoad the picture in the imgur.com/r/.../xxxxxx'''
    print("The page for the spyder: ", http_url, '\n')
    user_agent = {'User-agent': 'Mozilla/5.0'}
    response = requests.get(http_url, headers=user_agent)
    assert(response.status_code == 200)
    html_doc = response.text
    soup = 	BeautifulSoup(html_doc, "html5lib")
    imageName = soup.h1.string
    imageID = http_url.split('/')[-1]
    download_url = "http://imgur.com/download/" + imageID + '/'+ imageName
    print('Download URL:', download_url)
    file_name = imageName.replace("\"", "").replace("\'", "").replace("*", "").replace("/", "").replace("?", "").replace("|", "").replace("<", "").replace(">", "").replace(":", "") + '.gif'
    file_response = requests.get(download_url)
    file = open(file_name, 'wb')
    file.write(file_response.content)
    file.close()
    print(response.status_code)
    print("Done")

http_url = "https://imgur.com/r/puppies/TvnyjEc"
DownloadPic(http_url)