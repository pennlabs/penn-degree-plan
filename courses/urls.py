from django.urls import path

from . import views
urlpatterns = [
    path('<slug:semester>/sections/', views.SectionList.as_view()),
    path('<slug:semester>/courses/', views.CourseList.as_view()),
    path('<slug:semester>/courses/<slug:full_code>/',  views.CourseDetail.as_view()),
]
