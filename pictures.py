import  requests
from bs4 import BeautifulSoup


def download_picture(url):
    res = requests.get(url)
    img = res.content
    filename = 'img/' + url.split('/')[-1]
    with open(filename,'wb') as f:
        f.write(img)




def get_html():
    url = 'https://pic.netbian.com/4kmeinv/index.html'
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
    }
    res =requests.get(url,headers=headers)
    res.encoding = 'utf-8'
    if res.status_code == 200:
        html = res.text
        soup = BeautifulSoup(html,'lxml')
        all_list = soup.find(class_ = 'slist')
        all_img = all_list.find_all('li')
        for img in all_img:
            src = img['src']
            download_picture(src)
            print(src)
if __name__ == '__main__':
    get_html()