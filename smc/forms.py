from django import forms
from .models import MenuItem

class OrderForm(forms.Form):
    roll_id = forms.CharField(label='Roll ID', max_length=10, widget=forms.TextInput(attrs={'id': 'roll_id'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        menu_items = MenuItem.objects.all()
        self.fields['menu_items'] = [item for item in menu_items]
        for item in menu_items:
            field_name = f"item_{item.item_id}"
            field_label = f"{item.name} - ${item.price}"
            self.fields[field_name] = forms.BooleanField(label=field_label, required=False)
