from django.contrib import admin
from jedzonko.models import Recipe, Plan, RecipePlan, Page, Dayname

admin.site.register(Recipe)
admin.site.register(Plan)
admin.site.register(RecipePlan)
admin.site.register(Page)
admin.site.register(Dayname)
