from django import forms
from cities.models import CityReviews


class CreateReviewForm(forms.ModelForm):
    class Meta:
        model = CityReviews
        fields = ['City','State','Comments', 'Rating']


class UpdateReviewForm(forms.ModelForm):

    class Meta:
        model = CityReviews
        fields = ['Comments', 'Rating']

    def save(self, commit=True):
        review = self.instance
        review.Comments = self.cleaned_data['Comments']
        review.Rating = self.cleaned_data['Rating']

        if commit:
            review.save()
        return review
