from django.shortcuts import redirect
from companies.models import Company


def add_duplicate(request, pk):
    obj = Company.objects.get(id=pk)
    obj.pk = None
    obj.save()
    return redirect(f'/admin/companies/company/{obj.id}/change/')
