from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.test import TestCase
from options.models import (  # TODO: can't resolve this import for some reason (also appears in other PCP Schedule tests)
    Option,
)
from rest_framework.test import APIClient

from alert.management.commands.recomputestats import recompute_precomputed_fields
from alert.models import AddDropPeriod
from courses.models import Friendship
from courses.util import invalidate_current_semester_cache
from plan.models import PrimarySchedule, Schedule
from tests.alert.test_alert import TEST_SEMESTER, set_semester
from tests.courses.util import create_mock_data, create_mock_data_with_reviews


primary_schedule_url = "/api/plan/primary-schedules/"
TEST_SEMESTER = "2019A"


def set_semester():
    post_save.disconnect(
        receiver=invalidate_current_semester_cache,
        sender=Option,
        dispatch_uid="invalidate_current_semester_cache",
    )
    Option(key="SEMESTER", value=TEST_SEMESTER, value_type="TXT").save()
    AddDropPeriod(semester=TEST_SEMESTER).save()


class PrimaryScheduleTest(TestCase):
    def setUp(self):
        self.u1 = User.objects.create_user(
            username="jacobily", email="jacob@example.com", password="top_secret"
        )
        set_semester()
        _, self.cis120, self.cis120_reviews = create_mock_data_with_reviews(
            "CIS-120-001", TEST_SEMESTER, 2
        )
        _, self.cis121, self.cis121_reviews = create_mock_data_with_reviews(
            "CIS-121-001", TEST_SEMESTER, 2
        )
        self.s = Schedule(
            person=self.u1,
            semester=TEST_SEMESTER,
            name="My Test Schedule",
        )
        self.s.save()
        self.s.sections.set([self.cis120])

        self.s2 = Schedule(
            person=self.u1,
            semester=TEST_SEMESTER,
            name="My Test Schedule 2",
        )
        self.s2.save()
        self.s2.sections.set([self.cis121])

        self.client = APIClient()
        self.client.login(username="jacobily", password="top_secret")

        # TODO: write test cases for the following cases
        """
            - remove primary schedule (and check no other primary scheudles in the models)
                - can't do this since we don't have a remove primary schedule feature. I think 
                it's fine that we don't have one for now.
        """

    def test_put_primary_schedule(self):
        response = self.client.put(primary_schedule_url, {"schedule_id": self.s.id})
        self.assertEqual(response.status_code, 200)
        # print(response.json())
        # print(PrimarySchedule.objects.all().values())
        # self.assertEqual(response.json()["id"], self.s.id)
        # self.assertEqual(response.json()["name"], self.s.name)
        # self.assertEqual(response.json()["sections"][0]["id"], self.cis120.id)
        # self.assertEqual(response.json()["sections"][0]["course"]["id"], self.cis120.course.id)

    def test_replace_primary_schedule(self):
        response = self.client.put(primary_schedule_url, {"schedule_id": 123})  # invalid ID
        self.assertEqual(response.status_code, 400)

        response = self.client.put(primary_schedule_url, {"schedule_id": self.s.id})
        self.assertEqual(response.status_code, 200)
        # print(PrimarySchedule.objects.all().values())
        # self.assertEqual(response.data["id"], self.s.id)

        response = self.client.put(primary_schedule_url, {"schedule_id": self.s2.id})
        self.assertEqual(response.status_code, 200)
        # print(PrimarySchedule.objects.all().values())
        # self.assertEqual(response.data["id"], self.s2.id)

    def test_primary_schedule_friends(self):
        response = self.client.put(primary_schedule_url, {"schedule_id": self.s.id})

        u2 = User.objects.create_user(
            username="jacob2", email="jacob2@gmail.com", password="top_secret"
        )
        u3 = User.objects.create_user(
            username="jacob3", email="jacob3@gmail.com", password="top_secret"
        )
        self.client2 = APIClient()
        self.client2.login(username="jacob2", password="top_secret")
        self.client3 = APIClient()
        self.client3.login(username="jacob3", password="top_secret")

        Friendship.objects.create(sender=self.u1, recipient=u2, status=Friendship.Status.ACCEPTED)
        u2_s = Schedule(
            person=u2,
            semester=TEST_SEMESTER,
            name="U2 Test Schedule",
        )
        u2_s.save()
        u2_s.sections.set([self.cis120])
        response = self.client2.put(primary_schedule_url, {"schedule_id": u2_s.id})
        # self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.data["id"], u2_s.id)

        response = self.client.get(primary_schedule_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        # print("1", response.json())
        # self.assertEqual(response.data[0]["id"], self.s.id)
        # self.assertEqual(response.data[1]["id"], u2_s.id)

        Friendship.objects.create(sender=self.u1, recipient=u3, status=Friendship.Status.ACCEPTED)
        u3_s = Schedule(
            person=u3,
            semester=TEST_SEMESTER,
            name="U3 Test Schedule",
        )
        u3_s.save()
        u3_s.sections.set([self.cis120])

        # shouldn't change bc no primary scheudle for u3 yet
        response = self.client.get(primary_schedule_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        # print("2", response.json())

        # add a primary schedule for u3
        response = self.client3.put(primary_schedule_url, {"schedule_id": u3_s.id})
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.data["id"], u3_s.id)

        # should have all 3 now
        response = self.client.get(primary_schedule_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)
        # print("3", response.json())

        # remove u2 as a friend
        friendshipu2 = Friendship.objects.get(sender=self.u1, recipient=u2)
        friendshipu2.delete()

        # only have u1 and u3 now
        response = self.client.get(primary_schedule_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        # print("4", response.json())
        # self.assertEqual(response.data[0]["id"], self.s.id)
        # self.assertEqual(response.data[1]["id"], u3_s.id)
