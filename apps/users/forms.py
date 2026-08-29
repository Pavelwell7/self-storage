from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            upper_name = field_name.upper()
            field.widget.attrs["id"] = upper_name

            if not isinstance(field.widget, forms.FileInput):
                field.widget.attrs["name"] = f"{upper_name}_EDIT"

            if field_name == "avatar":
                field.widget.attrs.update(
                    {"class": "form-control", "accept": "image/*"}
                )
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs["class"] = "form-control"
            else:
                field.widget.attrs["class"] = (
                    "form-control fs_24 ps-2 SelfStorage__input"
                )

            if field.label and "placeholder" not in field.widget.attrs:
                field.widget.attrs["placeholder"] = field.label


class UserProfileForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "phone", "avatar"]
