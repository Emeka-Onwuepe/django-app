from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
# from django.utils import timezone
import datetime
import re
from PIL import Image
from math import floor
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
# Create your models here.


class Section(models.Model):
    Name = models.CharField("Name", max_length=156)
    description = models.TextField(default="null", blank=False)

    def __str__(self):
        return self.Name

    class Meta:
        managed = True
        verbose_name = 'Section'
        verbose_name_plural = 'Sections'


class Publisher(models.Model):
    account = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="Account")
    first_name = models.CharField("First Name", max_length=156)
    last_name = models.CharField("Last Name", max_length=156)
    section = models.ForeignKey(
        Section, on_delete=models.CASCADE, related_name="Section")
    verified = models.BooleanField(default=False)
    description = models.TextField("description", max_length=150, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        managed = True
        verbose_name = 'Publisher'
        verbose_name_plural = 'Publishers'


class Article(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    title_slug = models.SlugField(default="null")
    description = models.TextField()
    keywords = models.CharField(max_length=255, default="null")
    image = models.ImageField(null=True)
    image_source = models.CharField(max_length=255, null=True, blank=True)
    image_description = models.CharField(
        max_length=255, default='image', blank=True)
    sub_heading = models.CharField(max_length=255, null=True, blank=True)
    body_text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    mod_date = models.DateTimeField(null=True)
    publisher = models.ManyToManyField(Publisher)
    view_count = models.IntegerField(default=0)
    publish = models.BooleanField(default=False)
    references = models.TextField(default="null", null=True, blank=True)

    def bodySnippet(self):
        body = self.body_text[:120]
        bodySnippet = re.sub(
            r"\s\w+$|(<strong>|</strong>|<em>|</em>|<b>|</b>|<i>|</i>|<u>|</u>|<a.+?>|</a>)", "", body)
        return f'{bodySnippet} ....'

    def __str__(self):
        return self.title

    class Meta:
        managed = True
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        ordering = ['-pub_date']

    # def delete(self, *args, **kwargs):
    #     self.image.delete()
    #     super().delete(*args, **kwargs)

    def save(self, skip_md=True, *args, **kwargs):
        if skip_md:
            self.mod_date = datetime.datetime.now()

        if self.image:
            im = Image.open(self.image)
            width, height = im.size
            output = BytesIO()
            n = 0.5
            Width = floor(width * n)
            Height = floor(height * n)
            if width > 1000:
                im = im.resize((Width, Height))
                im.save(output, format='JPEG', quality=100)
                output.seek(0)
                self.image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.image.name.split(
                    '.')[0], 'image/jpeg', sys.getsizeof(output), None)

        super().save(*args, **kwargs)  # Call the real save() method


class Sections(models.Model):
    """Model definition for Sections."""
    # TODO: Define fields here
    article = models.ForeignKey(
        Article, related_name='sections', on_delete=models.CASCADE)
    sub_heading = models.CharField(max_length=255, null=True)
    Sub_section_image = models.ImageField(null=True, blank=True)
    image_source = models.CharField(max_length=255, null=True, blank=True)
    image_description = models.CharField(
        max_length=255, default="image", blank=True)
    body_text = models.TextField(null=True)

    class Meta:
        """Meta definition for Sections."""
        verbose_name = 'Sections'
        verbose_name_plural = 'Sections'

    def __str__(self):
        """Unicode representation of Sections."""
        return self.sub_heading

    def save(self, *args, **kwargs):
        if self.Sub_section_image:
            im = Image.open(self.Sub_section_image)
            width, height = im.size
            output = BytesIO()
            n = 0.5
            Width = floor(width * n)
            Height = floor(height * n)
            if width > 1000:
                im = im.resize((Width, Height))
                im.save(output, format='JPEG', quality=100)
                output.seek(0)
                self.Sub_section_image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.Sub_section_image.name.split('.')[
                                                              0], 'image/jpeg', sys.getsizeof(output), None)

        super().save(*args, **kwargs)  # Call the real save() method

    # def delete(self, *args, **kwargs):
    #     self.Sub_section_image.delete()
    #     super().delete(*args, **kwargs)


@receiver(pre_save, sender=Article)
def delete_Artictle_image(sender, instance, *args, **kwargs):
    if instance.pk:
        article = Article.objects.get(pk=instance.pk)
        if article.image != instance.image:
            article.image.delete(False)


@receiver(pre_save, sender=Sections)
def delete_Sections_image(sender, instance, *args, **kwargs):
    if instance.pk:
        section = Sections.objects.get(pk=instance.pk)
        if section.Sub_section_image != instance.Sub_section_image:
            section.Sub_section_image.delete(False)


@receiver(post_delete, sender=Article)
def delete_artictle_image(sender, instance, using, *args, **kwargs):
    if instance.image:
        instance.image.delete(save=False)


@receiver(post_delete, sender=Sections)
def delete_sections_image(sender, instance, using, *args, **kwargs):
    if instance.Sub_section_image:
        instance.Sub_section_image.delete(save=False)
