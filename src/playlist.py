import isodate
import datetime

from src.apimixin import APIMixin


class PlayList(APIMixin):
    '''
    Класс инициализирующийся от _id_ плейлиста
    '''

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id

        self.title = self.get_playlist_info()['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'

    def __repr__(self):
        return f"{self.__class__.__name__}, " \
               f"{self.playlist_id}," \
               f"{self.title}, " \
               f"{self.url}"

    def get_playlist_info(self):
        """Загружаем информацию о плейлисте"""

        request_info = PlayList.get_service().playlists().list(part="snippet", id=self.playlist_id)
        response_info = request_info.execute()

        return response_info

    @property
    def get_video_info(self):
        """
        Получаем и возвращаем ответ со всеми видеороликами в плейлисте.
        """

        playlist_videos = PlayList.get_service().playlistItems().list(playlistId=self.playlist_id,
                                                                      part='contentDetails',
                                                                      maxResults=50).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        video_response = PlayList.get_service().videos().list(part='contentDetails,statistics',
                                                              id=','.join(video_ids)
                                                              ).execute()

        return video_response

    @property
    def total_duration(self):
        """
        Считаем и возвращаем суммарную длительность
        всех видеороликов в плейлисте
        """

        time_line = []

        # Обходим перебором список времен продолжительности видео
        for video in self.get_video_info['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            time_line.append(duration)
        # Суммируем и возвращаем длительность у видео в плейлисте
        result = sum(time_line, datetime.timedelta())
        return result

    def show_best_video(self):
        """
        Находим и возвращаем ссылку на самое популярное видео из плейлиста
        (по количеству лайков)
        """

        highest_likes = 0
        top_url_video = ''
        for i in self.get_video_info['items']:
            likes = i['statistics']['likeCount']
            if int(likes) > int(highest_likes):
                highest_likes = likes
                top_url_video = i['id']

        return f'https://youtu.be/{top_url_video}'
