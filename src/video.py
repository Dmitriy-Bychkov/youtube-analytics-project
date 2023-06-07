from src.apimixin import APIMixin


class Video(APIMixin):

    def __init__(self, video_id: str) -> None:
        self.video_id = video_id

        video_response = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                          id=self.video_id
                                                          ).execute()

        try:
            self.video_title = video_response['items'][0]['snippet']['title']
            self.url = f'https://youtu.be/{self.video_id}'
            self.view_count = video_response['items'][0]['statistics']['viewCount']
            self.like_count = video_response['items'][0]['statistics']['likeCount']

        except IndexError:
            self.video_title = None
            self.url = None
            self.view_count = None
            self.like_count = None

    def __str__(self):
        return f'{self.video_title}'


class PLVideo(Video):

    def __init__(self, video_id: str, playlist_id: str) -> None:
        super().__init__(video_id)
        self.playlist_id = playlist_id
