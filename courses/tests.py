from django.test import TestCase, override_settings
from django.test import RequestFactory

from rest_framework.test import APIClient

from options.models import *
from .models import *
from .util import *
from .views import *

TEST_SEMESTER = '2019A'


def set_semester():
    Option(key="SEMESTER", value=TEST_SEMESTER, value_type='TXT').save()


class SepCourseCodeTest(TestCase):
    def test_four_letter_dept_code(self):
        self.assertEqual(('ANTH', '361', '401'), separate_course_code('ANTH361401'))

    def test_three_letter_dept_code(self):
        self.assertEqual(('CIS', '120', '001'), separate_course_code('CIS 120001'))

    def test_two_letter_dept_code(self):
        self.assertEqual(('WH', '110', '001'), separate_course_code('WH  110001'))

    def test_four_letter_with_dashes(self):
        self.assertEqual(('PSCI', '110', '001'), separate_course_code('PSCI-110-001'))

    def test_three_letter_with_dashes(self):
        self.assertEqual(('CIS', '110', '001'), separate_course_code('CIS -110-001'))

    def test_two_letter_with_dashes(self):
        self.assertEqual(('WH', '110', '001'), separate_course_code('WH  -110-001'))

    def test_invalid_course(self):
        try:
            separate_course_code('BLAH BLAH BLAH')
            self.fail('Should throw exception')
        except ValueError:
            pass


class GetCourseSectionTest(TestCase):
    def setUp(self):
        self.c = Course(department=Department.objects.get_or_create(code='PSCI')[0],
                        code='131',
                        semester=TEST_SEMESTER,
                        title='American Foreign Policy')
        self.c.save()
        self.s = Section(code='001', course=self.c)
        self.s.save()

    def assertCourseSame(self, s):
        course, section = get_course_and_section(s, TEST_SEMESTER)
        self.assertEqual(course, self.c, s)
        self.assertEqual(section, self.s, s)

    def test_get_course_exists_nodash(self):
        test_valid = [
            'PSCI131001',
            'PSCI 131 001',
            'PSCI 131001',
            'PSCI-131-001',
            'psci131001',
            'psci-131-001',
            'psci 131 001',
        ]
        for test in test_valid:
            self.assertCourseSame(test)

    def test_create_course(self):
        course, section = get_course_and_section('CIS 120 001', TEST_SEMESTER)
        self.assertEqual(Course.objects.count(), 2)
        self.assertEqual(course.department.code, 'CIS')
        self.assertEqual(course.code, '120')
        self.assertEqual(section.code, '001')


class CourseStatusUpdateTestCase(TestCase):
    def setUp(self):
        self.course, self.section = get_course_and_section('CIS-120-001', TEST_SEMESTER)

    def test_update_status(self):
        self.section.status = 'C'
        self.section.save()
        up = record_update(self.section.normalized,
                           TEST_SEMESTER,
                           'C',
                           'O',
                           True,
                           'JSON')
        up.save()
        update_course_from_record(up)
        _, section = get_course_and_section(self.section.normalized, TEST_SEMESTER)
        self.assertEqual('O', section.status)


class CrosslistingTestCase(TestCase):
    def setUp(self):
        self.anch, _ = get_course_and_section('ANCH-027-401', TEST_SEMESTER)
        self.clst, _ = get_course_and_section('CLST-027-401', TEST_SEMESTER)

    def test_add_primary_listing(self):
        set_crosslistings(self.anch, '')
        self.anch.save()
        self.assertEqual(self.anch, self.anch.primary_listing)

    def test_add_existing_class(self):
        set_crosslistings(self.clst, 'ANCH-027-401')
        self.clst.save()
        clst, _ = get_course_and_section('CLST-027-401', TEST_SEMESTER)
        anch, _ = get_course_and_section('ANCH-027-401', TEST_SEMESTER)
        self.assertEqual(self.anch, clst.primary_listing)
        self.assertEqual(2, Course.objects.count())

    def test_crosslisting_set(self):
        set_crosslistings(self.clst, 'ANCH-027-401')
        set_crosslistings(self.anch, '')
        self.clst.save()
        self.anch.save()
        self.assertTrue(self.anch in self.clst.crosslistings.all())
        self.assertTrue(self.clst in self.anch.crosslistings.all())

    def test_crosslisting_newsection(self):
        set_crosslistings(self.anch, 'HIST-027-401')
        self.anch.save()
        self.assertEqual(3, Course.objects.count())


class RequirementTestCase(TestCase):
    def setUp(self):
        get_course('CIS', '120', '2012A')  # dummy course to make sure we're filtering by semester
        self.course = get_course('CIS', '120', TEST_SEMESTER)
        self.course2 = get_course('CIS', '125', TEST_SEMESTER)
        self.department = Department.objects.get(code='CIS')

        self.req1 = Requirement(semester=TEST_SEMESTER,
                                school='SAS',
                                code='TEST1',
                                name='Test 1')

        self.req2 = Requirement(semester=TEST_SEMESTER,
                                school='SAS',
                                code='TEST2',
                                name='Test 2')

        self.req1.save()
        self.req2.save()

        self.req1.departments.add(self.department)
        self.req2.courses.add(self.course)
        self.req2.courses.add(self.course2)
        self.req1.overrides.add(self.course2)

    def assertCoursesEqual(self, expected, actual):
        def get_codes(x): sorted([f'{c.department.code}-{c.code}' for c in x])
        self.assertEqual(get_codes(expected), get_codes(actual))

    def test_requirements_nooverride(self):
        reqs = self.course.requirements
        self.assertTrue(2, len(reqs))

    def test_requirements_override(self):
        reqs = self.course2.requirements
        self.assertEqual(1, len(reqs))
        self.assertEqual(self.req2, reqs[0])

    def test_satisfying_courses(self):
        # make it so req1 has one department-level requirement, one course-level one, and one override.
        c1 = get_course('MEAM', '101', TEST_SEMESTER)
        self.req1.courses.add(c1)
        courses = self.req1.satisfying_courses.all()
        self.assertEqual(2, len(courses))

        self.assertCoursesEqual([self.course, c1], courses)

    def test_override_precedent(self):
        # even if a course is in the list of courses, don't include it if it's in the list of overrides
        self.req1.courses.add(self.course2)
        courses = self.req1.satisfying_courses.all()
        self.assertEqual(1, len(courses))
        self.assertCoursesEqual([self.course], courses)
        reqs = self.course2.requirements
        self.assertEqual(1, len(reqs))
        self.assertEqual(self.req2, reqs[0])


class MeetingTestCase(TestCase):
    def setUp(self):
        pass


'''
API Test Cases
'''


class TypedSearchBackendTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.search = TypedSearchBackend()

    def test_type_course(self):
        req = self.factory.get('/', {'type': 'course', 'search': 'ABC123'})
        terms = self.search.get_search_fields(None, req)
        self.assertEqual(['full_code'], terms)

    def test_type_keyword(self):
        req = self.factory.get('/', {'type': 'keyword', 'search': 'ABC123'})
        terms = self.search.get_search_fields(None, req)
        self.assertEqual(['title', 'sections__instructors__name'], terms)

    def test_auto_course(self):
        courses = ['cis', 'CIS', 'cis120', 'anch-027', 'cis 121', 'ling-140']
        for course in courses:
            req = self.factory.get('/', {'type': 'auto', 'search': course})
            terms = self.search.get_search_fields(None, req)
            self.assertEqual(['full_code'], terms, f'search:{course}')

    def test_auto_keyword(self):
        keywords = ['rajiv', 'gandhi', 'programming', 'hello world']
        for kw in keywords:
            req = self.factory.get('/', {'type': 'auto', 'search': kw})
            terms = self.search.get_search_fields(None, req)
            self.assertEqual(['title', 'sections__instructors__name'], terms, f'search:{kw}')


@override_settings(SWITCHBOARD_TEST_APP='api')
class CourseListTestCase(TestCase):
    def setUp(self):
        self.course, self.section = get_course_and_section('CIS-120-001', TEST_SEMESTER)
        self.math, self.math1 = get_course_and_section('MATH-114-001', TEST_SEMESTER)
        self.client = APIClient()
        set_semester()

    def test_get_courses(self):
        response = self.client.get('/all/courses/')
        self.assertEqual(len(response.data), 2)
        course_codes = [d['course_id'] for d in response.data]
        self.assertTrue('CIS-120' in course_codes and 'MATH-114' in course_codes)

    def test_search_by_dept(self):
        response = self.client.get('/all/courses/', {'search': 'math', 'type': 'auto'})
        self.assertEqual(len(response.data), 1)
        course_codes = [d['course_id'] for d in response.data]
        self.assertTrue('CIS-120' not in course_codes and 'MATH-114' in course_codes)

    def test_search_by_instructor(self):
        self.section.instructors.add(Instructor.objects.get_or_create(name='Tiffany Chang')[0])
        self.math1.instructors.add(Instructor.objects.get_or_create(name='Josh Doman')[0])
        searches = ['Tiffany', 'Chang']
        for search in searches:
            response = self.client.get('/all/courses/', {'search': search, 'type': 'auto'})
            self.assertEqual(len(response.data), 1)
            course_codes = [d['course_id'] for d in response.data]
            self.assertTrue('CIS-120' in course_codes and 'MATH-114' not in course_codes, f'search:{search}')

    def test_semester_setting(self):
        new_sem = TEST_SEMESTER[:-1] + 'Z'
        get_course_and_section('MATH-104-001', new_sem)

        response = self.client.get(f'/{TEST_SEMESTER}/courses/')
        self.assertEqual(len(response.data), 2)

        response = self.client.get(f'/{new_sem}/courses/')
        self.assertEqual(len(response.data), 1)

        response = self.client.get('/all/courses/')
        self.assertEqual(len(response.data), 3)

    def test_current_semester(self):
        new_sem = TEST_SEMESTER[:-1] + 'Z'
        get_course_and_section('MATH-104-001', new_sem)
        response = self.client.get(f'/current/courses/')
        self.assertEqual(len(response.data), 2)


@override_settings(SWITCHBOARD_TEST_APP='api')
class SectionListTestCase(TestCase):
    def setUp(self):
        self.course1, self.section1 = get_course_and_section('CIS-120-001', TEST_SEMESTER)
        self.course2, self.section2 = get_course_and_section('CIS-120-002', TEST_SEMESTER)
        self.client = APIClient()
        set_semester()

    def test_get_sections(self):
        response = self.client.get('/all/sections/')
        self.assertEqual(len(response.data), 2)
        codes = [d['section_id'] for d in response.data]
        self.assertTrue('CIS-120-001' in codes and 'CIS-120-002' in codes)


@override_settings(SWITCHBOARD_TEST_APP='api')
class CourseDetailTestCase(TestCase):
    def setUp(self):
        self.course, self.section = get_course_and_section('CIS-120-001', TEST_SEMESTER)
        self.math, self.math1 = get_course_and_section('MATH-114-001', TEST_SEMESTER)
        self.client = APIClient()
        set_semester()

    def test_get_course(self):
        course, section = get_course_and_section('CIS-120-201', TEST_SEMESTER)
        response = self.client.get('/all/courses/CIS-120/')
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.data['course_id'], 'CIS-120')
        self.assertEqual(len(response.data['sections']), 2)

    def test_not_get_course(self):
        response = self.client.get('/all/courses/CIS-160/')
        self.assertEqual(response.status_code, 404)
