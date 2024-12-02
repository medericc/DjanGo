from django import forms
from .models import Match, Highlight, Season

class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['date', 'opponent', 'points', 'assists', 'rebounds', 'steals', 'blocks', 'turnovers']

class HighlightForm(forms.ModelForm):
    class Meta:
        model = Highlight
        fields = ['title', 'description', 'media', 'match']

class SeasonForm(forms.ModelForm):
    class Meta:
        model = Season
        fields = ['year', 'matches']
        widgets = {
            'matches': forms.CheckboxSelectMultiple()
        }
