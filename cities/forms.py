from django import forms
from cities.models import CityReviews


class CreateReviewForm(forms.ModelForm):
    class Meta:
        model = CityReviews
        fields = ['City','Comments', 'Rating', 'author']
