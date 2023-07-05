from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, DetailView, ListView, DeleteView, TemplateView

from blog.models import Blog
from postapp.forms import MailingForm
from postapp.models import Mailing, Client, Message, MailingAttempt
from postapp.services import cache_message


class HomePageView(TemplateView):
    template_name = 'postapp/home.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['count_mailing_all'] = Mailing.objects.all().count()
        context_data['count_mailing_active'] = Mailing.objects.filter(mailing_status=Mailing.CREATED).count()
        context_data['count_unique_clients'] = Client.objects.distinct().count()
        context_data['blog'] = Blog.objects.all().order_by('?')[:3]
        return context_data


class ClientListView(LoginRequiredMixin, ListView):
    model = Client

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.has_perm('postapp.set_mailing_status'):
            return queryset

        return queryset.filter(user=self.request.user)


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    fields = ('email', 'full_name', 'comments')
    success_url = reverse_lazy('postapp:client_list')

    def form_valid(self, form):
        client = form.save()
        client.user = self.request.user
        client.save()
        return super().form_valid(form)


class ClientUpdateView(UserPassesTestMixin, UpdateView):
    model = Client
    fields = ('email', 'full_name', 'comments')
    success_url = reverse_lazy('postapp:client_list')

    def test_func(self):
        client = self.get_object()
        user = self.request.user
        return user.is_authenticated and (client.user == user or user.has_perm('postapp.change_client'))


class ClientDeleteView(UserPassesTestMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('postapp:client_list')

    def test_func(self):
        client = self.get_object()
        user = self.request.user
        return user.is_authenticated and (client.user == user or user.has_perm('postapp.delete_client'))


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.has_perm('postapp.view_mailing'):
            return queryset

        return queryset.filter(user=self.request.user)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.has_perm('postapp.view_mailing') or self.request.user == self.object.user:
            return self.object
        raise HttpResponseForbidden


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('postapp:mailing_list')

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.save()
        return super().form_valid(form)


class MailingUpdateView(UserPassesTestMixin, UpdateView):
    model = Mailing
    fields = '__all__'
    success_url = reverse_lazy('postapp:mailing_list')

    def test_func(self):
        mailing = self.get_object()
        user = self.request.user
        return user.is_authenticated and (mailing.user == user or user.has_perm('postapp.change_mailing'))


class MailingDeleteView(UserPassesTestMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('postapp:mailing_list')

    def test_func(self):
        mailing = self.get_object()
        user = self.request.user
        return user.is_authenticated and (mailing.user == user or user.has_perm('postapp.delete_mailing'))


class MessageListView(LoginRequiredMixin, ListView):
    model = Message

    def get_queryset(self):
        queryset = cache_message(Message, 'message')
        if self.request.user.has_perm('postapp.set_mailing_status'):
            return queryset
        return queryset.filter(user=self.request.user)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ('title', 'body',)
    success_url = reverse_lazy('postapp:message_list')

    def form_valid(self, form):
        message = form.save()
        message.user = self.request.user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(UserPassesTestMixin, UpdateView):
    model = Message
    fields = ('title', 'body',)
    success_url = reverse_lazy('postapp:message_list')

    def test_func(self):
        message = self.get_object()
        user = self.request.user
        return user.is_authenticated and (message.user == user or user.has_perm('postapp.change_message'))


class MessageDeleteView(UserPassesTestMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('postapp:message_list')

    def test_func(self):
        message = self.get_object()
        user = self.request.user
        return user.is_authenticated and (message.user == user or user.has_perm('postapp.delete_message'))


class MailingAttemptListView(LoginRequiredMixin, ListView):
    model = MailingAttempt
    template_name = 'postapp/mailing_attempt_list.html'


@permission_required(perm='postapp.set_mailing_status')
def set_mailing_status(request, pk):
    obj = get_object_or_404(Mailing, pk=pk)
    if obj:
        obj.mailing_status = Mailing.CREATED
        obj.save()
    return redirect(request.META.get('HTTP_REFERER'))
