from copy import deepcopy

from dateutil.tz import gettz
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.test import TestCase
from options.models import Option
from rest_framework.test import APIClient

from alert.management.commands.recomputestats import recompute_demand_distribution_estimates
from alert.models import AddDropPeriod, Registration
from courses.models import Instructor, Section
from courses.util import get_add_drop_period, invalidate_current_semester_cache, record_update
from PennCourses.settings.base import TIME_ZONE
from review.models import Review
from tests.courses.util import create_mock_data
from tests.review.test_api import PCRTestMixin, create_review


TEST_CURRENT_SEMESTER = "2021C"
TEST_SEMESTER = "2021A"  # Past semester for reviews

assert TEST_CURRENT_SEMESTER >= "2021C", "TEST_CURRENT_SEMESTER must be at least 2021C"
assert "b" not in TEST_CURRENT_SEMESTER.lower(), "TEST_CURRENT_SEMESTER cannot be a summer semester"
assert TEST_SEMESTER >= "2021A", "TEST_SEMESTER must be at least 2021A"
assert "b" not in TEST_SEMESTER.lower(), "TEST_SEMESTER cannot be a summer semester"


def set_semester():
    post_save.disconnect(
        receiver=invalidate_current_semester_cache,
        sender=Option,
        dispatch_uid="invalidate_current_semester_cache",
    )
    Option(key="SEMESTER", value=TEST_CURRENT_SEMESTER, value_type="TXT").save()
    AddDropPeriod(semester=TEST_CURRENT_SEMESTER).save()
    AddDropPeriod(semester=TEST_SEMESTER).save()


"""
Below are some utility functions that make writing out the response.data dictionaries
a bit easier to do. All of the tests use instructor_quality as the reviewbit to test.
these helper functions cut down on a lot of the repeated characters in the responses.
"""


def ratings_dict(label, rInstructorQuality, rFinalEnrollmentPercentage, rPercentOpen, rNumOpenings):
    return {
        label: {
            "rInstructorQuality": rInstructorQuality,
            "rFinalEnrollmentPercentage": rFinalEnrollmentPercentage,
            "rPercentOpen": rPercentOpen,
            "rNumOpenings": rNumOpenings,
        }
    }


def average(rInstructorQuality, rFinalEnrollmentPercentage, rPercentOpen, rNumOpenings):
    return ratings_dict(
        "average_reviews",
        rInstructorQuality,
        rFinalEnrollmentPercentage,
        rPercentOpen,
        rNumOpenings,
    )


def recent(rInstructorQuality, rFinalEnrollmentPercentage, rPercentOpen, rNumOpenings):
    return ratings_dict(
        "recent_reviews", rInstructorQuality, rFinalEnrollmentPercentage, rPercentOpen, rNumOpenings
    )


def rating(rInstructorQuality, rFinalEnrollmentPercentage, rPercentOpen, rNumOpenings):
    return ratings_dict(
        "ratings", rInstructorQuality, rFinalEnrollmentPercentage, rPercentOpen, rNumOpenings
    )


def set_registrations(section_id, registration_spec_list):
    for reg_spec in registration_spec_list:
        reg = Registration(section_id=section_id)
        reg.save()
        for key, value in reg_spec.items():
            setattr(reg, key, value)
        reg.save()


def get_sec_by_id(sec_id):
    return Section.objects.get(id=sec_id)


def get_start_end_duration(adp):
    start = adp.estimated_start
    end = adp.estimated_end
    duration = end - start
    return start, end, duration


def get_to_date_func(adp):
    start, end, duration = get_start_end_duration(adp)

    def to_date(percent):
        return start + percent * duration

    return to_date


class TwoSemestersOneInstructorTestCase(TestCase, PCRTestMixin):
    @classmethod
    def setUpTestData(cls):
        set_semester()
        cls.instructor_name = "Instructor One"
        create_review(
            "ESE-120-001", TEST_SEMESTER, cls.instructor_name, {"instructor_quality": 3.5}
        )
        create_review("ESE-120-001", "2020C", cls.instructor_name, {"instructor_quality": 2})
        cls.ESE_120_001_TEST_SEMESTER_id = Section.objects.get(
            full_code="ESE-120-001", course__semester=TEST_SEMESTER
        ).id
        cls.ESE_120_001_2020C_id = Section.objects.get(
            full_code="ESE-120-001", course__semester="2020C"
        ).id
        course, section = create_mock_data("ESE-120-001", TEST_CURRENT_SEMESTER)
        section.capacity = 100
        section.save()
        cls.current_sem_adp = get_add_drop_period(TEST_CURRENT_SEMESTER)
        cls.adp = get_add_drop_period(TEST_SEMESTER)
        AddDropPeriod(semester="2020C").save()
        cls.old_adp = get_add_drop_period("2020C")
        cls.average_instructor_quality = (2 + 3.5) / 2
        cls.recent_instructor_quality = 3.5
        cls.old_instructor_quality = 2
        old_status = "O"
        new_status = "C"
        start, end, duration = get_start_end_duration(cls.adp)
        for date in [start + i * duration / 5 for i in range(1, 5)] + [
            start + 0.81 * duration,
            start + 0.82 * duration,
        ]:
            # O[.2]C[.4]O[.6]C[.8]O[.81]C[.82]O
            record_update(
                "ESE-120-001",
                TEST_SEMESTER,
                old_status,
                new_status,
                False,
                dict(),
                created_at=date,
            )
            old_status, new_status = new_status, old_status
        cls.recent_percent_open_plot = [
            (0, 1),
            (0.2, 0.0),
            (0.4, 1),
            (0.6, 0.0),
            (0.8, 1),
            (0.81, 0),
            (0.82, 1),
            (1, 1),
        ]
        cls.recent_percent_open = 3 / 5 - 0.01
        old_status = "C"
        new_status = "O"
        start, end, duration = get_start_end_duration(cls.old_adp)
        for date in [start + i * duration / 4 for i in range(1, 4)]:
            # C[.25]O[.5]C[.75]O
            record_update(
                "ESE-120-001", "2020C", old_status, new_status, False, dict(), created_at=date,
            )
            old_status, new_status = new_status, old_status
        cls.average_percent_open_plot = [
            (0, 0.5),
            (0.2, 0),
            (0.25, 0.5),
            (0.4, 1),
            (0.5, 0.5),
            (0.6, 0.0),
            (0.75, 0.5),
            (0.8, 1),
            (0.81, 0.5),
            (0.82, 1),
            (1, 1),
        ]
        cls.average_percent_open = (1 / 2 + 3 / 5 - 0.01) / 2
        cls.old_percent_open = 1 / 2
        to_date = get_to_date_func(cls.adp)
        # O[.2]C[.4]O[.6]C[.8]O[.81]C[.82]O
        registration_list_TS = [
            {"created_at": to_date(0.1), "cancelled_at": to_date(0.19), "cancelled": True},
            {
                "created_at": to_date(0.15),
                "notification_sent_at": to_date(0.4),
                "notification_sent": True,
            },
            {
                "created_at": to_date(0.45),
                "notification_sent_at": to_date(0.6),
                "notification_sent": True,
            },
            {"created_at": to_date(0.61), "deleted_at": to_date(0.79), "deleted": True},
        ]
        set_registrations(cls.ESE_120_001_TEST_SEMESTER_id, registration_list_TS)
        cls.recent_pca_demand_plot = [
            (0, 0.0),
            (0.2, 0.5),
            (0.4, 0.0),
            (0.6, 0.5),
            (0.8, 0.0),
            (0.81, 0.5),
            (0.82, 0.0),
        ]
        to_date = get_to_date_func(cls.old_adp)
        # C[.25]O[.5]C[.75]O
        registration_list_2020C = [
            {
                "created_at": to_date(0.1001),
                "notification_sent_at": to_date(0.25),
                "notification_sent": True,
            },
            {
                "created_at": to_date(0.51),
                "cancelled_at": to_date(0.52),
                "deleted_at": to_date(0.53),
                "deleted": True,
            },
            {"created_at": to_date(0.76), "deleted_at": to_date(0.77), "deleted": True},
        ]
        set_registrations(cls.ESE_120_001_2020C_id, registration_list_2020C)
        cls.average_pca_demand_plot = [
            (0, 0.0),
            (0.1001, 0.25),
            (0.2, 0.5),
            (0.25, 0.25),
            (0.4, 0.0),
            (0.5, 0.25),
            (0.6, 0.5),
            (0.75, 0.25),
            (0.8, 0.0),
            (0.81, 0.25),
            (0.82, 0.0),
        ]

        cls.recent_num_updates = 3
        cls.average_num_updates = (3 + 2) / 2
        cls.old_num_updates = 2
        recent_review = Review.objects.get(section_id=cls.ESE_120_001_TEST_SEMESTER_id)
        recent_review.enrollment = 80
        recent_review.save()
        test_sem_class = get_sec_by_id(cls.ESE_120_001_TEST_SEMESTER_id)
        test_sem_class.capacity = 100
        test_sem_class.save()
        average_review = Review.objects.get(section_id=cls.ESE_120_001_2020C_id)
        average_review.enrollment = 99
        average_review.save()
        old_sem_class = get_sec_by_id(cls.ESE_120_001_2020C_id)
        old_sem_class.capacity = 100
        old_sem_class.save()
        cls.recent_enrollment_pct = 80 / 100
        cls.average_enrollment_pct = (80 / 100 + 99 / 100) / 2
        cls.old_enrollment_pct = 99 / 100

        recompute_demand_distribution_estimates(
            semesters=TEST_CURRENT_SEMESTER + "," + TEST_SEMESTER + "," + "2020C"
        )

        local_tz = gettz(TIME_ZONE)
        cls.current_add_drop_period = {
            "start": cls.current_sem_adp.estimated_start.astimezone(tz=local_tz),
            "end": cls.current_sem_adp.estimated_end.astimezone(tz=local_tz),
        }
        cls.recent_pca_demand_plot_since_semester = TEST_SEMESTER
        cls.average_pca_demand_plot_since_semester = "2020C"
        cls.recent_pca_demand_plot_num_semesters = 1
        cls.average_pca_demand_plot_num_semesters = 2
        cls.recent_percent_open_plot_since_semester = TEST_SEMESTER
        cls.average_percent_open_plot_since_semester = "2020C"
        cls.recent_percent_open_plot_num_semesters = 1
        cls.average_percent_open_plot_num_semesters = 2

    def setUp(self):
        self.client = APIClient()
        self.client.force_login(User.objects.create_user(username="test"))

    def test_course(self):
        subdict = {
            **average(
                self.average_instructor_quality,
                self.average_enrollment_pct,
                self.average_percent_open,
                self.average_num_updates,
            ),
            **recent(
                self.recent_instructor_quality,
                self.recent_enrollment_pct,
                self.recent_percent_open,
                self.recent_num_updates,
            ),
        }
        course_subdict = deepcopy(subdict)
        for field in [
            "pca_demand_plot",
            "percent_open_plot",
            "pca_demand_plot_since_semester",
            "pca_demand_plot_num_semesters",
            "percent_open_plot_since_semester",
            "percent_open_plot_num_semesters",
        ]:
            course_subdict["average_reviews"][field] = getattr(self, "average_" + field)
        for field in [
            "pca_demand_plot",
            "percent_open_plot",
            "pca_demand_plot_since_semester",
            "pca_demand_plot_num_semesters",
            "percent_open_plot_since_semester",
            "percent_open_plot_num_semesters",
        ]:
            course_subdict["recent_reviews"][field] = getattr(self, "recent_" + field)
        self.assertRequestContainsAppx(
            "course-reviews",
            "ESE-120",
            {**course_subdict, "instructors": {Instructor.objects.get().pk: subdict}},
        )

    def test_instructor(self):
        subdict = {
            **average(
                self.average_instructor_quality,
                self.average_enrollment_pct,
                self.average_percent_open,
                self.average_num_updates,
            ),
            **recent(
                self.recent_instructor_quality,
                self.recent_enrollment_pct,
                self.recent_percent_open,
                self.recent_num_updates,
            ),
        }
        self.assertRequestContainsAppx(
            "instructor-reviews",
            Instructor.objects.get().pk,
            {**subdict, "courses": {"ESE-120": subdict}},
        )

    def test_department(self):
        subdict = {
            **average(
                self.average_instructor_quality,
                self.average_enrollment_pct,
                self.average_percent_open,
                self.average_num_updates,
            ),
            **recent(
                self.recent_instructor_quality,
                self.recent_enrollment_pct,
                self.recent_percent_open,
                self.recent_num_updates,
            ),
        }
        self.assertRequestContainsAppx(
            "department-reviews", "ESE", {"courses": {"ESE-120": subdict}}
        )

    def test_history(self):
        self.assertRequestContainsAppx(
            "course-history",
            ["ESE-120", Instructor.objects.get().pk],
            {
                "sections": [
                    rating(
                        self.recent_instructor_quality,
                        self.recent_enrollment_pct,
                        self.recent_percent_open,
                        self.recent_num_updates,
                    ),
                    rating(
                        self.old_instructor_quality,
                        self.old_enrollment_pct,
                        self.old_percent_open,
                        self.old_num_updates,
                    ),
                ]
            },
        )

    def test_autocomplete(self):
        self.assertRequestContainsAppx(
            "review-autocomplete",
            [],
            {
                "instructors": [
                    {
                        "title": self.instructor_name,
                        "desc": "ESE",
                        "url": f"/instructor/{Instructor.objects.get().pk}",
                    }
                ],
                "courses": [{"title": "ESE-120", "desc": [""], "url": "/course/ESE-120",}],
                "departments": [{"title": "ESE", "desc": "", "url": "/department/ESE"}],
            },
        )


class OneReviewTestCase(TestCase, PCRTestMixin):
    @classmethod
    def setUpTestData(cls):
        set_semester()
        cls.instructor_name = "Instructor One"
        create_review(
            "ESE-120-001", TEST_SEMESTER, cls.instructor_name, {"instructor_quality": 3.5}
        )
        cls.ESE_120_001_id = Section.objects.get(full_code="ESE-120-001").id
        cls.instructor_quality = 3.5
        cls.current_sem_adp = get_add_drop_period(TEST_CURRENT_SEMESTER)
        cls.adp = get_add_drop_period(TEST_SEMESTER)
        start = cls.adp.estimated_start
        end = cls.adp.estimated_end
        duration = end - start
        old_status = "O"
        new_status = "C"
        cls.percent_open_plot = [(0, 1)]
        for date in [start + i * duration / 7 for i in range(1, 7)]:
            # O[1/7]C[2/7]O[3/7]C[4/7]O[5/7]C[6/7]O
            percent_thru = cls.adp.get_percent_through_add_drop(date)
            record_update(
                "ESE-120-001",
                TEST_SEMESTER,
                old_status,
                new_status,
                False,
                dict(),
                created_at=date,
            )
            cls.percent_open_plot.append((percent_thru, int(new_status == "O")))
            old_status, new_status = new_status, old_status
        cls.percent_open_plot.append((1, 1))
        to_date = get_to_date_func(cls.adp)
        set_registrations(
            cls.ESE_120_001_id,
            [
                {"created_at": to_date(0.25), "cancelled_at": to_date(0.26), "cancelled": True},
                {
                    "created_at": to_date(0.5),
                    "notification_sent_at": to_date(4 / 7),
                    "notification_sent": True,
                },
                {"created_at": to_date(0.75), "deleted_at": to_date(5.9 / 7), "deleted": True},
            ],
        )

        cls.num_updates = 3
        review = Review.objects.get()
        review.enrollment = 80
        review.save()
        sec = get_sec_by_id(cls.ESE_120_001_id)
        sec.capacity = 100
        sec.save()

        recompute_demand_distribution_estimates(semesters=TEST_SEMESTER)

        cls.percent_open = (duration * 4 / 7).total_seconds() / duration.total_seconds()
        cls.pca_demand_plot = [
            (0, 0),
            (0.25, 0.5),
            (2 / 7, 0),
            (3 / 7, 0.5),
            (4 / 7, 0),
            (5 / 7, 0.5),
            (6 / 7, 0),
            (1, 0),
        ]

        local_tz = gettz(TIME_ZONE)
        cls.current_add_drop_period = {
            "start": cls.current_sem_adp.estimated_start.astimezone(tz=local_tz),
            "end": cls.current_sem_adp.estimated_end.astimezone(tz=local_tz),
        }
        cls.pca_demand_plot_since_semester = TEST_SEMESTER
        cls.pca_demand_plot_num_semesters = 1
        cls.percent_open_plot_since_semester = TEST_SEMESTER
        cls.percent_open_plot_num_semesters = 1
        cls.enrollment_pct = 80 / 100

    def setUp(self):
        self.client = APIClient()
        self.client.force_login(User.objects.create_user(username="test"))

    def test_course(self):
        subdict = {
            **average(
                self.instructor_quality, self.enrollment_pct, self.percent_open, self.num_updates
            ),
            **recent(
                self.instructor_quality, self.enrollment_pct, self.percent_open, self.num_updates
            ),
        }
        course_subdict = deepcopy(subdict)
        for field in [
            "pca_demand_plot",
            "percent_open_plot",
            "pca_demand_plot_since_semester",
            "pca_demand_plot_num_semesters",
            "percent_open_plot_since_semester",
            "percent_open_plot_num_semesters",
        ]:
            course_subdict["average_reviews"][field] = getattr(self, field)
        for field in [
            "pca_demand_plot",
            "percent_open_plot",
            "pca_demand_plot_since_semester",
            "pca_demand_plot_num_semesters",
            "percent_open_plot_since_semester",
            "percent_open_plot_num_semesters",
        ]:
            course_subdict["recent_reviews"][field] = getattr(self, field)
        self.assertRequestContainsAppx(
            "course-reviews",
            "ESE-120",
            {**course_subdict, "instructors": {Instructor.objects.get().pk: subdict}},
        )

    def test_instructor(self):
        subdict = {
            **average(
                self.instructor_quality, self.enrollment_pct, self.percent_open, self.num_updates
            ),
            **recent(
                self.instructor_quality, self.enrollment_pct, self.percent_open, self.num_updates
            ),
        }
        self.assertRequestContainsAppx(
            "instructor-reviews",
            Instructor.objects.get().pk,
            {**subdict, "courses": {"ESE-120": subdict}},
        )

    def test_department(self):
        subdict = {
            **average(
                self.instructor_quality, self.enrollment_pct, self.percent_open, self.num_updates
            ),
            **recent(
                self.instructor_quality, self.enrollment_pct, self.percent_open, self.num_updates
            ),
        }
        self.assertRequestContainsAppx(
            "department-reviews", "ESE", {"courses": {"ESE-120": subdict}}
        )

    def test_history(self):
        self.assertRequestContainsAppx(
            "course-history",
            ["ESE-120", Instructor.objects.get().pk],
            {
                "sections": [
                    rating(
                        self.instructor_quality,
                        self.enrollment_pct,
                        self.percent_open,
                        self.num_updates,
                    )
                ]
            },
        )

    def test_autocomplete(self):
        self.assertRequestContainsAppx(
            "review-autocomplete",
            [],
            {
                "instructors": [
                    {
                        "title": self.instructor_name,
                        "desc": "ESE",
                        "url": f"/instructor/{Instructor.objects.get().pk}",
                    }
                ],
                "courses": [{"title": "ESE-120", "desc": [""], "url": "/course/ESE-120",}],
                "departments": [{"title": "ESE", "desc": "", "url": "/department/ESE"}],
            },
        )


class TwoInstructorsOneSectionTestCase(TestCase, PCRTestMixin):
    @classmethod
    def setUpTestData(cls):
        set_semester()
        cls.instructor_1_name = "Instructor One"
        cls.instructor_2_name = "Instructor Two"
        create_review(
            "ESE-120-001", TEST_SEMESTER, cls.instructor_1_name, {"instructor_quality": 3.5}
        )
        create_review(
            "ESE-120-001", TEST_SEMESTER, cls.instructor_2_name, {"instructor_quality": 3.5}
        )
        cls.ESE_120_001_id = Section.objects.get(full_code="ESE-120-001").id
        cls.instructor_quality = 3.5
        cls.current_sem_adp = get_add_drop_period(TEST_CURRENT_SEMESTER)
        cls.adp = get_add_drop_period(TEST_SEMESTER)
        start = cls.adp.estimated_start
        end = cls.adp.estimated_end
        duration = end - start
        old_status = "O"
        new_status = "C"
        cls.percent_open_plot = [(0, 1)]
        for date in [start + i * duration / 7 for i in range(1, 7)]:
            # O[1/7]C[2/7]O[3/7]C[4/7]O[5/7]C[6/7]O
            percent_thru = cls.adp.get_percent_through_add_drop(date)
            record_update(
                "ESE-120-001",
                TEST_SEMESTER,
                old_status,
                new_status,
                False,
                dict(),
                created_at=date,
            )
            cls.percent_open_plot.append((percent_thru, int(new_status == "O")))
            old_status, new_status = new_status, old_status
        cls.percent_open_plot.append((1, 1))
        to_date = get_to_date_func(cls.adp)
        set_registrations(
            cls.ESE_120_001_id,
            [
                {"created_at": to_date(0.25), "cancelled_at": to_date(0.26), "cancelled": True},
                {
                    "created_at": to_date(0.5),
                    "notification_sent_at": to_date(4 / 7),
                    "notification_sent": True,
                },
                {"created_at": to_date(0.75), "deleted_at": to_date(5.9 / 7), "deleted": True},
            ],
        )

        cls.num_updates = 3
        for review in Review.objects.all():
            review.enrollment = 80
            review.save()
        sec = get_sec_by_id(cls.ESE_120_001_id)
        sec.capacity = 100
        sec.save()

        recompute_demand_distribution_estimates(semesters=TEST_SEMESTER)

        cls.percent_open = (duration * 4 / 7).total_seconds() / duration.total_seconds()
        cls.pca_demand_plot = [
            (0, 0),
            (0.25, 0.5),
            (2 / 7, 0),
            (3 / 7, 0.5),
            (4 / 7, 0),
            (5 / 7, 0.5),
            (6 / 7, 0),
            (1, 0),
        ]

        local_tz = gettz(TIME_ZONE)
        cls.current_add_drop_period = {
            "start": cls.current_sem_adp.estimated_start.astimezone(tz=local_tz),
            "end": cls.current_sem_adp.estimated_end.astimezone(tz=local_tz),
        }
        cls.pca_demand_plot_since_semester = TEST_SEMESTER
        cls.pca_demand_plot_num_semesters = 1
        cls.percent_open_plot_since_semester = TEST_SEMESTER
        cls.percent_open_plot_num_semesters = 1
        cls.enrollment_pct = 80 / 100

    def setUp(self):
        self.client = APIClient()
        self.client.force_login(User.objects.create_user(username="test"))

    def test_course(self):
        subdict = {
            **average(
                self.instructor_quality, self.enrollment_pct, self.percent_open, self.num_updates
            ),
            **recent(
                self.instructor_quality, self.enrollment_pct, self.percent_open, self.num_updates
            ),
        }
        course_subdict = deepcopy(subdict)
        for field in [
            "pca_demand_plot",
            "percent_open_plot",
            "pca_demand_plot_since_semester",
            "pca_demand_plot_num_semesters",
            "percent_open_plot_since_semester",
            "percent_open_plot_num_semesters",
        ]:
            course_subdict["average_reviews"][field] = getattr(self, field)
        for field in [
            "pca_demand_plot",
            "percent_open_plot",
            "pca_demand_plot_since_semester",
            "pca_demand_plot_num_semesters",
            "percent_open_plot_since_semester",
            "percent_open_plot_num_semesters",
        ]:
            course_subdict["recent_reviews"][field] = getattr(self, field)
        self.assertRequestContainsAppx(
            "course-reviews",
            "ESE-120",
            {
                **course_subdict,
                "instructors": {
                    Instructor.objects.get(name=self.instructor_1_name).pk: subdict,
                    Instructor.objects.get(name=self.instructor_2_name).pk: subdict,
                },
            },
        )

    def test_instructor(self):
        subdict = {
            **average(
                self.instructor_quality, self.enrollment_pct, self.percent_open, self.num_updates
            ),
            **recent(
                self.instructor_quality, self.enrollment_pct, self.percent_open, self.num_updates
            ),
        }
        self.assertRequestContainsAppx(
            "instructor-reviews",
            Instructor.objects.get(name=self.instructor_1_name).pk,
            {**subdict, "courses": {"ESE-120": subdict}},
        )
        self.assertRequestContainsAppx(
            "instructor-reviews",
            Instructor.objects.get(name=self.instructor_2_name).pk,
            {**subdict, "courses": {"ESE-120": subdict}},
        )

    def test_department(self):
        subdict = {
            **average(
                self.instructor_quality, self.enrollment_pct, self.percent_open, self.num_updates
            ),
            **recent(
                self.instructor_quality, self.enrollment_pct, self.percent_open, self.num_updates
            ),
        }
        self.assertRequestContainsAppx(
            "department-reviews", "ESE", {"courses": {"ESE-120": subdict}}
        )

    def test_history(self):
        self.assertRequestContainsAppx(
            "course-history",
            ["ESE-120", Instructor.objects.get(name=self.instructor_1_name).pk],
            {
                "sections": [
                    rating(
                        self.instructor_quality,
                        self.enrollment_pct,
                        self.percent_open,
                        self.num_updates,
                    )
                ]
            },
        )
        self.assertRequestContainsAppx(
            "course-history",
            ["ESE-120", Instructor.objects.get(name=self.instructor_2_name).pk],
            {
                "sections": [
                    rating(
                        self.instructor_quality,
                        self.enrollment_pct,
                        self.percent_open,
                        self.num_updates,
                    )
                ]
            },
        )

    def test_autocomplete(self):
        self.assertRequestContainsAppx(
            "review-autocomplete",
            [],
            {
                "instructors": [
                    {
                        "title": self.instructor_1_name,
                        "desc": "ESE",
                        "url": (
                            "/instructor/"
                            + str(Instructor.objects.get(name=self.instructor_1_name).pk)
                        ),
                    },
                    {
                        "title": self.instructor_2_name,
                        "desc": "ESE",
                        "url": (
                            "/instructor/"
                            + str(Instructor.objects.get(name=self.instructor_2_name).pk)
                        ),
                    },
                ],
                "courses": [{"title": "ESE-120", "desc": [""], "url": "/course/ESE-120",}],
                "departments": [{"title": "ESE", "desc": "", "url": "/department/ESE"}],
            },
        )


# TODO: More tests to add:
# 2 sections of same class
# 2 different classes in same semester
# classes that don't qualify
# classes with no registrations
# current / future classes?