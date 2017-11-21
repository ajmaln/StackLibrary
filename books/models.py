from django.db import models
from django.utils import timezone

from StackLibrary.my_settings import SETTINGS
from books.exceptions import AlreadyIssuedException
from library.models import Register
from members.exceptions import MaximumIssuedBooks, MaximumRenewalCount
from members.models import Member


class Book(models.Model):
    title = models.CharField(max_length=40)
    book_code = models.CharField(unique=True, max_length=4, blank=True)
    author = models.CharField(max_length=40, null=True, blank=True)
    publisher = models.CharField(max_length=40, null=True, blank=True)
    category = models.CharField(max_length=40, null=True)
    price = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.id and not self.book_code and SETTINGS.id_auto_generate:
            self.book_code = self.get_code()
        return super().save()

    def available_copies(self):
        return self.issues.filter(is_available=True).count()

    def get_code(self):
        if Book.objects.count() == 0:
            return "{:04}".format(1)
        else:
            return "{:04}".format(int(Book.objects.latest('created_at').book_code)+1)


class Issue(models.Model):
    code = models.CharField(max_length=10, unique=True)
    book = models.ForeignKey(Book, related_name='issues', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_available = models.BooleanField(default=True)
    issued_to = models.ForeignKey(Member, related_name='issued_to', null=True)
    issued_date = models.DateTimeField(null=True)
    renewed_date = models.DateTimeField(null=True)
    return_date = models.DateTimeField(null=True)

    next_renewal_date = models.DateField(null=True)
    renewal_count = models.IntegerField(default=0)

    last_issued_to = models.ForeignKey(Member, related_name='last_issued_to', null=True)
    last_issued_date = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.book) + '-' + self.code

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if SETTINGS.id_auto_generate and not self.id:
            self.code = self.get_code()
        return super().save(force_insert, force_update, using, update_fields)

    def issue(self, user):
        if not self.is_available:
            raise AlreadyIssuedException
        if user.issued_books().count() == SETTINGS.max_book_per_member:
            raise MaximumIssuedBooks
        self.issued_to = user
        self.issued_date = timezone.now()
        self.next_renewal_date = self.issued_date + timezone.timedelta(days=SETTINGS.issue_duration)
        self.is_available = False
        Register.objects.create(member_involved=self.issued_to, type='Issue', details='{}'.format(self.book.title))
        self.save()

    def renew(self):
        if self.renewal_count == SETTINGS.maximum_renewals and SETTINGS.maximum_renewals >= 0:
            raise MaximumRenewalCount
        self.renewal_count += 1
        self.renewed_date = timezone.now()
        self.next_renewal_date = self.renewed_date + timezone.timedelta(days=SETTINGS.issue_duration)
        log = Register.objects.create(member_involved=self.issued_to, type='Renew', details='{}'.format(self.book.title))
        self.save()
        return log

    def return_book(self):
        self.renewal_count = 0
        self.is_available = True
        self.last_issued_date = self.issued_date
        self.last_issued_to = self.issued_to
        log = Register.objects.create(member_involved=self.issued_to, type='Return', details='{}'.format(self.book.title))
        self.issued_to = None
        self.return_date = timezone.now()
        self.save()
        return log

    def get_code(self):
        return self.book.book_code + str(self.book.issues.count()+1)

    @property
    def renewal_available(self):
        if self.is_available:
            raise Exception
        else:
            return True if (self.next_renewal_date - timezone.now().date()).days <= 3 else False
