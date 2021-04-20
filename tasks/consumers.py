from channels.consumer import SyncConsumer
from time import sleep
from tasks.webscrape_li import linkedin_search
from tasks.webscrape_search import definition_search
from tasks.word_collect import word_collection

class BackgroundTaskConsumer(SyncConsumer):

    # This is here for testing purposes
    def test_wait(self, message):
        if 'wait' not in message.keys():
            raise ValueError('message must include wait key')

        if not isinstance(message['wait'], int):
            raise ValueError('wait value must be an integer')

        print(f"Task: test_wait has begun with wait value: {message['wait']}")
        sleep(message['wait'])
        print(f"Task: test_wait has ended")

    # This will be used to scrape Linkedin
    def scrape_linkedin(self, message):

        if 'url' not in message.keys():
            raise ValueError('message must include url key.')

        print(f"Task: Linkedin search scraping has begun with url value: {message['url']}")
        linkedin_search(URL=message['url'], limit=message['limit'])
        print(f"Task: Linkedin search scraping has ended.")

# This will be used to scrape google for a word definition
    def scrape_definition(self, message):

        if 'limit' not in message.keys():
            raise ValueError('message must include limit key.')

        print(f"Task: Definition search scraping has begun with limit: {message['limit']}")
        definition_search(word_id=message['word_id'], limit=message['limit'])
        print(f"Task: Definition search scraping has ended.")

    # This will be used to scrape Linkedin
    def word_collect(self, message):

        if 'limit' not in message.keys():
            raise ValueError('message must include limit key.')

        print(f"Task: Word collection has begun with limit: {message['limit']}")
        word_collection(limit=message['limit'])
        print(f"Task: Word collection has ended.")


