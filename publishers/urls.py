from django.urls import path
from . import views

app_name = "publisher"

urlpatterns = [
    path('', views.register, name="register"),
    path('editProfile', views.editProfile, name="editProfile"),
    path('editProfilePro', views.editProfilePro, name="editProfilePro"),
    path('<str:username>', views.publisherView, name="publisherView"),
    path('<str:username>/articlecreate',
         views.ArticleCreateView, name="articleCreateView"),
    path('<str:username>/<int:article_id>/articlecreation',
         views.ArticleCreationView, name="articleCreationView"),
    path('<int:article_id>/<slug:article_slug>',
         views.articlePublisherView, name="articlePublisherView"),
    path('publish/<int:article_id>/<slug:article_slug>',
         views.publishView, name="publishView"),
    path('<str:username>/controlview', views.controlView, name="controlView"),
    path('delete/<int:article_id>',
         views.articleDeleteView, name="articleDeleteView"),
    path('withdraw/<int:article_id>', views.articleWithdrawView,
         name="articleWithdrawView"),
    path('<str:username>/<int:article_id>/editview',
         views.editView, name="editView"),
    path('<str:username>/<int:article_id>/editpro',
         views.editPro, name="editpro"),
]
