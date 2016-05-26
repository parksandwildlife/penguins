from django import forms
from datetime import date
from datetimewidget.widgets import DateWidget


class SelectDateForm(forms.Form):
    select_date = forms.DateField(required=False, initial=date.today())

    def __init__(self, *args, **kwargs):
        super(SelectDateForm, self).__init__(*args, **kwargs)
        self.fields['select_date'].widget.attrs.update({'class': 'datepicker'})


class GraphForm(forms.Form):
    start_date = forms.DateField(
        widget=DateWidget(
            attrs={
                'id': "startTime",
                'width': '45%'},
            usel10n=False,
            bootstrap_version=3))
    end_date = forms.DateField(
        widget=DateWidget(
            attrs={
                'id': "endTime"},
            usel10n=False,
            bootstrap_version=3))

    def clean(self):
        cleaned_data = super(GraphForm, self).clean()
        start = cleaned_data.get("start_date")
        end = cleaned_data.get("end_date")
        if not start:
            self._errors['start_date'] = self.error_class(
                ["Please enter a start date"])
        if not end:
            self._errors['end_date'] = self.error_class(
                ["Please enter an end date"])
        if start and end and (end <= start):
            raise forms.ValidationError(
                "The end date is before the start date!")
        return cleaned_data
