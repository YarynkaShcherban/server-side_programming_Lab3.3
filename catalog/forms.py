from django import forms
from store.models import Book, Publisher, Author

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'isbn', 'price', 'publisher', 'author']
        widgets = {
            'author': forms.CheckboxSelectMultiple(),
        }