import json

from django.conf import settings
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .models import Skills, Vacancy


def hello(request):
    return HttpResponse("Hello World!")


@method_decorator(csrf_exempt, name="dispatch")
class VacancyView(ListView):
    model = Vacancy

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()

        search_text = request.GET.get("text")
        if search_text:
            self.object_list = self.object_list.filter(text=search_text)
        self.object_list = self.object_list.order_by("text")

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        vacancies = [
            {"id": vacancy.id, "text": vacancy.text}
            for vacancy in page_obj
        ]

        return JsonResponse({
            "items": vacancies,
            "num_pages": paginator.num_pages,
            "total": paginator.count,
        }, safe=False)


class UserVacancyDetailView(View):
    def get(self, request):
        user_qs = User.objects.annotate(vacancies=Count("vacancy_set"))

        paginator = Paginator(user_qs, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        users = [
            {
                "id": user.id,
                "username": user.username,
                "vacancies": user.vacancies,
            }
            for user in page_obj
        ]

        return JsonResponse({
            "items": users,
            "total": paginator.count,
            "num_pages": paginator.num_pages,
        })


@method_decorator(csrf_exempt, name="dispatch")
class VacancyCreateView(CreateView):
    model = Vacancy
    fields = ["user", "slug", "text", "status", "skills"]

    def get(self, request, *args, **kwargs):
        return JsonResponse({"error": "Method not allowed"}, status=405)

    def post(self, request):
        vacancy_data = json.loads(request.body)
        vacancy = Vacancy.objects.create(
            user_id=vacancy_data["user_id"],
            slug=vacancy_data["slug"],
            text=vacancy_data["text"],
            status=vacancy_data["status"],
        )
        return JsonResponse({
            "id": vacancy.id,
            "slug": vacancy.slug,
            "text": vacancy.text,
            "status": vacancy.status,
            "created": str(vacancy.created),
            "user": vacancy.user_id,
            "skills": [s.name for s in vacancy.skills.all()],
        })


@method_decorator(csrf_exempt, name="dispatch")
class VacancyDetailView(DetailView):
    model = Vacancy

    def get(self, request, *args, **kwargs):
        vacancy = self.get_object()
        return JsonResponse({
            "id": vacancy.id,
            "slug": vacancy.slug,
            "text": vacancy.text,
            "status": vacancy.status,
            "created": str(vacancy.created),
            "user": vacancy.user_id,
            "skills": [s.name for s in vacancy.skills.all()],
        })


@method_decorator(csrf_exempt, name="dispatch")
class VacancyUpdateView(UpdateView):
    model = Vacancy
    fields = ["user", "slug", "text", "status", "skills"]

    def get(self, request, *args, **kwargs):
        return JsonResponse({"error": "Method not allowed"}, status=405)

    def patch(self, request, *args, **kwargs):
        self.object = self.get_object()
        vacancy_data = json.loads(request.body)

        self.object.slug = vacancy_data["slug"]
        self.object.text = vacancy_data["text"]
        self.object.status = vacancy_data["status"]

        for skill_name in vacancy_data["skills"]:
            try:
                skill_obj = Skills.objects.get(name=skill_name)
            except Skills.DoesNotExist:
                return JsonResponse({"error": "skill not found"}, status=404)
            self.object.skills.add(skill_obj)

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "text": self.object.text,
            "slug": self.object.slug,
            "status": self.object.status,
            "created": str(self.object.created),
            "user": self.object.user_id,
            "skills": list(self.object.skills.all().values_list("name", flat=True)),
        })


@method_decorator(csrf_exempt, name="dispatch")
class VacancyDeleteView(DeleteView):
    model = Vacancy
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({"status": "ok"}, status=200)
