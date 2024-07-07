from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django_filters.views import FilterView
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph

from .filters import TrainingFilter
from .forms import TrainingForm, ResourceItemFormSet, ResourcePersonFormSet, TrainingFileFormSet
from .models import Training, ResourceItem
from django.views.generic import ListView
from django.views.generic.edit import (
    CreateView, UpdateView
)

def create_training(request):
    if request.method == "POST":
        form = TrainingForm(request.POST)
        formset = ResourceItemFormSet(request.POST)
        if formset.is_valid() & form.is_valid():

            training_new = form.save()
            resource_items = formset.save(commit=False)

            for obj in formset.deleted_objects:
                obj.delete()
            for resource_item in resource_items:
                resource_item.fk_training = training_new
                resource_item.save()

            return redirect('home')

    else:
        form = TrainingForm()
        formset = ResourceItemFormSet()

        context = {
            "form": form,
            "formset": formset
        }

        # return render(request, "training/training_create_or_update.html", context)
        return render(request, "training/create_training.html", context)
def update_training(request, pk):
    training = Training.objects.get(id=pk)
    resource_items = ResourceItem.objects.filter(fk_training=training)
    form = TrainingForm(instance=training)
    formset = ResourceItemFormSet(request.POST or None, instance=training)

    if request.method == "POST":
        form = TrainingForm(request.POST, instance=training)

        if formset.is_valid() & form.is_valid():
            formset.instance = training
            form.save()
            formset.save()
            return redirect("create-training", pk=training.id)

    context = {
        "form": form,
        "formset": formset,
        "training": training,
        "resource_items": resource_items
    }

    # return render(request, "training/training_create_or_update.html", context)
    return render(request, "training/create_training.html", context)

class TrainingInline():
    form_class = TrainingForm
    model = Training
    template_name = "training/training_create_or_update.html"

    def form_valid(self, form):
        print("form_valid")
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        self.object = form.save()


        for name, formset in named_formsets.items():
            print(name)
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                print("formset_save_func is not None")
                formset_save_func(formset)
            else:
                formset.save()
        return redirect('home')

    def formset_training_files_valid(self, formset):
        training_files = formset.save(commit=False)

        for obj in formset.deleted_objects:
            obj.delete()
        for training_file in training_files:
            training_file.fk_training = self.object
            training_file.save()

    def formset_resource_items_valid(self, formset):
        """
        Hook for custom formset saving.Useful if you have multiple formsets
        """
        # print("formset_resource_item_valid")
        resource_items = formset.save(commit=False)  # self.save_formset(formset, contact)
        # add this 2 lines, if you have can_delete=True parameter
        # set in inlineformset_factory func
        for obj in formset.deleted_objects:
            obj.delete()
        for resource_item in resource_items:
            resource_item.fk_training = self.object
            resource_item.save()


    def formset_resource_persons_valid(self, formset):
        """
        Hook for custom formset saving.Useful if you have multiple formsets
        """
        # print("formset_resource_item_valid")
        resource_persons = formset.save(commit=False)  # self.save_formset(formset, contact)
        # add this 2 lines, if you have can_delete=True parameter
        # set in inlineformset_factory func
        for obj in formset.deleted_objects:
            obj.delete()
        for resource_person in resource_persons:
            resource_person.fk_training = self.object
            resource_person.save()


class TrainingCreate(LoginRequiredMixin, TrainingInline, CreateView):

    def get_context_data(self, **kwargs):
        print("get_context_data")
        ctx = super(TrainingCreate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        print("get_named_formsets")
        if self.request.method == "GET":
            return {
                'training_files': TrainingFileFormSet(prefix='training_files'),
                'resource_persons': ResourcePersonFormSet(prefix='resource_persons'),
                'resource_items': ResourceItemFormSet(prefix='resource_items'),
            }
        else:
            return {
                'training_files': TrainingFileFormSet(self.request.POST or None, self.request.FILES or None,
                                                      prefix='training_files'),
                'resource_persons': ResourcePersonFormSet(self.request.POST or None, self.request.FILES or None,
                                                      prefix='resource_persons'),
                'resource_items': ResourceItemFormSet(self.request.POST or None, self.request.FILES or None,
                                                      prefix='resource_items'),
            }


class TrainingUpdate(LoginRequiredMixin, TrainingInline, UpdateView):

    def get_context_data(self, **kwargs):
        ctx = super(TrainingUpdate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        return {
            'training_files': TrainingFileFormSet(self.request.POST or None, self.request.FILES or None,
                                                  instance=self.object, prefix='training_files'),
            'resource_persons': ResourcePersonFormSet(self.request.POST or None, self.request.FILES or None,
                                                  instance=self.object, prefix='resource_persons'),
            'resource_items': ResourceItemFormSet(self.request.POST or None, self.request.FILES or None,
                                                  instance=self.object, prefix='resource_items'),
        }


class GeneratePDF(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="form_letter.pdf"'

        doc = SimpleDocTemplate(response, pagesize=A4)
        # rightMargin=0, leftMargin=0,
        # topMargin=0, bottomMargin=0)

        elements = []
        data = []
        headings = ['ID', 'Name', 'Training Type', 'Start Date', 'End Date', 'City', 'Street Address']
        data.append(headings)
        trainings = Training.objects.all()

        styleSheet = getSampleStyleSheet()
        styleSheet.add(ParagraphStyle(name='Right', alignment=TA_RIGHT))
        styleSheet.add(ParagraphStyle(name='Center', alignment=TA_CENTER))

        for idx, training in enumerate(trainings):
            data.append([
                Paragraph(str(idx + 1), styleSheet["Center"]),
                Paragraph(training.name, styleSheet["BodyText"]),
                Paragraph(training.type.name, styleSheet["BodyText"]),
                Paragraph(str(training.date_start), styleSheet["Center"]),
                Paragraph(str(training.date_end), styleSheet["Center"]),
                Paragraph(training.city.name, styleSheet["BodyText"]),
                Paragraph(training.street_address, styleSheet["BodyText"]),
            ])

        table_style = TableStyle(
            [
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),

            ])

        colWidths = [.5 * inch, 1 * inch, 1 * inch, 1 * inch, 1 * inch, 1 * inch, 1 * inch]

        t = Table(data, style=table_style, colWidths=colWidths, hAlign='LEFT')

        elements.append(t)
        # write the document to disk
        doc.build(elements)

        return response


class TrainingListView(LoginRequiredMixin, FilterView):
    model = Training
    filterset_class = TrainingFilter
    template_name = 'training/home.html'
    paginate_by = 10


def new_training(request):
    if request.method == 'POST':
        form = TrainingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TrainingForm()
    return render(request, 'training/new_training.html', {'form': form})


def edit_training(request, pk):
    training = get_object_or_404(Training, pk=pk)
    if request.method == 'POST':
        form = TrainingForm(request.POST, instance=training)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TrainingForm(instance=training)
    return render(request, 'training/edit_training.html', {'form': form, 'training': training})


def delete_training(request, pk):
    training = get_object_or_404(Training, pk=pk)

    if request.method == 'GET':
        training.delete()
        return redirect('home')
    else:
        return redirect('home')
