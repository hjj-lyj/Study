import  requests
from bs4 import BeautifulSoup
url = 'https://pic.netbian.com/4kmeinv/index.html'
res = requests.get(url)
html = res.text
soup = BeautifulSoup(html,'lxml')
li = soup.find_all("li")#筛选标签
for i in li:
    img = i.a.img
    if img != None:
        img = i.a.img["src"] #获取src该属性
        img_path='https://pic.netbian.com/' + img
        img_content = requests.get(img_path).content
        with open("./img/"+img.split('/')[-1],'wb') as f:
            f.write(img_content)
            print(1)




