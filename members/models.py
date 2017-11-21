from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property

from StackLibrary.my_settings import SETTINGS


class Member(models.Model):
    id_code = models.CharField(unique=True, max_length=10, null=False, blank=True)
    full_name = models.CharField(max_length=40)
    date_of_birth = models.DateField(null=True, blank=True)
    course = models.CharField(max_length=40)
    phone = models.CharField(max_length=12)
    fine = models.IntegerField(default=0)

    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.id and SETTINGS.id_auto_generate and not self.id_code:
            self.id_code = self.get_id_code()
        return super().save()

    def issued_books(self):
        return self.issued_to.all()

    @cached_property
    def add_fine(self):
        try:
            books = self.issued_books().annotate(extra_days=models.Sum(models.F('next_renewal_date')-timezone.now().date(),
                                                                       output_field=models.DurationField()))
            for book in books:
                if book.extra_days.days > 0:
                    self.fine += book.extra_days.days
            self.save()
        finally:
            return self.fine

    def remove_fine(self, amt=0):
        if amt:
            self.fine -= amt
        else:
            self.fine = 0
        self.save()

    def get_id_code(self):
        if Member.objects.count() == 0:
            return "M{:05}".format(1)
        else:
            return "M{:05}".format(int(Member.objects.latest('date_joined').id_code.lstrip('M'))+1)
