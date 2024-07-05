from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from job_parser.models import Vacancy
import requests


def get_vacancies(request):
    api_url = "https://api.hh.ru/vacancies" 
    headers = {
        "HH-User-Agent": "JobParser/0.1.0 (kryukov.aan@mail.ru)"
    }
    body = {
        "page": 0,
        "per_page": 100,
    }

    if request.method == "POST":
        fields = ["text", "salary", "currency", "experience", "employment"]
        for field in fields: 
            field_value = request.POST.get(field)
            if field_value and field_value != "null":
                body[field] = field_value
        
        if "salary" in body:
                body['only_with_salary'] = True

        response = requests.get(url=api_url, headers=headers, params=body)

        if response.status_code == 200:
            data = response.json()

            request.session['pages'] = int(data['pages'])
            request.session['current_page'] = int(data['page'])
            request.session['body'] = body
            for item in data["items"]:
                parse_json(item)

    return create_filters(body.copy())

def load_also_vacancies(request, pages):
    
    api_url = "https://api.hh.ru/vacancies"
    headers = {"HH-User-Agent": "JobParser/0.1.0 (kryukov.aan@mail.ru)"}

    for i in range(pages):

        body = request.session["body"]
        body["page"] += 1
        request.session["body"] = body

        response = requests.get(url=api_url, headers=headers, params=request.session["body"])
        if response.status_code == 200:
            data = response.json()
            for item in data["items"]:
                if not Vacancy.objects.filter(id=item["id"]).exists():
                    parse_json(item)

def create_filters(filters):  
    try:
        del filters["page"], filters["per_page"], filters["only_with_salary"]
    except:
        pass

    filter_params = {}

    if "text" in filters:
        filter_params['vacancy_name__icontains'] = filters['text']
        del filters["text"]
        
    if "currency" in filters:
        if "salary" not in filters:
             del filters["currency"]
        filter_params['currency'] = filters['currency']

    if "salary" in filters:
        try:
            salary = int(filters['salary'])
            filter_params['min_salary__gte'] = salary - (salary * 0.3)
            filter_params['max_salary__lte'] = salary + (salary * 0.3)
            del filters["salary"]
        except ValueError:
            pass

    filter_params.update(filters)
    return filter_params

def parse_json(item):
    vacancy_data = {
        "id": item["id"],
        "vacancy_name": item["name"].lower(),
        "archived": item["archived"],
        "area": item["area"]["name"],
        "information": (item["snippet"]["requirement"] if item["snippet"]["requirement"] else "-") + "\n" + (item["snippet"]["responsibility"] if item["snippet"]["responsibility"] else "-"),
        "min_salary": item["salary"]["from"] if item["salary"] and item["salary"]["from"] else 0,
        "max_salary": item["salary"]["to"] if item["salary"] and item["salary"]["to"] else 2**31 - 1,
        "currency": item["salary"]["currency"] if item["salary"] and item["salary"]["currency"] else "RUR",
        "schedule": item["schedule"]["name"],
        "professional_roles": item["professional_roles"][0]["name"],
        "employment": item["employment"]["id"],
        "experience": item["experience"]["id"],
        "published_at": item["published_at"], 
        "url": item["alternate_url"],
    }
    vacancy, created = Vacancy.objects.update_or_create(id=item["id"], defaults=vacancy_data)
    if not created: 
        print("Vacancy updated")

def index(request, start=True):
    list_session_arguments = ["filters", "pages", "body"]
    for session_item in list_session_arguments:
        if session_item in request.session:
            del request.session[session_item]
    return render(request, "index.html", {"start": start})

def vacancies_list(request, filters={}):
    
    if "filters" in request.session:
        filters = request.session["filters"]
    else:
        filters = get_vacancies(request)
        request.session["filters"] = filters
        load_also_vacancies(request, 3)
        
    list_vacancies = Vacancy.objects.filter(**filters)

    paginator = Paginator(list_vacancies, 90)
    page_num = request.GET.get("page")
    page_obj = paginator.get_page(page_num)
    if request.session['pages'] - request.session["body"]["page"] >= 3:
        load_also_vacancies(request, 3)
    else:
        load_also_vacancies(request, request.session['pages'] - request.session["body"]["page"] - 1)
    return render(request, "list_vacancies.html", {"page_obj": page_obj, "count": paginator.object_list.__len__()})