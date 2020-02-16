from django.db import models
from django.db.models import Avg, Q


class Review(models.Model):
    """
    Represents the aggregate review for an instructor for a single section of a course.
    By virtue of being associated to a course, every semester of a course will have a new Review
    object.

    Actual scores for the review is stored in the ReviewBit related object, can be accessed via the
    `reviewbit_set` of the object.
    """

    # sections have at most one review per instructor attached to the section.
    section = models.ForeignKey("courses.Section", on_delete=models.CASCADE)
    instructor = models.ForeignKey("courses.Instructor", on_delete=models.CASCADE)

    class Meta:
        unique_together = (("section", "instructor"),)

    def __str__(self):
        return f"{self.section} - {self.instructor}"

    def set_scores(self, bits):
        for key, value in bits.items():
            ReviewBit.objects.update_or_create(review=self, field=key, defaults={"score": value})

    @staticmethod
    def get_averages(course_code, instructor_name=None, fields=None):
        if fields is None:
            # Default fields (topline numbers on PCR)
            fields = [
                "course_quality",
                "difficulty",
                "instructor_quality",
            ]

        # We're using some of the aggregation tricks documented on Django's Aggregation Cheat Sheet:
        # https://docs.djangoproject.com/en/2.2/topics/db/aggregation/#cheat-sheet

        # Filter down a queryset to just include this course
        qs = Review.objects.filter(section__course__full_code=course_code)
        if (
            instructor_name is not None
        ):  # if an instructor is specified, filter down to just that instructor
            qs = qs.filter(instructor_name__contains=instructor_name)

        # pass each aggregation as its own argument to `aggregate` (using dictionary comprehensions)
        return qs.aggregate(
            **{
                # average the score of all the reviewbits of a certain field
                # (that's where the filter comes in)
                field: Avg("reviewbit__score", filter=Q(reviewbit__field=field))
                for field in fields
            }
        )


class ReviewBit(models.Model):
    """
    A single key/value pair associated with a review. Fields are things like "course_quality",
    and scores are averages which range from 0 to 4.
    """

    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    field = models.CharField(max_length=32)
    score = models.DecimalField(max_digits=6, decimal_places=5)

    class Meta:
        unique_together = (("review", "field"),)

    def __str__(self):
        return f"#{self.review.pk} - {self.field}: {self.score}"
