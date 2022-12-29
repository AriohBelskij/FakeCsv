from django import forms
from extra_views import InlineFormSetFactory
from django.forms import TextInput
from fakedata.models import FakeSchema, Column, DataSet


class FakeSchemaForm(forms.ModelForm):
    title = forms.CharField(
        widget=TextInput(attrs={"placeholder": "Name for new schema"})
    )

    class Meta:
        model = FakeSchema
        fields = "__all__"
        widgets = {"author": forms.HiddenInput()}


class ColumnForm(forms.ModelForm):
    column_name = forms.CharField(
        required=True,
        widget=TextInput(attrs={"placeholder": "Name for column"}),
    )

    class Meta:
        model = Column
        fields = "__all__"


class ColumnInline(InlineFormSetFactory):
    model = Column
    form_class = ColumnForm

    fields = "__all__"

    factory_kwargs = {
        "extra": 1,
        "max_num": None,
        "can_order": False,
        "can_delete": True,
    }


class DataSetForm(forms.ModelForm):
    rows = forms.IntegerField(
        label="",
        widget=forms.NumberInput(attrs={"placeholder": "Number of rows"}),
    )

    class Meta:
        model = DataSet
        fields = ("rows",)
