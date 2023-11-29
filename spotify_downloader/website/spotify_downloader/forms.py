from django import forms

class linkForm(forms.Form):
    musicLink = forms.CharField(widget=forms.TextInput(attrs={'class' : "form-control", 'id' : "exampleInputEmail1"}), max_length=200, required=True)

    def __init__(self, *args, **kwargs):
        super(linkForm, self).__init__(*args, **kwargs)
        self.fields['musicLink'].label = ""
