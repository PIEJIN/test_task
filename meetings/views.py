from datetime import datetime
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import redirect, render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Visit, Object, User
from .serializers import (VisitSerializer, ObjectSerializer,
                          VisitCreateSerializer, UserSerializer,
                          ReportSerializer)


# ViewSet для работы с пользователями
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Отображение списка пользователей
    def list(self, request, *args, **kwargs):
        return render(request, 'index.html',)

    # Отображение информации о пользователе
    def retrieve(self, request, *args, **kwargs):
        return render(request, 'index.html',)


# ViewSet для работы с объектами
class ObjectViewSet(viewsets.ModelViewSet):
    queryset = Object.objects.all()
    serializer_class = ObjectSerializer

    # Отображение списка объектов
    def list(self, request, *args, **kwargs):
        obj = Object.objects.all()
        user = self.request.user
        context = {'object': obj, 'user': user}
        return render(request, 'index.html', context)

    # Отображение информации об объекте
    def retrieve(self, request, *args, **kwargs):
        obj = Object.objects.all()
        return render(request, 'index.html', {'object': obj})


# ViewSet для работы с визитами
class VisitViewSet(viewsets.ModelViewSet):
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer

    # Определение класса сериализатора
    def get_serializer_class(self):
        if self.action == 'create':
            return VisitCreateSerializer
        return VisitSerializer

    # Отображение списка визитов
    def list(self, request, *args, **kwargs):
        visit = Visit.objects.all()
        return render(request, 'index.html', {'visit': visit})

    # Отображение информации о визите
    def retrieve(self, request, *args, **kwargs):
        visit = Visit.objects.all()
        return render(request, 'index.html', {'visit': visit})


# Создание визита
def create_visit(request, id):
    obj = Object.objects.get(pk=id)
    user = request.user
    Visit.objects.create(visiter=user, objct=obj)
    return redirect('/api/objects/')


# Авторизация пользователя
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/api/objects/')
        else:
            return render(request, 'login.html', {'error': 'Invalid login'})
    return render(request, 'login.html')


# Начало визита
def start_visit(request, id):
    visit = Visit.objects.get(id=id)
    if not visit.is_started:
        visit.is_started = True
        visit.started = datetime.now()
        visit.save()
        return redirect('/api/objects/')


# Окончание визита
def end_visit(request, id):
    visit = Visit.objects.get(id=id)
    if visit.is_started:
        visit.is_ended = True
        visit.ended = datetime.now()
        visit.save()
        return redirect('/api/objects/')


# Генерация отчета
def generate_report(user, start_date, end_date):
    all_visits = Visit.objects.filter(visiter=user)
    ended_visits = Visit.objects.filter(
        visiter=user,
        is_ended=True,
        started__gt=start_date,
        ended__lt=end_date
        )
    planed_visits = Visit.objects.filter(visiter=user, is_ended=False)
    objects_visited_by_user = Object.objects.filter(
        visits__visiter=user,
        visits__is_ended=True,
        visits__started__gt=start_date,
        visits__ended__lt=end_date
    )
    unic_objects_visited_by_user = objects_visited_by_user.distinct()
    len_of_user_objects = len(unic_objects_visited_by_user)
    objects_count = {}
    for obj in unic_objects_visited_by_user:
        objects_count[obj.name] = Visit.objects.filter(
            objct=obj,
            visiter=user,
            is_ended=True,
            started__gt=start_date,
            ended__lt=end_date
        ).count()
    context = {
        'start_date': start_date,
        'end_date': end_date,
        'all_visits': all_visits,
        'ended_visits': ended_visits,
        'planed_visits': planed_visits,
        'len_of_user_objects': len_of_user_objects,
        'objects_count': objects_count,
        'unic_objects_visited_by_user': unic_objects_visited_by_user
    }
    return context


# Получение отчета
def get_report(request):
    user = request.user
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        # Проверка наличия дат и их валидация
        if start_date and end_date:
            context = generate_report(user, start_date, end_date)
            return render(request, 'report.html', context)
        else:
            return HttpResponse("Укажите обе даты.")
    else:
        return render(request, 'report.html', context)


# API для получения отчета
@api_view(['POST'])
def report_api(request):
    user = request.user
    start_date = request.data.get('start_date')
    end_date = request.data.get('end_date')
    if start_date and end_date:
        context = generate_report(user, start_date, end_date)
        serializer = ReportSerializer(context)
        return Response(serializer.data)
    else:
        return Response({"error": "Укажите обе даты."}, status=400)
