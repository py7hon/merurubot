import urllib3
import requests
import facebook
from bs4 import BeautifulSoup
from PIL import Image
from pathlib import Path

def upload(message, access_token, img_path=None):
    graph = facebook.GraphAPI(access_token)
    if img_path:
        post = graph.put_photo(image=open(img_path, 'rb'),
                               message=message)
    else:
        post = graph.put_object(parent_object='me',
                                connection_name='feed',
                                message=message)
    return post['post_id']


def getAccessToken(filename='access token.txt'):
    return Path(filename).read_text().strip()

def getStatus(soup, element='span', html_class='gallery'):
    html_elements = soup.find(element, {'class': html_class})
    paragraphs = ''.join(map(str, html_elements.contents))
    paragraphs = paragraphs.replace('</p>', '<p>').split('<p>')
    status_text = paragraphs[1]
    return status_text


def getSource(soup, element='a', html_class='button source'):
    btn = soup.find(element, {'class': html_class})
    return btn['href']


def getSoup(url):
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    return BeautifulSoup(response.data, 'html.parser')


# Basic code to save an image from a given url.
def saveImage(img_url, path='temp.png'):
    img = Image.open(requests.get(img_url, stream=True).raw)
    img.save(path)
    return path


def main():
    soup = getSoup('https://nhentai.net')
    status_text = getStatus(soup) + '\n\n' + 'Source: ' + getSource(soup)

    img_url = [x['data-src'] for x in soup.findAll('img')][3]
    img_path = saveImage(img_url)

    upload(status_text, getAccessToken(), img_path)


if __name__ == '__main__':
    main()
