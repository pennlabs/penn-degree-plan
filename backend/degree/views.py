from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django_auto_prefetching import AutoPrefetchViewSetMixin
from rest_framework import generics, status, viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from courses.models import Course
from degree.models import DegreePlan, UserDegreePlan
from degree.serializers import (
    DegreePlanDetailSerializer,
    DegreePlanListSerializer,
    UserDegreePlanDetailSerializer,
    UserDegreePlanListSerializer
)
from PennCourses.docs_settings import PcxAutoSchema


class DegreeList(generics.ListAPIView):
    """
    Retrieve a list of (all) degrees available from a given year.
    """

    schema = PcxAutoSchema(
        response_codes={
            "degree-list": {"GET": {200: "[DESCRIBE_RESPONSE_SCHEMA]Degrees listed successfully."}}
        },
    )

    serializer_class = DegreePlanListSerializer

    def get_queryset(self):
        year = self.kwargs["year"]
        queryset = DegreePlan.objects.filter(year=year)
        return queryset


class DegreeDetail(generics.RetrieveAPIView):
    """
    Retrieve a detailed look at a specific degree. Includes all details necessary to display degree
    info, including degree requirements that this degree needs.
    """

    schema = PcxAutoSchema(
        response_codes={
            "degree-detail": {
                "GET": {200: "[DESCRIBE_RESPONSE_SCHEMA]Degree detail retrieved successfully."}
            }
        },
    )

    serializer_class = DegreePlanDetailSerializer
    queryset = DegreePlan.objects.all()

class UserDegreePlanViewset(AutoPrefetchViewSetMixin, viewsets.ModelViewSet):
    """
    list, retrieve, create, destroy, and update user degree plans.
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = UserDegreePlan.objects.filter(person=self.request.user)
        queryset = queryset.prefetch_related(
            "fulfillments",
            "degree_plan",
            "degree_plan__rules",
        )
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return UserDegreePlanListSerializer
        return UserDegreePlanDetailSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({ "request": self.request }) # used to get the user
        return context