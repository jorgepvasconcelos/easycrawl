import os
from collections import deque


class CrawledQueue:
    def __init__(self, crawler_name: str):
        self.crawler_name = crawler_name

        self.__file_name = f"{self.crawler_name}_crawled_queue.txt"
        self.__queue_dir_name = f'crawlers_queue'
        self.__queue_dir_path = f'{os.getcwd()}/{self.__queue_dir_name}'
        self.__crawler_queue_file_path = f'{self.__queue_dir_path}/{self.__file_name}'

        self.__create_file_path()

    def __create_file_path(self):
        os.makedirs(self.__queue_dir_path, exist_ok=True)
        if not os.path.exists(self.__crawler_queue_file_path):
            with open(self.__crawler_queue_file_path, 'w'):
                ...

    def add_to_crawled_queue(self, url: str) -> None:
        self.__append_queue(url=url)

    def is_on_crawled_queue(self, url: str) -> bool:
        with open(self.__crawler_queue_file_path, 'r') as file:
            for line, line_value in enumerate(file):
                if url == line_value.strip():
                    return True
            else:
                return False

    def __append_queue(self, url):
        with open(self.__crawler_queue_file_path, 'a') as file:
            file.write(f"\n{url}")


class CrawlerQueue:
    """
    The queue is a FIFO
    """

    def __init__(self, crawler_name: str):
        self.__crawler_queue = deque()
        self.crawled_queue = CrawledQueue(crawler_name)

    def get_request_from_queue(self):
        if self.__crawler_queue:
            url = self.__crawler_queue.popleft()
        else:
            return None

        self.__add_to_crawled_queue(url=url)

        return url

    def add_request_to_queue(self, url) -> None:
        if url in self.__crawler_queue:
            print(f'URL: {url} is on the __crawler_queue')
            return

        if not self.__page_already_crawled(url=url):
            self.__crawler_queue.append(url)
        else:
            print(f'URL: {url} already_crawled')

    def __page_already_crawled(self, url: str) -> bool:
        return self.crawled_queue.is_on_crawled_queue(url=url)

    def __add_to_crawled_queue(self, url: str) -> None:
        self.crawled_queue.add_to_crawled_queue(url=url)
