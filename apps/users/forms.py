from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "phone", "avatar"]
        widgets = {
            "email": forms.EmailInput(attrs={"id": "EMAIL", "name": "EMAIL_EDIT"}),
            "phone": forms.TextInput(attrs={"id": "PHONE", "name": "PHONE_EDIT"}),
            "first_name": forms.TextInput(
                attrs={"id": "FIRST_NAME", "name": "FIRST_NAME_EDIT"}
            ),
            "last_name": forms.TextInput(
                attrs={"id": "LAST_NAME", "name": "LAST_NAME_EDIT"}
            ),
            "avatar": forms.ClearableFileInput(
                attrs={"id": "AVATAR", "name": "AVATAR_EDIT"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            base_class = "form-control fs_24 ps-2 SelfStorage__input"
            if field_name == "avatar":
                base_class = "form-control"
            field.widget.attrs["class"] = base_class
            field.widget.attrs["placeholder"] = field.label
