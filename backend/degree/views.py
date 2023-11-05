from django.shortcuts import render
from rest_framework import generics
from PennCourses.docs_settings import PcxAutoSchema, reverse_func

from degree.models import (
    DegreePlan,
)

from degree.serializers import (
    DegreePlanSerializer,
)


class DegreeList(generics.ListAPIView):
    """
    Retrieve a list of (all) degrees available.
    """

    schema = PcxAutoSchema(
        response_codes={
            reverse_func("degree-list"): {
                "GET": {200: "[DESCRIBE_RESPONSE_SCHEMA]Courses listed successfully."}
            }
        },
    )

    serializer_class = DegreePlanSerializer

    # TODO: Actually return a list of possible degrees
    def get_queryset(self):
        queryset = DegreePlan.filter()
        return queryset


class DegreeListSearch(DegreeList):
    # TODO: unimplemented
    pass


class DegreeDetail(generics.RetrieveAPIView):
    """
    Retrieve a detailed look at a specific degree. Includes all details necessary to display degree
    info, including degree requirements that this degree needs.
    """

    schema = PcxAutoSchema(
        response_codes={
            reverse_func("degree-detail", args=["graduation", "full_code"]): {
                "GET": {200: "[DESCRIBE_RESPONSE_SCHEMA]Degree detail retrieved successfully."}
            }
        },
    )

    serializer_class = DegreePlanSerializer  # TODO: have a DegreeSerializer and DegreeListSerializer
    lookup_field = "full_code"

    # TODO: Actually include requirement data
    def get_queryset(self):
        queryset = DegreePlan.all()
        return queryset

class RuleList(generics.RetrieveAPIView):
    # TODO implement, maybe not needed
    pass