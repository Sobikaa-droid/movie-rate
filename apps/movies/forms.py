from django import forms

from .models import MovieReview, MovieRating


class MovieReviewForm(forms.ModelForm):
    impression = forms.IntegerField(max_value=1, min_value=-1)

    class Meta:
        model = MovieReview
        fields = ['title', 'memo', 'impression']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # Removes ':' as label suffix

        for field_name, field in self.fields.items():
            if field.required:
                field.label = f'{field.label}*'


class MovieRatingForm(forms.ModelForm):
    rating = forms.IntegerField(max_value=10, min_value=1)

    class Meta:
        model = MovieRating
        fields = ['rating']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # Removes ':' as label suffix
