from project_solo_app.models import Li_Job, Word, Background_Task
from django.db.models.functions import Lower
import re

def word_collection(limit=0):

    current_collect = Background_Task.objects.filter(activity='word_collect', status=1)
    if len(current_collect) !=0:
        return f"Can't scrape now. Existing scrape may be occurring."

    current_collect_object = Background_Task.objects.create(
        activity = 'word_collect',
        status = 1,
        current = 0,
        total = 0
    )

    li_job_count = 0
    unique_words = []
    unique_words_lower = []
    total_words = 0
    li_jobs = Li_Job.objects.all()

    current_collect_object.total = len(li_jobs)
    current_collect_object.save()

    for li_job in li_jobs:

        li_job_count += 1

        current_collect_object.current = 1
        current_collect_object.save()

        words = li_job.details.split()
        for word in words:
            total_words += 1

            #sanitize from the right side, any non-alphanumerics, permitting only +
            sanitize_attempt = 0
            while not word.isnumeric() and word != '' and word[-1] != (re.sub('[^A-Za-z0-9+]', '', word[-1])):
                if len(word)-1 > 0:
                    word = word[:len(word)-1]
                else:
                    word = ''
                sanitize_attempt += 1
                if sanitize_attempt > 10:
                    break

            #sanitize from the left side, any non-alphanumerics, permitting only +
            sanitize_attempt = 0
            while not word.isnumeric() and word != '' and word[0] != (re.sub('[^A-Za-z0-9]', '', word[0])):
                if len(word)-1 > 0:
                    word = word[len(word)-1:]
                else:
                    word = ''
                sanitize_attempt += 1
                if sanitize_attempt > 10:
                    break

            #eliminate words shorter than 5 characters where all are not capitalized alpha, but permitting + and #.
            if len(word) < 5 and word != (re.sub('[^A-Z+#]', '', word)):
                word = ""


            #eliminate words with 'http' present.
            if word.find('http') != -1:
                word = ""

            #convert _ to white space
            if word.find('_') != -1:
                word = word.replace('_', ' ')

            #convert $ to white space
            if word.find('$') != -1:
                word = word.replace('$', ' ')

            #convert & to white space
            if word.find('&') != -1:
                word = word.replace('&', ' ')

            #convert % to white space
            if word.find('%') != -1:
                word = word.replace('%', ' ')

            #convert @ to white space
            if word.find('@') != -1:
                word = word.replace('@', ' ')

            #convert * to white space
            if word.find('*') != -1:
                word = word.replace('*', ' ')

            #convert ? to white space
            if word.find('?') != -1:
                word = word.replace('?', ' ')

            #convert ! to white space
            if word.find('!') != -1:
                word = word.replace('!', ' ')

            #convert [ to white space
            if word.find('[') != -1:
                word = word.replace('[', ' ')

            #convert ] to white space
            if word.find(']') != -1:
                word = word.replace(']', ' ')

            #convert ( to white space
            if word.find('(') != -1:
                word = word.replace('(', ' ')

            #convert ) to white space
            if word.find(')') != -1:
                word = word.replace(')', ' ')

            #convert : to white space
            if word.find(':') != -1:
                word = word.replace(':', ' ')

            #convert ' to white space
            if word.find("'") != -1:
                word = word.replace("'", ' ')

            #convert ’ to white space
            if word.find('’') != -1:
                word = word.replace('’', ' ')

            #convert ´ to white space
            if word.find('´') != -1:
                word = word.replace('´', ' ')
                
            #convert \ to white space
            if word.find('\\') != -1:
                word = word.replace('\\', ' ')

            #convert - to white space
            if word.find('.') != -1:
                word = word.replace('.', ' ')

            #convert - to white space
            if word.find('-') != -1:
                word = word.replace('-', ' ')

            #convert — to white space (different?)
            if word.find('—') != -1:
                word = word.replace('—', ' ')

            #convert ; to white space
            if word.find(';') != -1:
                word = word.replace(';', ' ')

            #convert / to white space
            if word.find('/') != -1:
                word = word.replace('/', ' ')

            #convert , to white space
            if word.find(',') != -1:
                word = word.replace(',', ' ')

            #when white space is present in word, append new words from existing word to words
            if word.find(' ') != -1:
                new_words = word.split()
                for new_word in new_words:
                    words.append(new_word)
                word = ""

            if not word.isnumeric() and word != '' and word.lower() not in unique_words_lower:

                unique_words.append(word)
                unique_words_lower.append(word.lower())

        if limit > 0 and li_job_count == limit:
            print(f'Task has reached limit of: {limit}')
            break


    print(f'total words found: {total_words}')
    print(f'total unique words found: {len(unique_words)}')
    print(f'total unique words (lower) found: {len(unique_words_lower)}')

    #insert all new unique words into the db.
    for unique_word in unique_words:
        word_object = Word.objects.filter(word__iexact=unique_word.lower())
        if len(word_object) == 0:
            word_object = Word.objects.create(
                word = unique_word,
                status = 1
            )
            #if the word has strange characters we'll move it to the ignore status.
            if unique_word != (re.sub('[^A-Za-z0-9+#]', '', unique_word)):
                word_object.status = 0
                word_object.save(0)

    print('End of processing.')
    current_collect_object.delete()

    return 'done'