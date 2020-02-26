from django.contrib import admin
from .models import Section, Publisher, Article
from django.core.mail import send_mail
# Register your models here.


def verify_Publisher(modeladmin, request, querryset):

    for publisher in querryset:
        message = f"<div><h3> Hello {publisher} </h3><p> We are pleased to inform you that your account has been verified. </p><p>You can now <a href='https://illumepedia.herokuapp.com/login/'>LOGIN</a> to your account and start publishing</p></div>"
        send_mail("Account Verification", "", "Illumepedia", [
                  publisher.account.email], fail_silently=False, html_message=message)
    querryset.update(verified=True)


verify_Publisher.short_description = "Verify Publisher(s)"


def disqualify_Publisher(modeladmin, request, querryset):
    querryset.update(verified=False)


disqualify_Publisher.short_description = "disqualify Publisher(s)"


class PublisherView(admin.ModelAdmin):
    list_display = ("__str__", "verified", "section")
    actions = [verify_Publisher, disqualify_Publisher]


admin.site.register(Section)
admin.site.register(Publisher, PublisherView)
admin.site.register(Article)
