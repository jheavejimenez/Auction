from django import forms
from .models import Listing, User_Comment, Bid


choices = [
    ('Sneakers', 'Sneakers'),
    ('Fashion', 'Fashion'),
    ('Collectibles', 'Collectibles'),
    ('Handbags', 'Handbags')
]


class CreateListing(forms.ModelForm):
    class Meta:
        model = Listing
        fields = (
            'Title',
            'Descriptions',
            'itemImage',
            'category',
            'startingBid'
        )

        widgets = {
            'Title': forms.TextInput(attrs={
                'class': 'input-animation input-box',
                'placeholder': 'Title',
                'autocomplete': 'off'
            }),
            'Descriptions': forms.Textarea(attrs={
                'class': 'input-animation input-box text-box',
                'placeholder': 'Descriptions',
                'autocomplete': 'off'
            }),
            'itemImage': forms.TextInput(attrs={
                'class': 'input-animation input-box',
                'placeholder': 'Image URL',
                'autocomplete': 'off'
            }),
            'category': forms.Select(attrs={
                'class': 'select'}, choices=choices),
            'startingBid': forms.TextInput(attrs={
                'class': 'input-animation',
                'autocomplete': 'off',
                'placeholder': '$'
            })

        }


class CommentForm(forms.ModelForm):
    content = forms.CharField(label="", widget=forms.Textarea(attrs={
        'class': 'input-animation input-box Comment-box',
        'placeholder': 'Write a Comment',
        'autocomplete': 'off'
    }))

    class Meta:
        model = User_Comment
        fields = ['content']


class NewBidForm(forms.ModelForm):
    offer = forms.CharField(label="", widget=forms.TextInput(attrs={
        'class': 'input-animation input-box',
        'placeholder': 'Place your Bid Here',
        'autocomplete': 'off'
    }))

    class Meta:
        model = Bid
        fields = ['offer']
