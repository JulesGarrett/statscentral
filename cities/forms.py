from django import forms
from cities.models import CityReviews


class CreateReviewForm(forms.ModelForm):
    class Meta:
        model = CityReviews
        fields = ['City','Comments', 'Rating']


class UpdateReviewForm(forms.ModelForm):

    class Meta:
        model = CityReviews
        fields = ['City','Comments', 'Rating']

    def save(self, commit=True):
        review = self.instance
        review.City = self.cleaned_data['City']
        review.Comments = self.cleaned_data['Comments']
        review.Rating = self.cleaned_data['Rating']

        if commit:
            review.save()
        return review
