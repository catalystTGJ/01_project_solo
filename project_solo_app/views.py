from django.db.models.query_utils import select_related_descend
from django.shortcuts import HttpResponse, render, redirect
from django.contrib import messages
from .forms import RegisterForm

#needed for use of built-in django auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

#needed for background task application placed code
from tasks.webscrape_li import linkedin_search
from tasks.webscrape_search import definition_search
from tasks.word_collect import word_collection

#needed for direct access to the DB tables
from .models import Job, Li_Job, Word, Definition
from django.db.models.functions import Lower

# added for background tasks integration
from random import randint
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from time import sleep

# Index
def index(request):
    return redirect('/signin')

# Read
def signin(request):
    context = {}
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('/words')
    return render(request, 'signin.html', context)

# Read
def signout(request):
    request.session.flush()
    return redirect('/signin')

# Read
@login_required(login_url='/signin')
def words(request, action='', word_id=0):
    per_page = 10
    if 'target_render' in request.session:
        target_render = request.session['target_render']
    else:
        target_render = "words_defined.html"

    if 'word_id' in request.session:
        if word_id==0:
            word_id = int(request.session['word_id'])

    if 'job_page' in request.session:
        job_page = request.session['job_page']
    else:
        job_page = 0
    if 'defined_page' in request.session:
        defined_page = request.session['defined_page']
    else:
        defined_page = 0
    if 'relevant_page' in request.session:
        relevant_page = request.session['relevant_page']
    else:
        relevant_page = 0
    if 'irrelevant_page' in request.session:
        irrelevant_page = request.session['irrelevant_page']
    else:
        irrelevant_page = 0
    
    job_count = len(Li_Job.objects.filter(status=1))
    defined_count = len(Word.objects.filter(status=1, definitions__isnull=False))
    relevant_count = len(Word.objects.filter(status=1))
    irrelevant_count = len(Word.objects.filter(status=0))

    if action == '':
        target_render = 'words_defined.html'
    elif action == 'inc-exc':
        target_render = 'words_include_exclude.html'
    elif action == 'def-harvest':
        target_render = 'words_harvest.html'
    elif action == 'definitions':
        target_render = 'words_definitions.html'
    elif action == 'job-harvest':
        target_render = 'job_harvest.html'

    if action == 'job_top':
        job_page = 0
    elif action == 'job_previous':
        if job_page >= per_page:
            job_page -= per_page
    elif action == 'job_next':
        if job_page < job_count - per_page:
            job_page += per_page
    elif action == 'job_bottom':
        job_page = int(job_count/per_page)*per_page

    if action == 'defined_top':
        defined_page = 0
    elif action == 'defined_previous':
        if defined_page >= per_page:
            defined_page -= per_page
    elif action == 'defined_next':
        if defined_page < defined_count - per_page:
            defined_page += per_page
    elif action == 'defined_bottom':
        defined_page = int(defined_count/per_page)*per_page

    if action == 'relevant_top':
        relevant_page = 0
    elif action == 'relevant_previous':
        if relevant_page >= per_page:
            relevant_page -= per_page
    elif action == 'relevant_next':
        if relevant_page < relevant_count - per_page:
            relevant_page += per_page
    elif action == 'relevant_bottom':
        relevant_page = int(relevant_count/per_page)*per_page

    if action == 'irrelevant_top':
        irrelevant_page = 0
    elif action == 'irrelevant_previous':
        if irrelevant_page >= per_page:
            irrelevant_page -= per_page
    elif action == 'irrelevant_next':
        if relevant_page < irrelevant_count - per_page:
            irrelevant_page += per_page
    elif action == 'irrelevant_bottom':
        irrelevant_page = int(irrelevant_count/per_page)*per_page

    if action == 'relevant':
        word_object = Word.objects.get(id=word_id)
        if word_object:
            word_object.status = 1
            word_object.save()
    elif action == 'irrelevant':
        word_object = Word.objects.get(id=word_id)
        if word_object:
            word_object.status = 0
            word_object.save()

    if job_page > int(job_count/per_page)*per_page:
        job_page = int(job_count/per_page)*per_page

    if defined_page > int(defined_count/per_page)*per_page:
        defined_page = int(defined_count/per_page)*per_page

    if relevant_page > int(relevant_count/per_page)*per_page:
        relevant_page = int(relevant_count/per_page)*per_page

    if irrelevant_page > int(irrelevant_count/per_page)*per_page:
        irrelevant_page = int(irrelevant_count/per_page)*per_page

    request.session['job_page'] = job_page
    request.session['defined_page'] = defined_page
    request.session['relevant_page'] = relevant_page
    request.session['irrelevant_page'] = irrelevant_page
    request.session['target_render'] = target_render
    request.session['word_id'] = word_id

    job_end = job_page+per_page+5
    def_end = defined_page+per_page+5
    rel_end = relevant_page+per_page+5
    irrel_end = irrelevant_page+per_page+5

    context = {
        'job_count' : job_count,
        'defined_count' : defined_count,
        'relevant_count' : relevant_count,
        'irrelevant_count' : irrelevant_count,
        'job_page' : job_page + 1,
        'job_page_end' : job_end,
        'defined_page' : defined_page + 1,
        'defined_page_end' : def_end,
        'relevant_page' : relevant_page + 1,
        'relevant_page_end' : rel_end,
        'irrelevant_page' : irrelevant_page + 1,
        'irrelevant_page_end' : irrel_end,
        'irrelevant_words' : Word.objects.filter(status=0).annotate(lword=Lower('word')).order_by('lword')[irrelevant_page:irrel_end]
    }

    if target_render == 'job_harvest.html':
        context['jobs'] = Li_Job.objects.filter(status=1).annotate(ltitle=Lower('title')).order_by('ltitle')[job_page:job_end]

    if target_render == 'words_defined.html':
        context['defined_words'] = Word.objects.filter(status=1, definitions__isnull=False).annotate(lword=Lower('word')).order_by('lword')[defined_page:def_end]
    else:
        context['relevant_words'] = Word.objects.filter(status=1).annotate(lword=Lower('word')).order_by('lword')[relevant_page:rel_end]

    word_object = Word.objects.filter(id=word_id)
    if len(word_object) > 0:
        context['word'] = word_object[0]

    return render(request, target_render, context)


#below added for background task integration testing
channel_layer = get_channel_layer()

#definition harvest will scrape definitions for a word or words
def definition_harvest(request):
    if request.method == 'POST':
        if 'word_limit' in request.POST:
            limit = int(request.POST['word_limit'])
        else:
            limit = 0

        if 'word_id' in request.POST:
            word_id = int(request.POST['word_id'])
        else:
            word_id = 0

        if word_id > 0:
            if len(Word.objects.filter(id=word_id)) == 1:
                async_to_sync(channel_layer.send)('background-tasks', {'type': 'scrape_definition', 'word_id' : word_id, 'limit': 0})
                sleep(7)
                return redirect(f'/words/definitions/{word_id}')
        elif limit > 0:
            async_to_sync(channel_layer.send)('background-tasks', {'type': 'scrape_definition', 'word_id' : 0, 'limit': limit})

    return redirect('/words/def-harvest')

#linked_in web scrape function for background task
def job_harvest(request):
    if request.method == 'POST':
        if 'job_limit' in request.POST:
            limit = int(request.POST['job_limit'])
        else:
            limit = 0

        if 'url' in request.POST:
            URL = request.POST['url']
        else:
            URL = ''
        
        async_to_sync(channel_layer.send)('background-tasks', {'type': 'scrape_linkedin', 'url': URL, 'limit': limit})
    return redirect('/words/job-harvest')

#word collect will gather up words from jobs
def word_collect(request):
    if request.method == 'POST':
        if 'job_limit' in request.POST:
            limit = int(request.POST['job_limit'])
        else:
            limit = 0
        async_to_sync(channel_layer.send)('background-tasks', {'type': 'word_collect', 'limit': limit})
    return redirect('/words/def-harvest')
        
#test wait function for background task
def test_wait(request, wait):
    async_to_sync(channel_layer.send)('background-tasks', {'type': 'test_wait', 'wait': wait})
    return HttpResponse(f'test_wait message sent with wait={wait}', content_type='text/plain')



# GRAVEYARD

    # Read
# @login_required(login_url='/signin')
# def job_harvest_page_old(request):
#     data = ""
#     if request.method == 'POST':
#         linkedin_search(URL=request.POST['url'])
#     form = RegisterForm()
#     context = {
#         "regForm" : form,
#         "jobs" : Li_Job.objects.all()
#     }
#     return render(request, "job-harvest-old.html", context)




# import asyncio
# def get_or_create_eventloop():
#     try:
#         return asyncio.get_event_loop()
#     except RuntimeError as ex:
#         if "There is no current event loop in thread" in str(ex):
#             loop = asyncio.new_event_loop()
#             asyncio.set_event_loop(loop)
#             return asyncio.get_event_loop()


# # Read
# @login_required(login_url='/signin')
# def job_harvest_page(request):
#     context = {
#         "jobs" : Li_Job.objects.all()[0:15]
#     }
#     return render(request, "job_harvest.html", context)

# Read
# @login_required(login_url='/signin')
# def word_collect(request):

#     get_or_create_eventloop()

#     if request.method == 'POST':
#         limit = request.POST['job_limit']
#     word_collection(limit)

#     return redirect('/job-harvest-page')