from django import forms, template


register = template.Library()


@register.filter
def checkbox(field):
    return isinstance(field.field.widget, forms.CheckboxInput)


@register.filter
def bootstrap_widget(field):
    css_class = "form-check-input" if checkbox(field) else "form-control"
    if field.errors:
        css_class += " is-invalid"
    return field.as_widget(attrs={"class": css_class})
