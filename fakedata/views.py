from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.http import JsonResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import FormMixin
from extra_views import CreateWithInlinesView, UpdateWithInlinesView
from sweetify.views import SweetifySuccessMixin

from fakedata.forms import FakeSchemaForm, ColumnInline, DataSetForm
from fakedata.generator import generate_csv
from fakedata.models import FakeSchema, DataSet


class Login(LoginView):
    template_name = "registration/login.html"
    success_url = reverse_lazy("fakedata:schema-list")


class SchemaListView(LoginRequiredMixin, generic.ListView):
    model = FakeSchema
    queryset = FakeSchema.objects.all()
    paginate_by = 5
    template_name = "fakedata/schemalist.html"


class SchemaCreateView(
    LoginRequiredMixin, SweetifySuccessMixin, CreateWithInlinesView
):
    model = FakeSchema
    form_class = FakeSchemaForm
    inlines = [
        ColumnInline,
    ]
    template_name = "fakedata/schema-form.html"
    success_message = "Done!"

    def get_initial(self):
        return {"author": self.request.user}

    def get_success_url(self):
        if "action" in self.request.POST:
            if self.request.POST["action"] == "add_column":
                return reverse_lazy(
                    "fakedata:schema-edit", kwargs={"pk": self.object.id}
                )
            if self.request.POST["action"] == "submit":
                return reverse_lazy("fakedata:schema-list")
        return reverse_lazy("fakedata:schema-list")


class SchemaEdit(
    LoginRequiredMixin, SweetifySuccessMixin, UpdateWithInlinesView
):
    model = FakeSchema
    form_class = FakeSchemaForm
    inlines = [
        ColumnInline,
    ]
    template_name = "fakedata/schema-form.html"
    success_message = "Done!"

    def get_success_url(self):
        if "action" in self.request.POST:
            if self.request.POST["action"] == "add_column":
                return reverse_lazy(
                    "fakedata:schema-edit", kwargs={"pk": self.object.pk}
                )
            return reverse_lazy("fakedata:schema-list")


class SchemaDeleteView(
    LoginRequiredMixin, SweetifySuccessMixin, generic.DeleteView
):
    model = FakeSchema
    success_url = reverse_lazy("fakedata:schema-list")
    success_message = "Schema was delete! "


def is_ajax(request):
    return request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"


class DataSetsView(LoginRequiredMixin, FormMixin, generic.DetailView):
    model = FakeSchema
    form_class = DataSetForm
    template_name = "fakedata/datasets.html"
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super(DataSetsView, self).get_context_data(**kwargs)
        schema = self.get_object()
        context["column"] = schema.column.all()
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        schema = self.get_object()
        dataset = DataSet.objects.create(
            schema=schema, rows=int(request.POST["rows"])
        )
        if is_ajax(request):
            generate_csv(dataset)
            link = DataSet.objects.filter(schema=schema).first().download_link
            html = render_to_string(
                "fakedata/table.html",
                context={"fakeschema": schema, "download_link": link},
                request=request,
            )
            return JsonResponse(
                {
                    "msg": html,
                    "link": link,
                }
            )
        return HttpResponseRedirect(
            reverse_lazy("fakedata:schema-detail", kwargs={"pk": schema.pk})
        )
