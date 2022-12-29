from django.urls import path

from fakedata.views import (
    Login,
    SchemaListView,
    SchemaCreateView,
    SchemaEdit,
    SchemaDeleteView,
    DataSetsView,
)

urlpatterns = [
    path("", Login.as_view(), name="index"),
    path("schemas/", SchemaListView.as_view(), name="schema-list"),
    path("schemas/create/", SchemaCreateView.as_view(), name="schema-create"),
    path("schemas/<int:pk>/", DataSetsView.as_view(), name="schema-detail"),
    path("schemas/edit/<int:pk>/", SchemaEdit.as_view(), name="schema-edit"),
    path(
        "schemas/<int:pk>/delete/",
        SchemaDeleteView.as_view(),
        name="schema-delete",
    ),
]

app_name = "fakedata"
