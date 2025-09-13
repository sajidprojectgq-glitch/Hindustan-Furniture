from django import forms
from .models import CategorizePost

class FurnitureForm(forms.ModelForm):
    class Meta:
        model = CategorizePost
        fields = [
            "title",
            "type",
            "price",
            "discount_price",
            "stock",
            "brand",
            "material",
            "color",
            "width",
            "height",
            "depth",
            "img",
            "description",
            "is_featured",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }
