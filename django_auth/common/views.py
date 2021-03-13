from django.views.generic import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from common.forms import ProfileCreationForm
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy
from common.models import UserProfile
from allauth.socialaccount.models import SocialAccount
from django.shortcuts import render
import uuid

# Create your views here.
def index(request):
    context = {}
    if request.user.is_authenticated:
        context['username'] = request.user.username
        context['age'] = SocialAccount.objects.get(provider='github', user=request.user).extra_data['age']
        context['sex'] = SocialAccount.objects.get(provider='github', user=request.user).extra_data['sex']
        context['city'] = SocialAccount.objects.get(provider='github', user=request.user).extra_data['city']
        context['id'] = SocialAccount.objects.get(provider='github', user=request.user).uid
    return render(request, 'index.html', context)


class RegisterView(FormView):
    form_class = UserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('common:profile-create')

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        login(self.request, authenticate(username=username, password=raw_password))
        return super(RegisterView, self).form_valid(form)

class CreateUserProfile(FormView):
    form_class = ProfileCreationForm
    template_name = 'profile-create.html'
    success_url = reverse_lazy('common:index')

    def dispatch(self, request, *args, **kwargs):

        if self.request.user.is_anonymous:
            return HttpResponseRedirect(reverse_lazy('common:login'))
        return super(CreateUserProfile, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        socialacc = SocialAccount.objects.create(provider='github', user=self.request.user, uid = uuid.uuid4())
        socialacc.extra_data['age'] = form.cleaned_data.get('age')
        socialacc.extra_data['sex'] = form.cleaned_data.get('sex')
        socialacc.extra_data['city'] = form.cleaned_data.get('city')
        socialacc.save()
        return super(CreateUserProfile, self).form_valid(form)