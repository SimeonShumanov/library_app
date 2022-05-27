from django import forms
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.forms import SelectDateWidget
from django.shortcuts import render, redirect
from datetime import date

# Create your views here.
from django.urls import reverse_lazy
from django.views import generic

from library_app.library.models import Book, UserModel, StudentUser, RentedBook

current_year = date.today().year


def home_page(request):
    return render(request, 'index.html')


class StudentRegistrationForm(UserCreationForm):
    university = forms.CharField(max_length=50)
    date_of_birth = forms.DateField(widget=SelectDateWidget(years=range(1920, current_year + 1)))

    class Meta:
        model = UserModel
        fields = ('username', 'password1', 'password2',)

    def save(self, commit=True):
        user = super().save(commit=commit)

        profile = StudentUser(university=self.cleaned_data['university'],
                              date_of_birth=self.cleaned_data['date_of_birth'],
                              user=user)
        if commit:
            profile.save()
        return user


class StudentUpdateForm(forms.ModelForm):
    university = forms.CharField(max_length=50)
    date_of_birth = forms.DateField(widget=SelectDateWidget(years=range(1920, current_year + 1)))

    class Meta:
        model = UserModel
        fields = ['username']

    def save(self, commit=True):
        user = super().save(commit=commit)
        student_profile = StudentUser.objects.get(user_id=user.id)
        student_profile.university = self.cleaned_data['university']
        student_profile.date_of_birth = self.cleaned_data['date_of_birth']
        if commit:
            student_profile.save()
        return user


class RegisterStudentView(generic.CreateView):
    form_class = StudentRegistrationForm
    template_name = 'register_student.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        result = super().form_valid(form)
        login(self.request, self.object)
        return result


class LoginStudentView(LoginView):
    template_name = 'login_student.html'
    success_url = reverse_lazy('index')


class LogoutStudentView(LogoutView):
    pass


class ProfileDetails(generic.DetailView):
    model = UserModel
    template_name = 'profile_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_profile = StudentUser.objects.get(pk=self.object.id)
        context['student'] = student_profile
        return context


class AllBooksView(generic.ListView):
    model = Book
    template_name = 'browse_all_books.html'


class BookDetails(generic.DetailView):
    model = Book
    template_name = 'book_details.html'


class SuccessfulRentView(generic.TemplateView):
    template_name = 'success_rent.html'


def rent_book(request, pk):
    if request.method == "GET":
        rented_books = RentedBook.objects.all()
        rent = RentedBook(student_id=request.user.pk, book_id=pk)
        rent.student_id = request.user.id
        rent.book_id = pk
        if rented_books:
            for item in rented_books:
                if item.student_id == rent.student_id and item.book_id == int(rent.book_id):
                    return redirect('index')
        rent.save()
        return redirect('successful rent')


class StudentRentedBooksView(generic.ListView):
    model = RentedBook
    template_name = "view_student_rented_books.html"

    def get_queryset(self):
        student_rented_books = []
        queryset = super().get_queryset().filter(student_id=self.request.user.pk)
        for item in queryset:
            book_to_add = Book.objects.get(id=item.book_id)
            student_rented_books.append(book_to_add)
        return student_rented_books

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book_to_return = RentedBook.objects.filter(student_id=self.request.user.pk)
        context['books'] = book_to_return
        return context


class StudentAccountEditView(generic.UpdateView):
    model = UserModel
    form_class = StudentUpdateForm
    template_name = 'edit_account.html'
    success_url = reverse_lazy('index')


class ReturnBookView(generic.DeleteView):
    model = RentedBook
    success_url = reverse_lazy('index')




# def register(request):
#     if request.method == "POST":
#         student_form = RegisterForm(request.POST)
#         if student_form.is_valid():
#             student_form.save()
#             return redirect('index')
#     else:
#         student_form = RegisterForm()
#         context = {
#             'student_form': student_form
#         }
#         return render(request, 'register_student.html', context)


def search_books(request):
    if request.method == "POST":
        searched = request.POST.get('searched')
        searched_book = Book.objects.filter(name__icontains=searched).all()
        if searched.strip() == "":
            return render(request, 'index.html')
        context = {
            'search': searched_book,
        }
        return render(request, 'search_books.html', context)
