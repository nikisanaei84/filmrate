from django.contrib import admin
from prj.models import Movie,Review,Comment,Favorite,Profile

admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(Favorite)
admin.site.register(Profile)
# admin.site.register(Category)