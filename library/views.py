from django.shortcuts import render, redirect
from django.urls.base import reverse_lazy
from django.views.generic.base import TemplateView, View

from books.models import Issue
from library.models import Register
from members.models import Member


class IndexView(View):
    template_name = 'library/index.html'

    def get(self, request):
        return render(request, self.template_name, {'transactions': Register.objects.all().order_by('-date')[:10]})

    def post(self, request):
        code = request.POST['code']
        if code.startswith('M'):
            try:
                member = Member.objects.get(id_code=code)
            except Member.DoesNotExist:
                return render(request, self.template_name, {'transactions': Register.objects.all().order_by('-date')[:10], 'messages': 'member with {} id does not exist'.format(code)})
            return redirect('members:details', member.id)
        else:
            book = Issue.objects.get(code=code)
            return redirect('books:issue', book.code)
