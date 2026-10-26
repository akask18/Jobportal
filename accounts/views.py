
from django.contrib.auth import login
from django.db import transaction
from django.shortcuts import render, redirect

from .forms import RegisterForm, CompanyProfileForm
from .models import UserProfile


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        company_form = CompanyProfileForm(request.POST)

        if form.is_valid():
            role = form.cleaned_data["role"]

            if role == "company" and not company_form.is_valid():
                return render(request, "register.html", {
                    "form": form,
                    "company_form": company_form,
                })

            with transaction.atomic():
                user = form.save()
                UserProfile.objects.create(user=user, role=role)

                if role == "company":
                    company = company_form.save(commit=False)
                    company.user = user
                    company.save()

            login(request, user)
            return redirect("home")

    else:
        form = RegisterForm()
        company_form = CompanyProfileForm()

    return render(request, "register.html", {
        "form": form,
        "company_form": company_form,
    })
