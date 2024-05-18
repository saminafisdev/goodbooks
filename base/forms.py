from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from .models import Review

RATING_CHOICES = [
    (1, "1"),
    (2, "2"),
    (3, "3"),
    (4, "4"),
    (5, "5"),
]


class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Review
        fields = ["review_text", "rating"]
        widgets = {
            "review_text": forms.Textarea(attrs={"rows": 4, "cols": 40}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("review_text", css_class="form-control mb-3"),
            Field("rating", css_class="form-control mb-3"),
            Submit("submit", "Save", css_class="btn btn-primary"),
        )
