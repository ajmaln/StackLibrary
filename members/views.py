from django.contrib import messages
from django.shortcuts import render
from django.urls.base import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from books.exceptions import AlreadyIssuedException
from books.models import Issue
from members.exceptions import MaximumIssuedBooks
from members.forms import MemberForm
from members.models import Member


class IndexView(ListView):
    model = Member
    template_name = 'members/index.html'


class MemberCreateView(CreateView):
    model = Member
    template_name = 'members/create.html'
    form_class = MemberForm
    success_url = reverse_lazy('members:create')


class MemberDetailView(DetailView):
    model = Member
    template_name = 'members/details.html'

    def post(self, request, pk):
        book_id = ''
        try:
            self.object = self.model.objects.get(id=pk)
            book_id = self.request.POST['book_id']
            book = Issue.objects.get(code=book_id)
            book.issue(user=self.object)
        except Issue.DoesNotExist:
            messages.warning(request, 'Book with book code : {} does not exist'.format(book_id))
        except MaximumIssuedBooks as e:
            messages.warning(request, e.message)
        except AlreadyIssuedException as e:
            messages.warning(request, e.message.format(book.issued_to))
        return render(request, self.template_name, self.get_context_data())


class MemberEditView(UpdateView):
    model = Member
    template_name = 'members/create.html'
    form_class = MemberForm
    success_url = reverse_lazy('members:index')
