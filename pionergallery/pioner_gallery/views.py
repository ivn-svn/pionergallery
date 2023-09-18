import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import FormView
from django.views.generic import TemplateView
from django.contrib import messages
from .webapp.forms import ContactForm
from .webapp.models import Contact
from .user_login.models import UserPhoto
from .user_login.forms import ProfilePictureForm
from .user_login.models import UserProfile
from .user_login.forms import UserProfileForm
from .user_login.forms import UserPhotoForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.core.mail import send_mail
import os

from django.shortcuts import render
from django.core.mail import send_mail
from .forms import ContactForm
from .webapp.models import Contact  # Make sure you import the Contact model


# import logging
# logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# views.py


class Custom500View(TemplateView):
    template_name = 'pioner_gallery/errors/500.html'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        response.status_code = 500
        return response


class Custom404View(TemplateView):
    template_name = 'pioner_gallery/errors/404.html'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        response.status_code = 404
        return response


class UserGalleryView(View):
    def get(self, request, username):
        viewed_user = get_object_or_404(User, username=username)
        user_photos = UserPhoto.objects.filter(user=viewed_user)
        context = {
            'user_photos': user_photos,
            'viewed_user': viewed_user,
        }
        return render(request, 'pioner_gallery/user_gallery.html', context)


class EditGalleryView(UserGalleryView):

    def get(self, request, username):
        # Reuse the logic from the parent class to fetch photos
        user = get_object_or_404(User, username=username)
        user_photos = UserPhoto.objects.filter(user=request.user)
        context = {
            'user_photos': user_photos,
            'user': user,
            'edit_mode': True  # Set the edit_mode flag here
        }
        return render(request, 'pioner_gallery/user_gallery.html', context)

    def post(self, request, username):
        # Get the ID of the photo to delete from the POST data
        photo_id_to_delete = request.POST.get('photo_id')

        # Fetch the photo that belongs to the user and has the specified ID
        try:
            photo_to_delete = UserPhoto.objects.get(user=request.user, id=photo_id_to_delete)
            photo_to_delete.delete()
            messages.success(request, "Photo was deleted successfully!")
        except UserPhoto.DoesNotExist:
            messages.error(request, "Photo not found.")

        # Redirect back to the edit gallery page
        return redirect(reverse('edit_gallery', args=[request.user.username]))


class UploadPhotoView(LoginRequiredMixin, FormView):
    template_name = 'pioner_gallery/upload_photo.html'
    form_class = UserPhotoForm

    def form_valid(self, form):
        photo = form.save(commit=False)
        photo.user = self.request.user
        photo.save()
        return redirect(reverse('user_gallery', args=[self.request.user.username]))


class EditUploadedPhoto(UploadPhotoView):

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        photo_id = self.kwargs.get('photo_id')
        photo = UserPhoto.objects.get(id=photo_id)
        kwargs['instance'] = photo
        return kwargs

    def form_valid(self, form):
        # The form will handle updating the instance
        form.save()
        return redirect(reverse('user_gallery', args=[self.request.user.username]))


class UploadProfilePictureView(LoginRequiredMixin, FormView):
    template_name = 'pioner_gallery/edit_user_profile.html'
    form_class = ProfilePictureForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = UserProfile.objects.get(user=self.request.user)
        return kwargs

    def form_valid(self, form):
        form.save()
        return redirect('user_profile')


class EditUserProfileDetailsView(LoginRequiredMixin, FormView):
    template_name = 'pioner_gallery/edit_user_profile.html'
    form_class = UserProfileForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = UserProfile.objects.get(user=self.request.user)
        return kwargs

    def form_valid(self, form):
        form.save()
        return redirect('user_profile')


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('cover_page')


def newsfeed(request):
    photo_directory = os.path.join(settings.BASE_DIR, "staticfiles", "images", "gallery", "watermarked")
    photos = os.listdir(photo_directory)
    photos_list = sorted(photos, reverse=True)  # Sort the photos list in descending order
    print(photos_list)
    context = {
        'photo_urls': photos_list
    }
    return render(request, 'pioner_gallery/newsfeed.html', context)


def gallery(request):
    photo_directory = os.path.join(settings.BASE_DIR, "staticfiles", "images", "gallery", "watermarked")
    photos = os.listdir(photo_directory)
    photos_list = []
    for photo in photos:
        photos_list.append(photo)
    context = {
        'photo_urls': photos_list
    }
    return render(request, 'pioner_gallery/gallery.html', context)


def page_list(request):
    return render(request, 'pioner_gallery/page/list.html')


def blog(request):
    return render(request, 'pioner_gallery/blog.html')


# from pioner_gallery.webapp.models import Article, Category


from .webapp.models import Article


def home_page(request):
    articles = Article.objects.all().order_by('-created_at')[:6]  # Fetch the latest 6 articles.
    context = {
        'articles': articles,
    }
    # print(article.author)
    print(articles)
    return render(request, "pioner_gallery/home.html", context)


@login_required
def marketplace(request):
    # return render(request, "pioner_gallery/marketplace_dashboard.html")
    return render(request, "pioner_gallery/marketplace_dashboard.html")


def cover_page(request):
    return render(request, 'pioner_gallery/cover.html')


def contact_page(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Create a new Contact instance
            contact = Contact()

            # Assign the form data to the Contact fields
            contact.first_name = form.cleaned_data['first_name']
            contact.last_name = form.cleaned_data['last_name']
            contact.email = form.cleaned_data['email']
            contact.message_subject = form.cleaned_data['message_subject']
            contact.message_body = form.cleaned_data['message_body']

            # Save the contact to the database
            contact.save()

            # Section for E-mail sending:
            subject = 'New Contact Submission from ' + form.cleaned_data['first_name']
            message = 'You have received a new contact form submission from ' + form.cleaned_data['first_name'] + ' ' + \
                      form.cleaned_data['last_name'] + '. Email: ' + form.cleaned_data[
                          'email'] + '. Message Subject: ' + \
                      form.cleaned_data['message_subject'] + '. Message Body: ' + form.cleaned_data['message_body']
            send_mail(subject, message, 'iv.svetlin@outlook.com', ['isvetllin@gmail.com'])
            # End of E-mail sending section.

            # Redirect or show a success message
            return render(request, 'pioner_gallery/contact_success.html')
    else:
        form = ContactForm()

    return render(request, 'pioner_gallery/contact.html', {'form': form})


def user_login(request):
    context = {
        'page_title': 'User Login Page',
    }
    if request.method == 'POST':
        email = request.POST.get('floatingInput')
        password = request.POST.get('floatingPassword')

        try:
            # Get the user by email
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user is not None and user.check_password(password):
            login(request, user)
            print('Logged in now')
            context['login_success'] = 'Successfully logged in!'
            return render(request, 'registration/register.html', context)  # Redirect as needed
        else:
            context['login_error'] = 'Invalid credentials. Please try again.'

    return render(request, 'pioner_gallery/user_login.html', context)


def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        subscribe = request.POST.get('subscribe', False)

        # Check if the email is unique before creating a new user
        if not User.objects.filter(email=email).exists():
            # Create a new user in the database
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name,
                                            last_name=last_name)
            print(f"Created user: {user}")

            # Create a UserProfile instance for the user and link it to the user
            user_profile = UserProfile.objects.create(user=user, email=email, username=username)
            messages.success(request, f'User profile created: {username}')
            print(f"Created UserProfile: {user_profile}")
            # Authenticate the user (log them in immediately after registration)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page or desired URL after successful registration
                #  messages.success(request, 'Registration successful! You are now logged in.')
                return redirect('user_login')

            else:
                # Handle registration failure (e.g., username already taken)
                messages.error(request, 'Registration failed. Please try again.')
                print("Authentication failed.")
        else:
            # Handle registration failure (e.g., email already taken)
            messages.warning(request, 'Email already exists. Please choose another one.')
            print("Email already exists.")
    return render(request, 'registration/index.html')


@login_required
def user_profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    print(user_profile)
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()

    # Create a new form for the profile picture upload
    form = ProfilePictureForm(instance=user_profile)

    return render(request, 'pioner_gallery/profile.html', {
        'user_profile': user_profile,
        'form': form,
    })


@login_required
def delete_user_profile(request):
    if request.method == "POST":
        try:
            profile = UserProfile.objects.get(user=request.user)
            user = profile.user
            profile.delete()  # This will delete the profile
            user.delete()  # This will delete the user
            messages.success(request, "Your profile has been deleted!")
        except UserProfile.DoesNotExist:
            messages.error(request, "User profile not found.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
        return redirect('user_login')
    else:
        # Handle the GET request
        return render(request, 'pioner_gallery/delete_confirmation.html')


@login_required
def delete_confirmation(request):
    return render(request, 'pioner_gallery/delete_confirmation.html')


def privacy(request):
    return render(request, 'pioner_gallery/privacy.html')


def terms(request):
    return render(request, 'pioner_gallery/terms.html')


@require_POST
def cookie_consent(request):
    data = json.loads(request.body)
    consent = data.get('consent')

    # Check if user is authenticated
    if request.user.is_authenticated:
        # Save decision to the database
        profile = request.user.userprofile
        profile.cookie_consent = consent
        profile.save()
    else:
        # Save to session for anonymous users
        request.session['cookie_consent'] = consent

    return JsonResponse({"status": "success"})
