Solo project proposal:

Job listing Relevant Word dictionary tool
The project will be a semi-automatic word definition gathering tool.
The goal for this project is to hopefully shorten the time it takes to gather up unknown information that might be relevant to the job.
The user may or may not know all the subject matter that they would need to know, and by using this tool as a way to organize and centrally
manage this information, it would act as a quick reference.

Job listings will be scraped into the database. these job listings would be viewable as well.
From there the job's description/requirements/skills information will be able to be processed for definition gathering.
dictionary API's and/or web scraping techniques may be employeed to gather information for the unknown words.
manual definition insertion would also be possible.
the user will be able to include/exclude/correct/modify words to be viewed for a definition.
the user will be able to select the "best definition or definitions" for that word, so that those definitions float to the top of the heap.

Nice to haves would be: linkage to the source information for the definitions gathered.


This project uses Django's built-in auth, so creating a superuser is necessary when performing the initial set up.

python manage.py createsuperuser

additionally, this project uses channels and a worker process.

it will be necessary to launch the worker process in a separate terminal window,
performing the same steps as one normally does to run the server:

python manage.py runworker background-tasks

for more info on channels and workers see:

https://channels.readthedocs.io/en/latest/topics/worker.html