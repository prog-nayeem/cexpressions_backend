
from django.contrib import admin
from django.urls import path, include

admin.site.site_title = "Cexpressions site admin"
admin.site.site_header = "Cexpressions administration"
admin.site.index_title = "Site administration"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include("accounts.urls")),
    path('api/v1/', include('api.urls')),
    path('tinymce/', include('tinymce.urls')),
]
