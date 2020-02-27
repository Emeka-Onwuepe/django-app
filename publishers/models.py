from django.db import models
from django.contrib.auth.models import User 
from django.db.models.signals import pre_save
from django.dispatch import receiver
# from django.utils import timezone
import datetime
import re
# Create your models here.

class Section(models.Model):
    Name= models.CharField("Name", max_length=156)
    def __str__(self):
        return self.Name
    class Meta:
        managed = True
        verbose_name = 'Section'
        verbose_name_plural = 'Sections'

class Publisher(models.Model):
    account= models.OneToOneField(User, on_delete=models.CASCADE,related_name="Account")
    first_name= models.CharField("First Name", max_length=156)
    last_name= models.CharField("Last Name", max_length=156)
    section= models.ForeignKey(Section, on_delete=models.CASCADE,related_name="Section")
    verified= models.BooleanField(default=False)
    description= models.TextField("description",max_length=150,null=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    class Meta:
        managed = True
        verbose_name = 'Publisher'
        verbose_name_plural = 'Publishers'


class Article(models.Model):
    section= models.ForeignKey(Section,on_delete=models.CASCADE)
    title= models.CharField(max_length=255)
    title_slug= models.SlugField(default="null")
    description= models.TextField()
    keywords= models.CharField(max_length=255,default="null")
    image=models.ImageField(null=True)
    image_source= models.CharField(max_length=255, null=True, blank=True)
    sub_heading = models.CharField(max_length=255,null=True,blank=True)
    body_text= models.TextField()
    pub_date= models.DateTimeField(auto_now_add=True)
    mod_date= models.DateTimeField(null=True)
    publisher= models.ManyToManyField(Publisher)
    view_count= models.IntegerField(default=0)
    publish=models.BooleanField(default=False)

    def bodySnippet(self):
        body= self.body_text[:120]
        bodySnippet= re.sub(r"\s\w+$|(<strong>|</strong>|<em>|</em>|<b>|</b>|<i>|</i>|<u>|</u>|<a.+?>|</a>)","",body)
        return f'{bodySnippet} ....' 
    def __str__(self):
        return self.title
    class Meta:
        managed = True
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        ordering= ['-pub_date']

    def delete(self, *args, **kwargs):
         self.image.delete()
         super().delete(*args, **kwargs)

    def save(self,skip_md=True,*args, **kwargs):
        if skip_md:
            self.mod_date= datetime.datetime.now()    
        super().save(*args, **kwargs) # Call the real save() method

class Sections(models.Model):
    """Model definition for Sections."""
    # TODO: Define fields here
    article= models.ForeignKey(Article, related_name='sections', on_delete=models.CASCADE)
    sub_heading=models.CharField(max_length=255, null=True)
    Sub_section_image= models.ImageField(null=True, blank=True)
    image_source= models.CharField(max_length=255, null=True, blank=True)
    body_text= models.TextField(null=True)
    class Meta:
        """Meta definition for Sections."""
        verbose_name = 'Sections'
        verbose_name_plural = 'Sections'

    def __str__(self):
        """Unicode representation of Sections."""
        return self.sub_heading

    def delete(self, *args, **kwargs):
         self.Sub_section_image.delete()
         super().delete(*args, **kwargs)

@receiver(pre_save, sender=Article)
def delete_Artictle_image(sender, instance, *args, **kwargs):
    if instance.pk:
        article= Article.objects.get(pk=instance.pk)
        if article.image != instance.image:
            article.image.delete(False)


@receiver(pre_save, sender=Sections)
def delete_Sections_image(sender, instance, *args, **kwargs):
    if instance.pk:
        section= Sections.objects.get(pk=instance.pk)
        if section.Sub_section_image != instance.Sub_section_image:
            section.Sub_section_image.delete(False)


        
    