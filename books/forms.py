from django import forms

from books.models import Book, Issue
from members.models import Member


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ['created_at', 'updated_at']


class CopyFormManual(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['code', 'book']


class CopyFormAuto(forms.ModelForm):
    count = forms.IntegerField()

    class Meta:
        model = Issue
        fields = ['book']


class IssueForm(forms.Form):
    member = forms.ModelChoiceField(queryset=Member.objects.all(), required=False)
    member_id = forms.CharField(max_length=6, required=False)


class RenewForm(forms.Form):
    settle_fine = forms.IntegerField(required=False)
