from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from time import sleep
import random

from project_solo_app.models import Background_Task, Job, Li_Job, Li_Company, Li_Poster, Web_Scrape_Error

def linkedin_search(URL, limit=0):

    if not URL.startswith('https://www.linkedin.com/jobs/search/'):
        return f"Can't scrape now. Incorrect URL: {URL}"

    current_scrape = Background_Task.objects.filter(activity='web_scrape', status=1)
    if len(current_scrape) !=0:
        return f"Can't scrape now. Existing scrape may be occurring."

    curr_scrape_object = Background_Task.objects.create(
        activity = 'web_scrape',
        status = 1,
        url = URL,
        current = 0,
        total = 0
    )

    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1080")
    search_driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=options)
    #search_driver = webdriver.Chrome('/usr/local/bin/chromedriver')
    search_driver.get(URL)
    search_driver.add_cookie({'name' : 'lang' , 'value' : 'v=2&lang=en-us'})
    sleep(3)
    action = ActionChains(search_driver)
    search_page = search_driver.page_source
    search_soup = BeautifulSoup(search_page, "html.parser")
    job_results = search_soup.body.main.section.next_sibling
    total_job_line = job_results.find('span', class_='results-context-header__job-count')
    total_job_count = 0
    if total_job_line:
        total_job_count = int(total_job_line.text.replace(',','').replace('+',''))

    job_list = job_results.find_all('li')

    curr_job_count = len(job_list)

    print(f'Total job count for this search is: {total_job_count}')
    print(f'Initial job count in DOM is: {curr_job_count}')

    curr_scrape_object.total = curr_job_count
    curr_scrape_object.save()

    # ---- previous job count to compare to, as one of the means to know when to break the loop.
    prev_job_count = 0
    # ---- a value to be used to break the loop, should the prev_job_ount and curr_job_count be the same.
    retry_count_max = 3
    # ---- a limiter used during development, as another one of the means to break the loop.
    
    if limit == 0:
        loop_limit = 50
    else:
        loop_limit = int(limit/20)

    # ---- initial loop value, since the first page load already has a certain amount of jobs.
    loop_count = 2
    retry_count = 0
    scroll_loop=0
    see_more_jobs_click = 0

    while loop_count <= (total_job_count/25) and loop_count <= loop_limit:

        if scroll_loop == 0 and (limit == 0 or (limit > 0 and curr_job_count < limit)):
            try:
                for scroll_loop in range(20):
                    search_driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                    print(f'scroll count: {scroll_loop}')
                    sleep(.5)
            except:
                pass

        sleep(random.randint(2, 5))

        try:
            see_more_jobs = search_driver.find_element_by_xpath('/html/body/main/div/section/button')
            if see_more_jobs:
                see_more_jobs.click()
                see_more_jobs_click += 1
                print(f'see more jobs clicked: {see_more_jobs_click}')
        except:
            pass

        search_page = search_driver.page_source
        search_soup = BeautifulSoup(search_page, "html.parser")
        job_results = search_soup.body.main.section.next_sibling

        job_list = job_results.find_all('li')
        curr_job_count = len(job_list)

        print(f'Current job count in DOM is: {curr_job_count}')
        if limit > 0 and curr_job_count > limit:
            print(f'job count is adjusted to limit: {limit}')
            curr_scrape_object.total = limit
            curr_scrape_object.save()
            break
        else:
            curr_scrape_object.total = curr_job_count
            curr_scrape_object.save()

        if prev_job_count == curr_job_count:
            print('No additional jobs loaded this time...')
            retry_count += 1
            if retry_count == retry_count_max:
                print('Giving up now.')
                break
            else:
                print(f'Trying again... ({retry_count} retries attempted.)')
        else:
            prev_job_count = curr_job_count
            retry_count = 0

        loop_count += 1
        if loop_count >= loop_limit:
            print(f'Breaking loop at reaching the loop limit value of {loop_limit}')
            break

    print('Loop is completed.')

    # ------ beginning of the job pulling section

    job_count = 1

    for job_loop in range(len(job_list)):

        curr_scrape_object.current = job_count
        curr_scrape_object.save()

        company_name = "<MISSING>"
        company_link = ""
        company_location = ""
        job_link = "<MISSING>"
        job_linkedin_data_id = "<MISSING>"
        job_linkedin_data_search_id = ""
        job_listdate = ""
        poster_title = "<MISSING>"
        poster_subtitle = ""
        poster_link = ""
        job_details = {}
        job_criteria = {}

        ajob = job_list[job_loop]

        #For each job listing, we'll try to get the link at a minimum
        try:
            job_link = ajob.find('a')['href']
        except:
            pass

        #for each job listing, we will try to collect all the information.
        try:
            job_link = ajob.find('a')['href']
            company_line = ajob.find('a', class_='result-card__subtitle-link job-result-card__subtitle-link')
            company_location_line = ajob.find('span', class_='job-result-card__location')
            job_listdate_line = ajob.find('time', class_='job-result-card__listdate--new')

            search_driver.find_element_by_xpath(f'/html/body/main/div/section[2]/ul/li[{job_loop+1}]/a').click()
            sleep(random.randint(2, 4))
        
            search_page = search_driver.page_source
            job_soup = BeautifulSoup(search_page, "html.parser")
            job_title_line = job_soup.find('h2', class_='topcard__title')
            poster_title_line = job_soup.find('h3', class_='base-main-card__title')
            poster_subtitle_line = job_soup.find('h4', class_='base-main-card__subtitle')
            poster_link_line = job_soup.find('a', class_='message-the-recruiter__cta')

            print(f'Job #{job_count}')
            print('--------------------')
            if ajob:
                job_linkedin_data_id = ajob['data-id']
                job_linkedin_data_search_id = ajob['data-search-id']
                print(f'linkedin data ID: {job_linkedin_data_id}')
                print(f'linkedin data search ID: {job_linkedin_data_search_id}')

            if poster_title_line:
                poster_title = poster_title_line.text
                print(f'Poster title: {poster_title}')

            if poster_subtitle_line:
                poster_subtitle = poster_subtitle_line.text
                print(f'Poster subtitle: {poster_subtitle}')

            if poster_link_line:
                poster_link = poster_link_line["href"]
                print(f'Poster link: {poster_link}')

            if job_title_line:
                job_title = job_title_line.text
                print(f'job title: {job_title}')

            if job_listdate_line:
                job_listdate = job_listdate_line['datetime']
                print(f'job list date: {job_listdate}')

            print(f'job link: {job_link}')
            if company_line:
                company_name = company_line.text
                company_link = company_line["href"]
                print(f'company name: {company_name}')
                print(f'company link: {company_link}')

            if company_location_line:
                company_location = company_location_line.text
                print(f'company location: {company_name}')

            try:
                show_more = search_driver.find_element_by_class_name('show-more-less-html__button')
                show_more.click()
                sleep(.5)
            except:
                pass

            print('attempting details...')
            sleep(3)
            job_details_soup = job_soup.find('div', class_='description__text description__text--rich')
            job_details_lines = job_details_soup.find_all(['div', 'li', 'p'])
            for tag_loop in range(len(job_details_lines)):
                if len(job_details_lines[tag_loop].text) > 2:
                    job_details[tag_loop] = (job_details_lines[tag_loop].text)

            print('attempting job criteria...')
            job_criteria_soup = job_soup.find('ul', class_='job-criteria__list')
            job_criteria_headers = job_criteria_soup.find_all('h3', class_='job-criteria__subheader')
            job_criteria_values = job_criteria_soup.find_all('span', class_='job-criteria__text job-criteria__text--criteria')

            for crit_loop in range(len(job_criteria_headers)):
                job_criteria[job_criteria_headers[crit_loop].text] = job_criteria_values[crit_loop].text

            print('--------------------')

            # Database insertions

            li_poster_object = Li_Poster.objects.filter(title=poster_title)
            if len(li_poster_object)==0:
                li_poster_object = Li_Poster.objects.create(
                    title = poster_title,
                    subtitle = poster_subtitle,
                    url = poster_link
                )
            else:
                li_poster_object = li_poster_object[0]

            li_company_object = Li_Company.objects.filter(name=company_name)
            if len(li_company_object)==0:
                li_company_object = Li_Company.objects.create(
                    name = company_name,
                    location = company_location,
                    url = company_link
                )
            else:
                li_company_object = li_company_object[0]

            job_object = Job.objects.filter(title=f'{job_title} - (Li)')
            if len(job_object)==0:
                job_object = Job.objects.create(
                    title = f'{job_title} - (Li)',
                    status = 1
                )
            else:
                job_object = job_object[0]

            job_details_text = ""
            for j_line in job_details:
                job_details_text = f'{job_details_text}{job_details[j_line]}\n'

            li_job_object = Li_Job.objects.filter(data_id=job_linkedin_data_id)
            if len(li_job_object)==0:
                li_job_object = Li_Job.objects.create(
                    title = job_title,
                    data_id = job_linkedin_data_id,
                    data_search_id = job_linkedin_data_search_id,
                    url = job_link,
                    details = job_details_text,
                    criteria = job_criteria,
                    post_date = job_listdate,
                    status = 1,
                    company = li_company_object,
                    poster = li_poster_object,
                    job = job_object
                )
            else:
                if li_job_object.details != job_details_text:
                    li_job_object = li_job_object[0]
                    li_job_object.details = job_details_text
                    li_job_object.save()

        except:
            error_object = Web_Scrape_Error.objects.filter(url=job_link)
            if len(error_object)==0:
                error_object = Web_Scrape_Error.objects.create(
                    url = job_link,
                    count = 1,
                    status = 1
                )
            else:
                error_object = error_object[0]
                error_object.count += 1
                error_object.save()
                
        if limit > 0 and job_count == limit:
            print(f'Job has reached limit of: {limit}')
            break
        
        job_count += 1

    print('End of processing.')
    curr_scrape_object.delete()
    search_driver.quit()
    return 'done'