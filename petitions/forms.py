from django import forms
from .models import Petition

class PetitionForm(forms.ModelForm):
    class Meta:
        model = Petition
        fields = Petitionfields = ['title', 'description', 'movie_title', 'movie_year', 'movie_director']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Petition title (e.g. "Add Inception to our catalog")'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Why should this movie be added? What makes it special?'}),
            'movie_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Movie title'}),
            'movie_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Release year (optional)'}),
            'movie_director': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Director name (optional)'}),
        }

    def __int__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].required = True
        self.fields['description'].required = True
        self.fields['movie_title'].required = True
        self.fields['movie_year'].required = False
        self.fields['movie_director'].required = False