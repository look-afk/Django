import json
from os import name
from django.http import HttpResponse,JsonResponse
from django.views.generic import DetailView,ListView,CreateView,UpdateView,DeleteView
from django.views import View
from .models import Skills, Vacancy
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
# Create your views here.
def hello(request):
    return HttpResponse("Hello World!")




@method_decorator(csrf_exempt,name="dispatch")
class VacancyView(ListView):
    model = Vacancy
    

    def get(self,request,*args,**kwargs):
            super().get(request,*args,**kwargs)
            
            search_text = request.GET.get("text",None)
            if search_text:
                self.object_list = self.object_list.filter(text=search_text)
            
            respone = []
            for vacancy in self.object_list:
                respone.append({
                    "id": vacancy.id,
                    "slug": vacancy.slug,
                    "text": vacancy.text,
                    "status": vacancy.status,
                    "created": str(vacancy.created),
                    "user": vacancy.user_id,
                    "skills": [s.name for s in vacancy.skills.all()],
                })
            return JsonResponse(respone,safe=False,json_dumps_params={"ensure_ascii":True})
    



@method_decorator(csrf_exempt, name="dispatch")
class VacancyCreateView(CreateView):
     model = Vacancy
     fields = ["user","slug","text","status","skills"]
     def get(self, request, *args, **kwargs):
            return JsonResponse({"error": "Method not allowed"}, status=405)

     def post(self,request):
            vacancy_data = json.loads(request.body)
            vacancy = Vacancy.objects.create(
                user_id = vacancy_data["user_id"],
                slug = vacancy_data["slug"],
                text = vacancy_data["text"],
                status = vacancy_data["status"]
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
    def get(self,request, *args,**kwargs):
        if request.method == "GET":
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
     fields = ["user","slug","text","status","skills"]
     def get(self, request, *args, **kwargs):
            return JsonResponse({"error": "Method not allowed"}, status=405)

     def patch(self,request,*args,**kwargs):
            super().get(request,*args,**kwargs)
            vacancy_data = json.loads(request.body)
            
            self.object.slug = vacancy_data["slug"]
            self.object.text = vacancy_data["text"]
            self.object.status = vacancy_data["status"]
            

            for skills in vacancy_data["skills"]:
                try:
                    skill_obj = Skills.objects.get(name=skills)
                except Skills.DoesNotExist:
                    return JsonResponse({"Error: skill not found! :("}, status = 405)
                self.object.skills.add(skill_obj)
            
            self.object.save()
            
            return JsonResponse({
                "id": self.object.id,
                "text": self.object.text,
                "slug": self.object.slug,
                "status": self.object.status,
                "created": self.object.created,
                "user": list(self.object.skills.all().values_list("name",flat = True)),
                
            },safe=False)

@method_decorator(csrf_exempt,name="dispatch")     
class VacancyDeleteView(DeleteView):
     model = Vacancy
     success_url = "/"

     def delete(self,request,*args,**kwargs):
         self.object = self.get_object()
         self.object.delete()

         return JsonResponse({"status":"ok"},status=200)