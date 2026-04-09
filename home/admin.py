from django.contrib import admin

# Register your models here.
from .models import Experience,Idea,Article,ProjectStats,Project,Journey,Contact,Purchase
admin.site.register(Experience)
admin.site.register(Idea)
admin.site.register(Article)
admin.site.register(ProjectStats)
admin.site.register(Project)
admin.site.register(Journey)
admin.site.register(Contact)
admin.site.register(Purchase)