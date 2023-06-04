import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб - канала"""

    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    @classmethod
    def get_service(cls):
        return cls.youtube

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала.
        Дальше все данные будут подтягиваться по API.
        """
        self.__channel_id = channel_id
        channel = Channel.get_service().channels().list(id=channel_id, part='snippet,statistics').execute()

        self.title = channel['items'][0]['snippet']['title']
        self.description = channel['items'][0]['snippet']['description']
        self.url = channel['items'][0]['snippet']['thumbnails']["default"]['url']
        self.subscriber_count = channel['items'][0]['statistics']['subscriberCount']
        self.video_count = channel['items'][0]['statistics']['videoCount']
        self.views_count = channel['items'][0]['statistics']['viewCount']

    def __str__(self):
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __gt__(self, other):
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other):
        return int(self.subscriber_count) >= int(other.subscriber_count)

    def __lt__(self, other):
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other):
        return int(self.subscriber_count) <= int(other.subscriber_count)

    def __eq__(self, other):
        return int(self.subscriber_count) == int(other.subscriber_count)

    @property
    def channel_id(self):
        return self.__channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = Channel.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        all_info = json.dumps(channel, indent=2, ensure_ascii=False)

        print(all_info)

    def to_json(self, new_file):
        final_dict = {}
        final_dict["id"] = self.channel_id
        final_dict["title"] = self.title
        final_dict["description"] = self.description
        final_dict["url"] = self.url
        final_dict["subscriber_count"] = self.subscriber_count
        final_dict["video_count"] = self.video_count
        final_dict["view_count"] = self.view_count

        with open(new_file, 'w', encoding="UTF-8") as file:
            json.dump(final_dict, file, indent=2, ensure_ascii=False)