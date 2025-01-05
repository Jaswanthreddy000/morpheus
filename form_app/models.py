
from django.db import models
from django.core.exceptions import ValidationError

# Form Model
# class Form(models.Model):
#     title = models.CharField(max_length=255, unique=True)

#     def __str__(self):
#         return self.title

#     def save(self, *args, **kwargs):
#         # Perform validation before saving
#         if self.questions.count() > 100:
#             raise ValidationError("A form cannot have more than 100 questions.")
#         super().save(*args, **kwargs)

#     def get_ordered_questions(self):
#         return self.questions.order_by('order')
class Form(models.Model):
    title = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.title

    def clean(self):
        # Perform validation on related questions count
        if self.pk and self.questions.count() > 100:
            raise ValidationError("A form cannot have more than 100 questions.")

    def save(self, *args, **kwargs):
        # Only save the instance, defer validation to `clean`
        super().save(*args, **kwargs)

# Question Model
class Question(models.Model):
    QUESTION_TYPES = [
        ('text', 'Text'),
        ('dropdown', 'Dropdown'),
        ('checkbox', 'Checkbox'),
    ]
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=255)
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES)
    order = models.IntegerField()  # Order field for sorting questions

    class Meta:
        ordering = ['order']  # Default ordering by 'order'
        unique_together = ('form', 'order')  # Ensure unique order within a form

    def __str__(self):
        return self.text

    def get_ordered_options(self):
        # Retrieve options ordered by their 'order' field
        return self.options.order_by('order')


# Option Model
class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)
    order = models.IntegerField()  # Order field for sorting options

    class Meta:
        ordering = ['order']  # Default ordering by 'order'
        unique_together = ('question', 'order')  # Ensure unique order within a question

    def __str__(self):
        return self.text


# Response Model
class Response(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='responses')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response to {self.form.title} at {self.submitted_at}"


# Answer Model
class Answer(models.Model):
    response = models.ForeignKey(Response, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text_answer = models.TextField(blank=True, null=True)  # For text-based answers
    selected_options = models.ManyToManyField(Option, blank=True)  # For dropdown/checkbox answers

    def clean(self):
        # Validation based on question type
        if self.question.question_type == 'text' and not self.text_answer:
            raise ValidationError("Text answer is required for text questions.")
        if self.question.question_type in ['dropdown', 'checkbox'] and not self.selected_options.exists():
            raise ValidationError("At least one option must be selected for dropdown/checkbox questions.")

    def __str__(self):
        return f"Answer to {self.question.text}"
