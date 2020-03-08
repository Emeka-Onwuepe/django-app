from django.urls import path
from . import views

app_name="homeview"

urlpatterns = [
    path('',views.homeView,name="homeview"),
    path('contact-us',views.contactUs,name="contactUsView"),
    path('sendEmail',views.sendEmail,name="sendEmailView"),
    path('<str:section>',views.sectionView,name="sectionView"),
    path('<int:article_id>/<slug:article_slug>',views.articleView,name="articleView"),
    path('publisher/<int:publisher_id>/publisherPage', views.publisherPage, name="publisherPage"),
] 