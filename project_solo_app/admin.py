from django.contrib import admin
from .models import Word, Definition, Job , Li_Company, Li_Poster, Li_Job, Background_Task, Web_Scrape_Error

# Register your models here.

class WordAdmin(admin.ModelAdmin):
    pass
admin.site.register(Word, WordAdmin)

class DefinitionAdmin(admin.ModelAdmin):
    pass
admin.site.register(Definition, DefinitionAdmin)

class JobAdmin(admin.ModelAdmin):
    pass
admin.site.register(Job, JobAdmin)

class Li_CompanyAdmin(admin.ModelAdmin):
    pass
admin.site.register(Li_Company, Li_CompanyAdmin)

class Li_PosterAdmin(admin.ModelAdmin):
    pass
admin.site.register(Li_Poster, Li_PosterAdmin)

class Li_JobAdmin(admin.ModelAdmin):
    pass
admin.site.register(Li_Job, Li_JobAdmin)

class Background_TaskAdmin(admin.ModelAdmin):
    pass
admin.site.register(Background_Task, Background_TaskAdmin)

class Web_Scrape_ErrorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Web_Scrape_Error, Web_Scrape_ErrorAdmin)