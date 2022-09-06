from typing import List
from genre import GenreScraper
from title import TitleScraper
import csv

def make_url(suffix: str) -> str:
  base_url = 'https://www.imdb.com'
  return f'{base_url}{suffix}'

columns = ['title', 'title_link', 'cover_src', 'cover_description', 'genres', 'description']

with open('titles.csv', 'w') as file:
  writer = csv.writer(file)
  writer.writerow(columns)

def scrape_titles(links: List[str]) -> None:
  for link in links:
    title = TitleScraper.scrape_title(link)
    title_record = [title['title'], title['title_link'], title['title_cover']['cover_src'], title['title_cover']['cover_description'], '-'.join(title['genres']), title['description']]

    # TODO: for the title['songs'] save them in a separate file
    
    with open('titles.csv', 'a') as file:
      writer = csv.writer(file)
      writer.writerow(title_record)

def scrape_imdb() -> list:
  genres_browser_link = make_url('/feature/genre/?ref_=nv_ch_gr')
  genre_scraper = GenreScraper(genres_browser_link)
  
  with open('links.txt', 'r') as file:
    links = file.readlines()

  if not links:
    links = genre_scraper.scrape_titles_links()

  scrape_titles([link.strip() for link in links])


if __name__ == '__main__':
  scrape_imdb()