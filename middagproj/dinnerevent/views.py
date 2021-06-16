from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import ModelFormMixin, FormView
from django.contrib.auth.models import User
from django.views.generic import DeleteView, DetailView, CreateView, UpdateView
from .models import Event, Review, Comment
from .forms import EventForm, ReviewForm, CommentForm


class EventComment(SingleObjectMixin, FormView):
    template_name = "event_detail.html"
    form_class = CommentForm
    model = Event

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        return super(EventComment, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        text = form.cleaned_data['content']
        Comment.objects.create(user=form.instance.user, event=self.object, content=text)
        return super(EventComment, self).form_valid(form)

    def get_success_url(self):
        return reverse('event:eventdetail', kwargs={'pk': self.object.pk})


class ReviewCreate(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = "dinnerevent/event_review_form.html"
    model = Review
    form_class = ReviewForm

    def form_valid(self, form_class):
        form_class.instance.user = self.request.user
        self.Review = form_class.save(commit=False)
        self.Review.event = Event.objects.get(pk=self.kwargs['pk'])
        self.Review.save()
        evt = self.Review.event
        message = f'Anmeldelse av {evt} ble opprettet'
        messages.success(self.request, message)
        return super(ReviewCreate, self).form_valid(form_class)

    def get_context_data(self, **kwargs):
        context = super(ReviewCreate, self).get_context_data(**kwargs)
        event = Event.objects.get(pk=self.kwargs['pk'])
        context['event'] = event
        return context

    def get_success_url(self):
        return reverse_lazy('event:eventdetail', kwargs={'pk': self.kwargs['pk']})

    def test_func(self):
        event_reviews = Review.objects.filter(event__pk=self.kwargs['pk']).filter(user_id=self.request.user.id)
        if not event_reviews:
            return True
        return False


class EventDetail(DetailView):
    model = Event

    def get_context_data(self, **kwargs):
        context = super(EventDetail, self).get_context_data(**kwargs)
        event_review_by_user = User.objects.filter(review__event=self.object).filter(id=self.request.user.id)
        context['user_has_made_event_review'] = event_review_by_user
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        view = EventComment.as_view()
        return view(request, *args, **kwargs)


class EventCreate(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm

    def form_valid(self, form_class):
        form_class.instance.user = self.request.user
        self.Event = form_class.save(commit=False)
        self.Event.save()
        form_class.save_m2m()
        return HttpResponseRedirect(reverse('event:eventdetail', args=(self.Event.id,)))


class EventUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView, ModelFormMixin):
    model = Event
    form_class = EventForm
    template_name_suffix = '_update_form'

    def form_valid(self, form_class):
        form_class.instance.user = self.request.user
        self.Event = form_class.save(commit=False)
        self.Event.save()
        form_class.save_m2m()
        return HttpResponseRedirect(reverse('event:eventdetail', args=(self.Event.id,)))

    def test_func(self):
        event = self.get_object()
        if self.request.user == event.user:
            return True
        return False


class EventDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event

    success_url = '/'

    def test_func(self):
        event = self.get_object()
        if self.request.user == event.user:
            return True
        return False


def join_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.guests.count() >= event.seats:
        messages.error(request, 'Dette arrangementet er fullt.')
        return HttpResponseRedirect(reverse('event:eventdetail', args=[str(pk)]))
    events = Event.objects.all()
    for e in events:
        if request.user in e.guests.all():
            if e.time == event.time:
                messages.error(request, f'Du er påmeldt til et annet arrangement kl {event.time}.')
                return HttpResponseRedirect(reverse('event:eventdetail', args=[str(pk)]))
    event.guests.add(request.user)
    request.user.profile.events.add(event)
    messages.success(request, f"Du har blitt meldt på dette arrangementet, {request.user.username} !")
    return HttpResponseRedirect(reverse('event:eventdetail', args=[str(pk)]))


def unjoin_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    event.guests.remove(request.user)
    request.user.profile.events.remove(event)
    messages.success(request, f"Du har blitt meldt av dette arrangementet, {request.user.username} !")
    return HttpResponseRedirect(reverse('event:eventdetail', args=[str(pk)]))
