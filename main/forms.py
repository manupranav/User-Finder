from django import forms

# Reordering Form and View


class SearchForm(forms.Form):
    name = forms.CharField(strip=False)
