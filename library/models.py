from django.db import models


class LibraryManager(models.Manager):
    def get_settings(self):
        return LibrarySettings.objects.get(id=1)


class LibrarySettings(models.Model):
    initial_setup = models.BooleanField(default=False)
    id_auto_generate = models.BooleanField(default=True)
    no_of_books = models.IntegerField(default=5000)
    max_book_per_member = models.IntegerField(default=3)
    issue_duration = models.IntegerField(default=14)
    fine_after_deadline = models.IntegerField(default=1)
    maximum_renewals = models.IntegerField(default=-1)

    objects = LibraryManager()


class Register(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=40)
    details = models.CharField(max_length=40)
    fine = models.IntegerField(null=True)
    member_involved = models.ForeignKey('members.Member', related_name='member_involved')

    def __str__(self):
        return str(self.date) + '-' + self.details + '-' + self.type

