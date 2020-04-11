from django import forms
from cities.models import CityReviews


class CreateReviewForm(forms.ModelForm):
    class Meta:
        model = CityReviews
        fields = ['City','Comments', 'Rating']


class UpdateReviewForm(forms.ModelForm):

	class Meta:
		model = CityReviews
		fields = ['title', 'body', 'image']

	def save(self, commit=True):
		review = self.instance
		review.title = self.cleaned_data['title']
		review.body = self.cleaned_data['body']
        review.rating = self.cleaned_data['rating']

		if commit:
			blog_post.save()
		return blog_post
