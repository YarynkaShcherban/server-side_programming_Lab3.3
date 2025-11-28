from django import forms
from store.models import Book, Publisher, Author, Genre

class BookForm(forms.ModelForm):
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Book
        fields = ['name', 'isbn', 'price', 'publisher', 'author', 'genres']
        widgets = {
            'author': forms.CheckboxSelectMultiple(),
            'publisher': forms.Select(),
            'genres': forms.CheckboxSelectMultiple(),
        }

    def save(self, commit=True):
        book = super().save(commit=False)
        if commit:
            book.save()
            self.save_m2m()
            book.genres.set(self.cleaned_data['genres'])
        return book