from django.contrib.auth import login, logout
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, FormView, UpdateView

from .forms import FakeSmsAuthForm, InviteCodeForm, UserLoginForm
from .models import CustomUser
from .utils import generate_fake_sms_code


def home_page(request):
    """Домашняя страница"""
    return render(request, 'home.html')


class ProfileInfo(DetailView):
    """Представление для профиля"""

    model = CustomUser
    template_name = 'profile.html'

    def has_permission(self):
        return self.request.user.is_authenticated

    def get_object(self, queryset=None):
        return get_object_or_404(CustomUser,
                                 pk=self.request.session['_auth_user_id'])

    def get(self, request, *args, **kwargs):
        if self.has_permission():
            return super(ProfileInfo, self).get(self, request, *args, **kwargs)
        else:
            return redirect(reverse('referral:login'))

    def get_context_data(self, **kwargs):
        context = super(ProfileInfo, self).get_context_data(**kwargs)
        context['referrers'] = CustomUser.objects.filter(referrer=self.object)
        if not self.get_object().referrer:
            context['form'] = InviteCodeForm(instance=self.get_object())
        return context


class AddReferer(UpdateView):
    model = CustomUser
    template_name = 'profile.html'
    form_class = InviteCodeForm

    def get_form(self, form_class=None):
        return self.form_class(self.request.POST, instance=self.get_object())

    def get_object(self, queryset=None):
        return get_object_or_404(CustomUser,
                                 pk=self.request.session['_auth_user_id'])

    def get_context_data(self, **kwargs):
        context = super(AddReferer, self).get_context_data(**kwargs)
        context['referrers'] = CustomUser.objects.filter(referrer=self.object)
        if not self.get_object().referrer:
            context['form'] = InviteCodeForm(instance=self.get_object())
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.referrer = CustomUser.objects.get(
            invite_code=form.data['referrer_code'])
        form.save()
        return super(AddReferer, self).form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data()
        context['form'] = form
        context['message'] = 'Такого инвайт-кода не существует'
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse('referral:profile-view')


class ProfileView(View):
    def get(self, request, *args, **kwargs):
        print('get')
        view = ProfileInfo.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print('post')
        view = AddReferer.as_view()
        return view(request, *args, **kwargs)


class EditNameView(UpdateView):
    """Представление для изменения имени пользователя"""

    model = CustomUser
    fields = ('username', )

    template_name = 'edit_name.html'

    def get_object(self, queryset=None):
        return get_object_or_404(CustomUser,
                                 pk=self.request.session['_auth_user_id'])

    def get_success_url(self):
        return reverse('referral:profile-view')


class LogInView(FormView):
    """Представление для логина"""

    form_class = UserLoginForm
    template_name = 'login.html'

    def form_valid(self, form):
        self.request.session['phone'] = form.cleaned_data['phone']
        return super(LogInView, self).form_valid(form)

    def get_success_url(self):
        return reverse('referral:auth-check')


class AuthCheckView(FormView):
    """Представление для фейковой аутентификации по смс"""

    form_class = FakeSmsAuthForm
    template_name = 'sms_authentication.html'

    def post(self, request, **kwargs):
        phone = request.session['phone']
        try:
            user = CustomUser.objects.get(phone=phone)
        except CustomUser.DoesNotExist:
            user = CustomUser(phone=phone)
            user.save()

        if not request.user.is_authenticated:
            login(request, user)
        request.session['sms_code'] = generate_fake_sms_code()
        return redirect(reverse('referral:profile-view'))


class LogOutView(View):
    """Представление для логаута"""
    def get(self, request):
        logout(request)
        return redirect(reverse('referral:profile-view'))
