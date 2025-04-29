from django import forms
from django.urls import reverse


class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)
    model_choice = forms.ChoiceField(
        choices=[('all', 'All Books'), ('books_data', 'Books Data'), ('story_book', 'Story Books'), ('history_book', 'History Books')],
        required=False
    )
    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'pk': self.pk})