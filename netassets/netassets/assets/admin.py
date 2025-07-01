from django.contrib import admin
from .models import NetworkDevice, Switch, Computer, Printer, Router, UserProfile, UserPermission, UserDashboardCard
from simple_history.admin import SimpleHistoryAdmin

admin.site.register(NetworkDevice, SimpleHistoryAdmin)
admin.site.register(Switch, SimpleHistoryAdmin)
admin.site.register(Computer, SimpleHistoryAdmin)
admin.site.register(Printer, SimpleHistoryAdmin)
admin.site.register(Router, SimpleHistoryAdmin)
admin.site.register(UserProfile)
admin.site.register(UserPermission)
admin.site.register(UserDashboardCard) 