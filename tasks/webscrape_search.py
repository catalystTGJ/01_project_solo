from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from time import sleep
import random

from project_solo_app.models import Background_Task, Definition, Word

def definition_search(word_id=0, limit=0):

    if word_id == 0 and limit == 0:
        return f'Nothing to do. Job requires either a word id or a limit to proceed.'

    current_collect = Background_Task.objects.filter(activity='definition_search', status=1)
    if len(current_collect) !=0:
        return f"Can't scrape now. Existing definition scrape may be occurring."

    current_collect_object = Background_Task.objects.create(
        activity = 'definition_search',
        status = 1,
        current = 0,
        total = 0
    )

    if word_id > 0:
        current_collect_object.current = 1
        current_collect_object.total = 1
        current_collect_object.save()
    else:
        pass

    word_object = Word.objects.filter(id=word_id)
    if len(word_object) == 1:

        word = word_object[0].word
        URL = 'https://google.com/search?q=' + word

        options = Options()
        options.headless = True
        options.add_argument("--window-size=1920,1080")
        search_driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=options)
        search_driver.get(URL)
        search_driver.add_cookie({'name' : 'lang' , 'value' : 'v=2&lang=en-us'})
        sleep(2)
        action = ActionChains(search_driver)
        search_page = search_driver.page_source
        search_soup = BeautifulSoup(search_page, "html.parser")

        span_items = search_soup.find_all('span')
        for span_count in range(len(span_items)):
            span_text = span_items[span_count].text
            if span_text != word and span_text.find(word) > -1:

                definition_object = Definition.objects.filter(word=word_object[0], source='Google')
                if len(definition_object) == 0:
                    definition_object = Definition.objects.create(
                        definition = span_text,
                        source = 'Google',
                        source_url = URL,
                        word = word_object[0]
                    )

                print(f'item {span_count}: {span_text}')
                break

    print('End of processing.')
    current_collect_object.delete()
    search_driver.quit()
    return 'done'


    # current_collect_object.total = len(li_jobs)
    # current_collect_object.save()