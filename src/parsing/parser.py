from typing import List
import requests
from bs4 import BeautifulSoup
from src.news.news import News

def parse(urls: List[str]) -> List[News]:
    result = []
    for url in urls:
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        div_block = soup.find('div', string=lambda s: s and 'Популярное' in s)
        links = []
        if div_block:
            links = [a.get('href') for a in div_block.parent.find_all('a', href=True)]
        for link in links:
            page_url = url + link
            print(page_url)
            page_response = requests.get(page_url)
            page_html = page_response.text
            page_soup = BeautifulSoup(page_html, 'html.parser')
            news = News()
            news.header = page_soup.find('h1').text.strip()
            news.text = ''
            p_blocks = page_soup.find_all('p', class_='Paragraph_paragraph__9WAFK')
            for p_block in p_blocks:
                news.text += p_block.find('span').text.strip()
            news.date, news.time = page_soup.find('div', class_='PublishedMark_date__LG42P').text.strip().split(', ')
            news.time = news.time.replace(',', '')
            print(news)
            result.append(news)
    return result

if __name__ == '__main__':
    parse(['https://tass.ru/'])
