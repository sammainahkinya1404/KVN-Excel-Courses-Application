from django.contrib import admin
from kvnApp.models import Video_courses, Profile, Transaction,UserSubscription,UserProgress,SubscriptionModule

class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'level','topic')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'date_joined', 'is_email_verified')
    search_fields = ['email']
    ordering = ['email']
    readonly_fields = ('date_joined', 'last_login')

class TransactionAdmin(admin.ModelAdmin):  
    list_display = ('item', 'amount', 'phone_number', 'timestamp')

class UserSubcriptionAdmin(admin.ModelAdmin):   
    list_display = ('user','module','transaction')

class UserProgressionAdmin(admin.ModelAdmin):
    list_display = ('user','course','topic','progress','hours_watched')
class SubscriptionModuleAdmin(admin.ModelAdmin):
    list_display = ('name','price')

admin.site.register(UserProgress, UserProgressionAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Video_courses, VideoAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(UserSubscription, UserSubcriptionAdmin)
admin.site.register(SubscriptionModule, SubscriptionModuleAdmin)
