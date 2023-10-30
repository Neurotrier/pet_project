from django.contrib import admin
from todolist.models import *



class UserListAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created', 'user', 'is_finished')
    list_display_links = ('id', 'title')

class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'user_list')




admin.site.register(UserList, UserListAdmin)
admin.site.register(Task, TaskAdmin)
