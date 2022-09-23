from typing import List
from database import Song, Title
from genre import GenreScraper
from songs import SongsScraper
from title import TitleScraper
from os import path

song_scraper = SongsScraper()

def make_url(suffix: str) -> str:
  base_url = 'https://www.imdb.com'
  return f'{base_url}{suffix}'

def scrape_movies_links():
  links_file_path = r'links.txt'
  if not path.exists(links_file_path):
    open(links_file_path, 'x').close()

  with open('links.txt', 'r') as file:
    links = file.readlines()

  if not links:
    genres_browser_link = make_url('/feature/genre/?ref_=nv_ch_gr')
    genre_scraper = GenreScraper(genres_browser_link)
    links = genre_scraper.scrape_titles_links()

    with open('links.txt', 'w') as file:
      file.write('\n'.join(links))
  return links

def scrape_save_titles(links: List[str]) -> None:
  for link in links:
    title = TitleScraper.scrape_title(link)
    title_data = {
      **title,
      'genres': ' - '.join(title['genres']) 
    }
    
    with Title() as title:
      title.save_new_title(title_data)

def scrape_save_musics() -> None:
  with Title() as title:
      names = title.get_titles_names()
  
  for name, type in names:
    songs = song_scraper.get_title_musics(name, is_movie=type == 'movie')
    with Song() as song:
      song.save_new_songs(name, songs)


if __name__ == '__main__':
  Title().connect()
  Song().connect()
  links = scrape_movies_links()
  scrape_save_titles(links)
  scrape_save_musics()