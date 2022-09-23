from typing import List
from request import request
from bs4 import BeautifulSoup

def make_url(suffix: str) -> str:
  base_url = 'https://www.imdb.com'
  return f'{base_url}{suffix}'

request_page = request()

class GenreScraper:
  def __init__(self, genres_browser_link: str) -> None:
    self.genres_browser_link = genres_browser_link

  def scrape_titles_links(self) -> List[str]:
    genres_links, titles = self.__scrape_genres_links(), []
    for genre_link in genres_links:
      titles.extend(self.__scrape_genre(genre_link))
    return titles

  def __scrape_genres_links(self) -> List[str]:
    genre_browser_content = request_page(self.genres_browser_link)
    soup = BeautifulSoup(genre_browser_content, 'html.parser')
    genres_links_sections = soup.select('div.ab_links', limit=2)

    genres_section = genres_links_sections[0]
    genres_section.extend(genres_links_sections[1])

    return [
    make_url(link_element.attrs['href']) 
    for link_element in genres_section.select('a')
  ]

  def __get_sub_page_url(self, url: str, count: int) -> str:
    return f'{url}&start={count}&ref_=adv_nxt'

  def __get_links_from_page(self, url: str) -> list[str]:
    sub_page_content = request_page(url)
    soup = BeautifulSoup(sub_page_content, 'html.parser')
    movies_elements = soup.select('.lister-list .lister-item .lister-item-content h3 a')
    return [make_url(element.attrs['href']) for element in movies_elements]

  def __has_next_sub_page(self, page_url: str) -> bool:
    page_content = request_page(page_url)
    soup = BeautifulSoup(page_content, 'html.parser')
    description_element = soup.select_one('div.desc a')
    pagination_content: str = description_element.text
    return pagination_content.find('Next') > -1
    
  def __scrape_genre(self, genre_url: str) -> List[str]:
    genre_page_content = request_page(genre_url)
    soup = BeautifulSoup(genre_page_content, 'html.parser')

    page_description_element = soup.select_one('div.desc span')
    page_description_content = page_description_element.text    
    page_size = int(page_description_content[page_description_content.find('-')+1:page_description_content.find(' ')])

    current_count = page_size + 1
    current_page = self.__get_sub_page_url(genre_url, current_count)
    
    scraped_links = self.__get_links_from_page(genre_url)
    while self.__has_next_sub_page(current_page):
      current_page = self.__get_sub_page_url(genre_url, current_count)
      links = self.__get_links_from_page(current_page)
      scraped_links.extend(links)
      current_count += page_size
    return scraped_links