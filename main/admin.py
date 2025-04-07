from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Position)
admin.site.register(Candidate)
admin.site.register(Visited_Check)