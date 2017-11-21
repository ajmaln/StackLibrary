from django import forms

from members.models import Member


class MyDateField(forms.DateField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('input_formats', ("%d/%m/%Y",))
        super(MyDateField, self).__init__(*args, **kwargs)

    def widget_attrs(self, widget):
        widget.attrs['class'] = 'datepicker'
        return super(MyDateField, self).widget_attrs(widget)


class MemberForm(forms.ModelForm):
    date_of_birth = MyDateField()

    class Meta:
        model = Member
        exclude = ['date_joined', 'updated_at', 'fine']