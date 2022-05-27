from django.contrib import admin

from library_app.library.models import Book, StudentUser, RentedBook


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    pass


@admin.register(StudentUser)
class StudentAdmin(admin.ModelAdmin):
    pass


@admin.register(RentedBook)
class RentedBookAdmin(admin.ModelAdmin):
    pass
