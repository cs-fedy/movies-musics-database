from typing import Dict, List
from request import request
from bs4 import BeautifulSoup, Tag

def make_url(suffix: str) -> str:
  base_url = 'https://www.tunefind.com'
  return f'{base_url}{suffix}'

request_page = request()

class SongsScraper:
  def __get_title_link(self, tunefind_search_link: str, is_movie: bool) -> str:
    tunefind_search_page_content = request_page(tunefind_search_link)
    soup = BeautifulSoup(tunefind_search_page_content, 'html.parser')

    title_row_element = soup.select_one('.tf-site-search .row')
    title_cols_elements = title_row_element.select('.col-md-8')
    if is_movie:
      title_element = title_cols_elements[-1]
    else:
      title_element = title_cols_elements[0]

    return make_url(title_element.select_one('a').attrs['href'])

  def __get_season_episodes(self, season_link: str) -> List:
    season_page_content = request_page(season_link)
    soup = BeautifulSoup(season_page_content, 'html.parser')

    seasons_episodes_elements = soup.select('ul li h3 a')
    return [make_url(link_element.attrs['href']) for link_element in seasons_episodes_elements]

  def __get_tv_show_episodes_links(self, title_link: str) -> List:
    title_page_content = request_page(title_link)
    soup = BeautifulSoup(title_page_content, 'html.parser')

    seasons_elements = soup.select('ul li h3 a')
    seasons_links = [make_url(link_element.attrs['href']) for link_element in seasons_elements]

    links = []
    for season_link in seasons_links:
      episodes = self.__get_season_episodes(season_link)
      links.extend(episodes)
    return links

  def __get_episode_songs(self, episode_link: str) -> List:
    episode_page_content = request_page(episode_link)
    soup = BeautifulSoup(episode_page_content, 'html.parser')

    show_title_element = soup.select_one('h1')
    show_title = ' '.join(show_title_element.text.split(' ')[:-1])

    episode_title_element = soup.select_one('h2')
    episode_title = { 'title': f'{show_title} - {episode_title_element.text}' }

    songs_elements = soup.select('.SongRow_container__TbgMq')
    return [
      { **episode_title, **self.__get_song_details(song_element) }
      for song_element in songs_elements
    ]

  def __get_song_details(self, song_element: Tag) -> Dict:
    song_title_element = song_element.select_one('.SongTitle_link__qlRUV')
    description_element = song_element.select_one('.SceneDescription_description__SDFKK')
    artist_element = song_element.select_one('.ArtistSubtitle_subtitle__LaFIf')
    return {
      'song_title': song_title_element.text,
      'artist': artist_element.text,
      'description': description_element.text,
    }

  def get_title_musics(self, title_name: str, is_movie: bool) -> List:
    tunefind_search_url = make_url(f'/search/site?q={title_name}')
    title_link = self.__get_title_link(tunefind_search_url, is_movie)

    links = [title_link]
    if not is_movie:
      links = self.__get_tv_show_episodes_links(title_link)
    
    return [self.__get_episode_songs(episode) for episode in links]