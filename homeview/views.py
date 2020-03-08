from django.shortcuts import render, reverse
from django.http import Http404, HttpResponseRedirect, HttpResponse
from publishers.models import Section, Publisher, Article, Sections
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings


def homeView(request):
    section = Section.objects.filter(article__publish=True)
    filteredSection = []
    for item in section:
        if item not in filteredSection:
            filteredSection.append(item)
    #article= Article.objects.order_by("-mod_date")
    mostViewed = Article.objects.filter(
        publish=True).order_by("-view_count")[:10]
    return render(request, "homeview/homeview.html", {"sections": filteredSection, "mostviewed": mostViewed})


def contactUs(request):
    section = Section.objects.filter(article__publish=True)
    filteredSection = []
    for item in section:
        if item not in filteredSection:
            filteredSection.append(item)
    #article= Article.objects.order_by("-mod_date")
    mostViewed = Article.objects.filter(
        publish=True).order_by("-view_count")[:10]
    return render(request, "homeview/contactUs.html", {"sections": filteredSection, "mostviewed": mostViewed})


def articleView(request, article_id, article_slug):
    article = Article.objects.get(id=article_id)
    article_sections = Sections.objects.filter(article=article)
    section = Section.objects.get(article=article)
    nullvalue = "<p>null</p>" or "null"
    history= "HISTORY"
    article.view_count += 1
    article.save(skip_md=False)
    mostViewed = Article.objects.filter(section=section).filter(
        publish=True).order_by("-view_count")[:10]
    # articles=Article.objects.filter(section=section)
    if article.title_slug != article_slug:
        return render(request, "homeview/pagenotfound.html", {
            "sections": article_sections, "section": section, "mostviewed": mostViewed})
    return render(request, "homeview/articleview.html", {"article": article,
                                                         "sections": article_sections, "section": section, "mostviewed": mostViewed, "nullvalue": nullvalue,"HISTORY":history})


def sectionView(request, section):
    section = Section.objects.get(Name=section)
    mostViewed = Article.objects.filter(section=section).filter(
        publish=True).order_by("-view_count")[:10]
    return render(request, "homeview/sectionView.html", {"section": section, "mostviewed": mostViewed})


def publisherPage(request, publisher_id):
    publisher = Publisher.objects.get(id=publisher_id)
    article = Article.objects.filter(publisher=publisher)
    return render(request, "homeview/publisherPage.html", {"publisher": publisher, "article": article})


def sendEmail(request):
    if request.method == "POST":
        full_name = request.POST["full_name"]
        email = request.POST["email"]
        #email= settings.EMAIL_HOST_USER
        phone_number = request.POST["phone_number"]
        subject = request.POST["subject"]
        message = request.POST["message"]
        Message = f"Hello, my name is {full_name}, my phone number and email address are {phone_number}, {email} respectively. \r\n\n {message}"
        # send_mail(subject,Message,email,['pascalemy2010@gmail.com'],fail_silently=False,)
        send = send_mail(subject, Message, "Illumepedia", [
                         'pascalemy2010@gmail.com'], fail_silently=False,)
        if send:
            messages.add_message(request, messages.INFO,
                                 "You message was sent successfully.")
            return HttpResponseRedirect(reverse("homeview:contactUsView"))
        else:
            messages.add_message(
                request, messages.INFO, "Sorry, something went wrong. You message was not sent.")
            return HttpResponseRedirect(reverse("homeview:contactUsView"))
            #"Sorry, something went wrong. You message was not sent."

        # return HttpResponse("emailsent successfully")
