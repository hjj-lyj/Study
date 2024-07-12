import os
import requests
from bs4 import BeautifulSoup
import asyncio
import aiohttp


# 定义一个异步下载图片的函数
async def download_picture(session, url, save_dir='img/'):
    try:
        response = await session.get(url)
        response.raise_for_status()  # 确保请求成功
        img = await response.content.read()  # 读取响应内容

        # 清洗文件名，避免安全风险
        filename = os.path.basename(url)
        filename = filename.replace('/', '')
        filename = filename.replace('\\', '')

        # 创建保存目录，如果不存在
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        filepath = os.path.join(save_dir, filename)
        with open(filepath, 'wb') as f:
            f.write(img)
        print(url)
    except Exception as e:
        print(f"下载失败: {url}, 错误: {str(e)}")


# 定义一个异步获取HTML并提取图片链接的函数
async def get_html(url, save_dir='img/'):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 确保请求成功
        response.encoding = 'utf-8'
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        all_list = soup.find(class_='list')
        all_img = all_list.find_all('img')
        urls = [img['src'] for img in all_img]  # 提取图片链接
        return urls
    except Exception as e:
        print(f"获取HTML失败: {url}, 错误: {str(e)}")


# 主函数，使用asyncio下载图片
async def main():
    url = 'https://pic.netbian.com/4kmeinv/index.html'
    urls = await get_html(url)

    # 使用aiohttp创建一个session，用于复用连接
    async with aiohttp.ClientSession() as session:
        tasks = [download_picture(session, url) for url in urls]
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    # 使用事件循环运行异步代码
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
