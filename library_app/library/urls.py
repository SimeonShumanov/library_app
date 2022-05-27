from django.urls import path

from library_app.library.views import home_page, RegisterStudentView, search_books, LoginStudentView, LogoutStudentView, \
    ProfileDetails, AllBooksView, BookDetails, SuccessfulRentView, rent_book, StudentRentedBooksView, \
    StudentAccountEditView, ReturnBookView

urlpatterns = [
    path('', home_page, name='index'),
    path('register/', RegisterStudentView.as_view(), name='register'),
    path('search/', search_books, name='search books'),
    path('login/', LoginStudentView.as_view(), name='login'),
    path('logout/', LogoutStudentView.as_view(), name='logout'),
    path('profile/<pk>/', ProfileDetails.as_view(), name='details'),
    path('books/', AllBooksView.as_view(), name='books'),
    path('books/<pk>/', BookDetails.as_view(), name='book details'),
    path('succesful/', SuccessfulRentView.as_view(), name='successful rent'),
    path('rent/<pk>', rent_book, name='rent book'),
    path('rented/', StudentRentedBooksView.as_view(), name='rented books'),
    path('<pk>/update/', StudentAccountEditView.as_view(), name='edit account'),
    path('<pk>/return-book/', ReturnBookView.as_view(), name='return book')

]
