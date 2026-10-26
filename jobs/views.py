
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Job, Category


def home(request):
    jobs = Job.objects.filter(is_active=True).select_related(
        "company", "category"
    ).order_by("-created_at")[:6]

    categories = Category.objects.all().order_by("name")

    return render(request, "home.html", {
        "jobs": jobs,
        "categories": categories,
    })


def job_list(request):
    jobs = Job.objects.filter(is_active=True).select_related(
        "company", "category"
    ).order_by("-created_at")

    search_query = request.GET.get("q", "").strip()
    category_id = request.GET.get("category", "").strip()

    if search_query:
        jobs = jobs.filter(
            Q(title__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(location__icontains=search_query)
        )

    if category_id.isdigit():
        jobs = jobs.filter(category_id=int(category_id))

    categories = Category.objects.all().order_by("name")

    return render(request, "job_list.html", {
        "jobs": jobs,
        "categories": categories,
        "search_query": search_query,
        "selected_category": category_id,
    })


def job_detail(request, job_id):
    job = get_object_or_404(
        Job.objects.select_related("company", "category"),
        id=job_id,
        is_active=True,
    )

    return render(request, "job_detail.html", {"job": job})
