from django.core import serializers
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls.base import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from StackLibrary.my_settings import SETTINGS
from books.forms import BookForm, CopyFormAuto, CopyFormManual, IssueForm, RenewForm
from books.models import Book, Issue
from members.exceptions import MaximumIssuedBooks, MaximumRenewalCount
from members.models import Member


class IndexView(ListView):
    model = Book
    template_name = 'books/index.html'


class BookCreateView(SuccessMessageMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'books/book_create.html'
    success_url = reverse_lazy('books:create')
    success_message = '%(title)a added successfully'


class BookEditView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'books/book_create.html'
    success_url = reverse_lazy('books:index')


class BookDetailsView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'


class BookDeleteView(DeleteView):
    model = Book
    template_name = 'books/book_delete.html'
    success_url = reverse_lazy('books:index')
    success_message = '\'{}\' deleted Successfully'

    def delete(self, request, *args, **kwargs):
        messages.success(request, self.success_message.format(self.get_object().title))
        return super(BookDeleteView, self).delete(request, *args, **kwargs)


class CopyCreateView(CreateView):
    model = Issue
    template_name = 'books/issue_create.html'
    success_url = reverse_lazy('books:copy_create')

    def get_form_class(self):
        if SETTINGS.id_auto_generate:
            return CopyFormAuto
        else:
            return CopyFormManual

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['book'] = Book.objects.get(id=self.kwargs['pk'])
        finally:
            return context

    def get_initial(self):
        initial = super().get_initial()
        try:
            initial['book'] = Book.objects.get(id=self.kwargs['pk'])
        finally:
            return initial

    @transaction.atomic
    def form_valid(self, form):
        if SETTINGS.id_auto_generate:
            count = form.cleaned_data['count']
            for i in range(0, count):
                self.model.objects.create(book=form.cleaned_data['book'])
            messages.success(self.request, "Copies created Successfully")
            return redirect('books:copy_create')
        else:
            return super().form_valid(form)


class IssueView(View):
    template_name = 'books/issue_copy.html'
    issue_form_class = IssueForm
    renew_form_class = RenewForm
    form_class = None

    def get_object(self, code):
        return Issue.objects.get(code=code)

    def get_form_class(self, book):
        if book.is_available:
            return self.issue_form_class
        else:
            return self.renew_form_class

    def get(self, request, code=None):
        try:
            self.object = self.get_object(code)
            form = self.get_form_class(self.object)(None)
            if not self.object.is_available and self.object.issued_to.add_fine == 0:
                form.fields['settle_fine'].widget.attrs['disabled'] = True
            return render(request, self.template_name, {'copy': self.object, 'form': form})
        except Issue.DoesNotExist:
            messages.add_message(request, messages.INFO, 'Object with code {} does not exist'.format(code))
            return redirect('library:index')

    def post(self, request, code):
        copy = Issue.objects.get(code=code)
        form = self.get_form_class(copy)(request.POST)
        if form.is_valid():
            if copy.is_available:
                try:
                    if form.cleaned_data['member'] is not None:
                        copy.issue(form.cleaned_data['member'])
                    elif form.cleaned_data['member_id'] is not None:
                        member = Member.objects.get(id_code=form.cleaned_data['member_id'])
                        copy.issue(member)
                    else:
                        return render(request, self.template_name, {'copy': copy, 'form': form,
                                      'messages': ['Please enter a member id or choose one from the list']})
                    return redirect('members:details', copy.issued_to.id)
                except MaximumIssuedBooks as e:
                    return render(request, self.template_name,
                                  {
                                      'copy': copy,
                                      'form': form,
                                      'messages': [e.message]
                                  })
            else:
                if form.cleaned_data['settle_fine']:
                    if not copy.issued_to.fine < form.cleaned_data['settle_fine']:
                        copy.issued_to.remove_fine(form.cleaned_data['settle_fine'])
                    else:
                        return render(request, self.template_name,
                                      {
                                          'copy': copy,
                                          'form': form,
                                          'messages': ['Amount entered is greater than existing fine!']
                                      })
                try:
                    r = copy.renew()
                    r.fine = form.cleaned_data['settle_fine']
                except MaximumRenewalCount as e:
                    return render(request, self.template_name, {'copy': copy, 'form': form, 'messages': [e.message]})
        return render(request, self.template_name, {'copy': copy, 'form': form})


class ReturnView(View):
    template_name = 'books/issue_return.html'
    success_url = reverse_lazy('books:')

    def get(self, request, code):
        return render(request, self.template_name, {'object': self.get_object(code)})

    def get_object(self, code):
        return Issue.objects.get(code=code)

    def post(self, request, code):
        book = self.get_object(code)
        member = book.issued_to
        book.return_book()
        return redirect('members:details', member.id)


class SearchBooks(View):
    @csrf_exempt
    def post(self, request):
        query = request.POST['search_string']
        result = (Book.objects.filter(title__icontains=query) | Book.objects.filter(author__icontains=query) | Book.objects.filter(category__icontains=query)).distinct()
        data = serializers.serialize('json', result)
        return HttpResponse(data)
