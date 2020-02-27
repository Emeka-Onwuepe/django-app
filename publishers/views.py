from django.shortcuts import render, reverse
from django.http import Http404, HttpResponseRedirect, HttpResponse
from .models import Section, Publisher, Article, Sections
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .form import CreateUserForm, EditUserForm, EditPublisherForm, SectionForm, ArticleCreationForm, ArticleModelForm, PublishArticleForm
from django.forms import formset_factory, modelformset_factory, inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
import re
from django.core.mail import send_mail
# Create your views here.


def register(request):
    if request.method == "POST":
        section_pk = int(request.POST["section"])
        section = Section.objects.get(pk=section_pk)
        description = request.POST["description"]
        form = CreateUserForm(request.POST)
        if form.is_valid():
            # form.save()
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            send_mail("Hello Boss", f"There is a new publisher at Illumpedia. Email: {email}", "Illumepedia", [
                'pascalemy2010@gmail.com'], fail_silently=False,)
            user = form.save()
            if not user:
                sections = Section.objects.all()
                form = CreateUserForm()
                return render(request, "publisher/register.html", {"form": CreateUserForm(), "sections": sections})
            Publisher.objects.create(account=user, first_name=first_name,
                                     last_name=last_name, section=section, description=description)
            return HttpResponseRedirect(reverse("login:loginView"))
        else:
            form = CreateUserForm(request.POST)
            sections = Section.objects.all()
            return render(request, "publisher/register.html", {"form": form, "sections": sections})

    else:
        sections = Section.objects.all()
        form = CreateUserForm()
        return render(request, "publisher/register.html", {"form": CreateUserForm(), "sections": sections})


@login_required(login_url="login:loginView")
def editProfile(request):
    user = request.user
    publisher = Publisher.objects.get(account=user)
    Userform = EditUserForm(instance=user)
    PublisherForm = EditPublisherForm(instance=publisher)
    return render(request, "publisher/editprofile.html", {"userform": Userform, "publisherform": PublisherForm})


@login_required(login_url="login:loginView")
def editProfilePro(request):
    user = request.user
    publisher = Publisher.objects.get(account=user)
    Userform = EditUserForm(data=request.POST, instance=user)
    PublisherForm = EditPublisherForm(data=request.POST, instance=publisher)
    if Userform.is_valid() and PublisherForm.is_valid():
        Userform.save()
        PublisherForm.save()
        username = user.username
        messages.add_message(request, messages.INFO,
                             "Profile Updated Successfully")
        return HttpResponseRedirect(reverse("publisher:publisherView", kwargs={"username": username}))


@login_required(login_url="login:loginView")
def publisherView(request, username):
    user = User.objects.get(username=username)
    try:
        publisher = Publisher.objects.get(account=user)
    except Publisher.DoesNotExist:
        #request.session["notPublisher"]="You are not registered as a publisher"
        # return HttpResponse("You are not registered as a publisher")
        # HttpResponseRedirect(reverse("login:loginView"))
        logout(request)
        return HttpResponseRedirect(reverse("publisher:register"))
    form = ArticleCreationForm()
    if publisher.verified:
        return render(request, "publisher/publisherview.html", {"user": user, "form": form})
    else:
        return render(request, "publisher/nonpublisherview.html", {"user": user, "form": form})


@login_required(login_url="login:loginView")
def ArticleCreateView(request, username):
    user = User.objects.get(username=username)
    publisher = Publisher.objects.get(account=user)
    section = publisher.section
    if request.method == "POST":
        form = ArticleCreationForm(data=request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            title_slug = form.cleaned_data["title_slug"]
            description = form.cleaned_data["description"]
            keywords = form.cleaned_data["keywords"]
            article = Article.objects.create(section=section, title=title, title_slug=title_slug,
                                             description=description, keywords=keywords)
            article.publisher.add(publisher)
            return HttpResponseRedirect(reverse('publisher:articleCreationView',
                                                kwargs={"username": username, 'article_id': article.id}))
        else:
            return render(request, "publisher/publisherview.html", {"user": user, "form": form})
    return HttpResponseRedirect(reverse('publisher:articleCreateView', kwargs={"username": username}))


@login_required(login_url="login:loginView")
def ArticleCreationView(request, username, article_id):
    user = User.objects.get(username=username)
   # publisher=Publisher.objects.get(account=user)
    article = Article.objects.get(pk=article_id)
    formsets = inlineformset_factory(
        Article, Sections, form=SectionForm, extra=2)
    SectionForms = formsets(instance=article)
    form = ArticleModelForm(instance=article)
    if request.method == "POST":
        form = ArticleModelForm(
            data=request.POST, files=request.FILES, instance=article)
        SectionForms = formsets(
            data=request.POST, files=request.FILES, instance=article)
        if form.is_valid() and SectionForms.is_valid():
            form.save()
            SectionForms.save()
            return HttpResponseRedirect(reverse('publisher:articlePublisherView',
                                                kwargs={"article_id": article.id, "article_slug": article.title_slug}))
        else:
            return render(request, 'publisher/createarticle.html', {'form': form,
                                                                    'sectionsForm': SectionForms, 'article': article, 'user': user})
    return render(request, 'publisher/createarticle.html', {'form': form,
                                                            'sectionsForm': SectionForms, 'article': article, 'user': user})


@login_required(login_url="login:loginView")
def articlePublisherView(request, article_id, article_slug):
    article = Article.objects.get(pk=article_id)
    article_sections = Sections.objects.filter(article=article)
    form = PublishArticleForm(instance=article)
    return render(request, "publisher/articlePublisherView.html",
                  {"article": article, "sections": article_sections, "form": form})


@login_required(login_url="login:loginView")
def publishView(request, article_id, article_slug):
    user = request.user
    article = Article.objects.get(pk=article_id)
    if request.method == "POST":
        form = PublishArticleForm(request.POST, instance=article)
        if form.is_valid():
            removeaddedslug = article.title_slug
            article.title_slug = re.sub(
                r"(-transformedslugdjango)", "", removeaddedslug)
            article.save()
            form.save()
            messages.add_message(request, messages.INFO,
                                 "Article published Successfully")
            return render(request, "publisher/articlePublisherView.html",
                          {"article": article, "user": user})
        else:
            return render(request, "publisher/articlePublisherView.html",
                          {"article": article, "user": user, "message": "An Error occured"})


@login_required(login_url="login:loginView")
def controlView(request, username):
    user = User.objects.get(username=username)
    publisher = Publisher.objects.get(account=user)
    article = Article.objects.filter(publisher=publisher)
    return render(request, "publisher/controlview.html", {'publisher': publisher, 'article': article, "user": user})


@login_required(login_url="login:loginView")
def editView(request, username, article_id):
    article = Article.objects.get(pk=article_id)
    formsets = inlineformset_factory(
        Article, Sections, form=SectionForm, extra=1)
    SectionForms = formsets(instance=article)
    form = ArticleModelForm(instance=article)
    if request.method == "POST":
        return render(request, "publisher/editview.html", {'form': form, 'sectionsForm': SectionForms, 'article': article})
    return HttpResponseRedirect(reverse('publisher:controlView', kwargs={"username": username}))


@login_required(login_url="login:loginView")
def editPro(request, username, article_id):
    formsets = inlineformset_factory(
        Article, Sections, form=SectionForm, extra=0)
    if request.method == "POST":
        article = Article.objects.get(id=article_id)
        form = ArticleModelForm(
            data=request.POST, files=request.FILES, instance=article)
        SectionForms = formsets(
            data=request.POST, files=request.FILES, instance=article)
        if form.is_valid() and SectionForms.is_valid():
            form.save()
            SectionForms.save()
            article.publish = False
            article.save()
            return HttpResponseRedirect(reverse('publisher:articlePublisherView',
                                                kwargs={"article_id": article.id, "article_slug": article.title_slug}))
        else:
            return render(request, "publisher/editview.html", {'form': form, 'sectionsForm': SectionForms, 'article': article})

    return HttpResponseRedirect(reverse('publisher:controlView', kwargs={"username": username}))


@login_required(login_url="login:loginView")
def articleWithdrawView(request, article_id):
    article = Article.objects.get(pk=article_id)
    user = request.user
    if request.method == "POST":
        article.publish = False
        slug = article.title_slug
        transformedSlug = f"{slug}-transformedslugdjango"
        article.title_slug = transformedSlug
        article.save(),
        return HttpResponseRedirect(reverse('publisher:controlView', kwargs={"username": user.username}))


@login_required(login_url="login:loginView")
def articleDeleteView(request, article_id):
    article = Article.objects.get(pk=article_id)
    user = request.user
    if request.method == "POST":
        article.delete()
        return HttpResponseRedirect(reverse('publisher:controlView', kwargs={"username": user.username}))
