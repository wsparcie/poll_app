from django import forms
from .models import Poll, Choice

class PollAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = kwargs.pop('choices', 2)
        for i in range(1, choices + 1):
            self.fields[f'choice{i}'] = forms.CharField(
                label=f'Choice {i}',
                max_length=100,
                min_length=1,
                widget=forms.TextInput(attrs={'class': 'form-control'}),
                required=True if i <= 2 else False
            )

    class Meta:
        model = Poll
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'cols': 20}),
        }

    def get_choice_fields(self):
        return [field for field_name, field in self.fields.items() if field_name.startswith('choice')]

class EditPollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['text', ]
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'cols': 20}),
        }

class ChoiceAddForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text', ]
        widgets = {
            'choice_text': forms.TextInput(attrs={'class': 'form-control', })
        }