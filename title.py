from typing import Dict
from bs4 import BeautifulSoup
from request import request
from songs import SongsScraper

request_page = request()
song_scraper = SongsScraper()
 

class TitleScraper:
  @staticmethod
  def scrape_title(title_url: str) -> Dict:
    title_page_content = request_page(title_url)
    soup = BeautifulSoup(title_page_content, 'html.parser')

    metadata_elements = soup.select_one('ul[data-testid="hero-title-block__metadata"] li')
    is_tv_show = metadata_elements.text.strip() == 'TV Series'

    title_element = soup.select_one('[data-testid="hero-title-block__title"]')
    title = title_element.text

    title_cover_element = soup.select_one('div[cel_widget_id="DynamicFeature_HeroPoster"] img')
    title_cover_details = {
      'cover_description': title_cover_element.attrs['alt'],
      'cover_src': title_cover_element.attrs['src']
    }

    genres_element = soup.select('div[data-testid="genres"] .ipc-chip-list__scroller a')
    title_description_element = soup.select_one('p[data-testid="plot"]')

    return {
      'title': title,
      'title_link': title_url,
      'title_cover': title_cover_details,
      'genres': [element.text for element in genres_element],
      'description': title_description_element.text,
      'is_movie': not is_tv_show,
      'is_tv_show': is_tv_show,
      'songs': song_scraper.get_title_musics(title, is_movie=not is_tv_show)
    }