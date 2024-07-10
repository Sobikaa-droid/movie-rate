from django import forms

from .models import MovieReview


class MovieReviewForm(forms.ModelForm):
    rating = forms.IntegerField(max_value=10, min_value=1, label='Rating')

    class Meta:
        model = MovieReview
        fields = ['title', 'memo', 'rating']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # Removes ':' as label suffix

        for field_name, field in self.fields.items():
            if field.required:
                field.label = f'{field.label}*'