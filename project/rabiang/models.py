from django.db import models


class Site(models.Model):
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Theme(models.Model):
    name = models.CharField(max_length=255)
    site = models.ForeignKey(Site, related_name='themes')
    menu = models.ManyToManyField('Menu')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Menu(models.Model):
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=512)
    menu = models.ForeignKey(Menu, related_name='menuItems')
    parent = models.ForeignKey('self', null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Module(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=512)
    site = models.ForeignKey(Site, related_name='modules')
    theme = models.ForeignKey(Theme, related_name='modules')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Document(models.Model):
    title = models.CharField(max_length=255)
    module = models.ForeignKey(Module, related_name='documents')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    document = models.ForeignKey(Document, related_name='comments')
    parent = models.ForeignKey('self', null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'commeted at {}'.format(self.created)


class Attachment(models.Model):
    document = models.ForeignKey(Document, related_name='files')
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
