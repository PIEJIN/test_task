from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (ObjectViewSet, VisitViewSet, create_visit, end_visit,
                    get_report, login_view, report_api, start_visit)

app_name = 'meetings'

router = DefaultRouter()

router.register(r'objects', ObjectViewSet, basename='objects')
router.register(r'visits', VisitViewSet, basename='visits')

urlpatterns = [

    path('', include(router.urls)),
    path('objects/create/<int:id>/', create_visit, name='create_visit'),
    path('objects/start/<int:id>/', start_visit, name='start_visit'),
    path('objects/end/<int:id>/', end_visit, name='end_visit'),
    path('report/', get_report, name='get_report'),
    path('reportapi/', report_api, name='report_api'),
    path('login/', login_view, name='login'),
]
