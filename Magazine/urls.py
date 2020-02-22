from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', include("homeview.urls")),
    path('admin/', admin.site.urls),
    path('publisher/',include("publishers.urls")),
    path('login/',include("login.urls")),
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name="login/passwordreset.html"),name='password_reset',),
    path('password_reset_done/',auth_views.PasswordResetView.as_view(template_name="login/password_reset_done.html"),name="password_reset_done",),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="login/password_reset_confirm.html"), name='password_reset_confirm',),
    path( 'password_reset_completed/',auth_views.PasswordResetCompleteView.as_view(template_name="login/password_reset_complete.html"), name='password_reset_complete',),
]

urlpatterns+=staticfiles_urlpatterns()

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
