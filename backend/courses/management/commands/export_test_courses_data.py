import csv
import os
from textwrap import dedent

from django.core.management.base import BaseCommand
from tqdm import tqdm

from courses.management.commands.export_anon_registrations import get_semesters
from courses.models import Course, Department, Instructor, Section
from PennCourses.settings.base import S3_resource
from review.models import Review, ReviewBit


test_data_fields = {
    "departments": ["id", "code", "name"],
    "courses_null_primary_listing": [
        "id",
        "semester",
        "department_id",
        "code",
        "title",
        "description",
        "full_code",
        "prerequisites",
    ],
    "courses_non_null_primary_listing": [
        "id",
        "semester",
        "department_id",
        "code",
        "title",
        "description",
        "full_code",
        "prerequisites",
        "primary_listing_id",
    ],
    "sections": [
        "id",
        "code",
        "course_id",
        "full_code",
        "status",
        "capacity",
        "activity",
        "meeting_times",
        "credits",
    ],
    "instructors": ["id", "name"],
    "sections_instructors_m2mfield": ["sections", "instructors", "instructors"],
    "sections_associated_sections_m2mfield": ["sections", "associated_sections", "sections"],
    "reviews": [
        "id",
        "section_id",
        "instructor_id",
        "enrollment",
        "responses",
        "form_type",
        "comments",
    ],
    "review_bits": [
        "id",
        "review_id",
        "field",
        "average",
        "median",
        "stddev",
        "rating0",
        "rating1",
        "rating2",
        "rating3",
        "rating4",
    ],
}  # define fields to export from each data type

related_id_fields = {
    "courses_null_primary_listing": {"department_id": "departments",},
    "courses_non_null_primary_listing": {
        "department_id": "departments",
        "primary_listing_id": "courses_null_primary_listing",
    },
    "reviews": {"section_id": "sections", "instructor_id": "instructors",},
    "review_bits": {"review_id": "reviews",},
}  # specify fields which represent foreign key relationships (id on other model),
# and the model of the foreign key


class Command(BaseCommand):
    help = "Export test courses, sections, instructors, and reviews data from the given semesters."

    def add_arguments(self, parser):
        parser.add_argument(
            "--courses_query",
            default="",
            type=str,
            help=(
                "A prefix of the course full_code (e.g. CIS-120) to filter exported courses by. "
                "Omit this argument to export all courses from the given semesters."
            ),
        )
        parser.add_argument(
            "--path",
            type=str,
            help="The path (local or in S3) you want to export test data to (must be a .csv file).",
        )
        parser.add_argument(
            "--upload_to_s3",
            default=False,
            action="store_true",
            help=(
                "Enable this argument to upload the output of this script to the penn.courses "
                "S3 bucket, at the paths specified by the above path arguments. "
            ),
        )
        parser.add_argument(
            "--semesters",
            type=str,
            help=dedent(
                """
                The semesters argument should be a comma-separated list of semesters
            corresponding to the semesters from which you want to export PCA registrations,
            i.e. "2019C,2020A,2020C" for fall 2019, spring 2020, and fall 2020.
            If you pass "all" to this argument, this script will export all status updates.
                """
            ),
            default="",
        )

    def handle(self, *args, **kwargs):
        upload_to_s3 = kwargs["upload_to_s3"]
        semesters = get_semesters(kwargs["semesters"], verbose=True)
        if len(semesters) == 0:
            raise ValueError("No semesters provided for status update export.")

        path = kwargs["path"]
        assert path.endswith(".csv") or path == os.devnull
        script_print_path = ("s3://penn.courses/" if upload_to_s3 else "") + path
        print(f"Exporting test data from semesters {semesters} to {script_print_path}...")

        querysets = dict()  # will map datatype to the queryset generated for that datatype
        fields = test_data_fields
        data_types = fields.keys()

        rows = 0
        output_file_path = "/app/export_test_data_output.csv" if upload_to_s3 else path
        with open(output_file_path, "w") as output_file:
            csv_writer = csv.writer(
                output_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )

            for data_type in data_types:
                print(f"Processing {data_type}...")

                if data_type.endswith("_m2mfield"):
                    for object in tqdm(querysets[fields[data_type][0]]):
                        for related_object in getattr(object, fields[data_type][1]).all():
                            rows += 1
                            csv_writer.writerow(
                                [data_type]
                                + [
                                    fields[data_type][0],
                                    object.id,
                                    fields[data_type][1],
                                    str(related_object.id),
                                    fields[data_type][2],
                                ]
                            )
                    continue

                if data_type == "departments":
                    queryset = Department.objects.all()
                elif data_type == "courses_null_primary_listing":
                    queryset = Course.objects.filter(
                        semester__in=semesters,
                        full_code__startswith=kwargs["courses_query"],
                        primary_listing__isnull=True,
                    )
                    querysets["courses_null_primary_listing"] = queryset
                elif data_type == "courses_non_null_primary_listing":
                    queryset = Course.objects.filter(
                        semester__in=semesters,
                        full_code__startswith=kwargs["courses_query"],
                        primary_listing__isnull=False,
                    )
                    querysets["courses_non_null_primary_listing"] = queryset
                    querysets["courses"] = list(querysets["courses_null_primary_listing"]) + list(
                        querysets["courses_non_null_primary_listing"]
                    )
                elif data_type == "sections":
                    queryset = Section.objects.filter(
                        course__in=querysets["courses"]
                    ).prefetch_related("associated_sections", "instructors")
                    querysets["sections"] = queryset
                elif data_type == "instructors":
                    queryset = Instructor.objects.all()
                    querysets["instructors"] = queryset
                elif data_type == "reviews":
                    queryset = Review.objects.filter(section__in=querysets["sections"])
                    querysets["reviews"] = queryset
                elif data_type == "review_bits":
                    queryset = ReviewBit.objects.filter(review__in=querysets["reviews"])
                    querysets["review_bits"] = queryset

                for object in tqdm(queryset):
                    rows += 1
                    csv_writer.writerow(
                        [data_type] + [str(getattr(object, field)) for field in fields[data_type]]
                    )

        if upload_to_s3:
            S3_resource.meta.client.upload_file(
                "/app/export_test_data_output.csv", "penn.courses", path
            )
            os.remove("/app/export_test_data_output.csv")

        print(f"Exported {rows} of test data from semesters {semesters} to {script_print_path}.")
