
# from django.contrib import admin
# from .models import Form, Question, Option, Response, Answer

# # Inline for Questions
# class QuestionInline(admin.TabularInline):
#     model = Question
#     extra = 0
#     fields = ('text', 'question_type', 'order')
#     ordering = ['order']

#     def get_queryset(self, request):
#         # Ensure only saved questions are shown
#         queryset = super().get_queryset(request)
#         return queryset.filter(form__isnull=False)


# # Inline for Options
# class OptionInline(admin.TabularInline):
#     model = Option
#     extra = 0
#     fields = ('text', 'order')
#     ordering = ['order']

#     def get_queryset(self, request):
#         # Ensure only saved options are shown
#         queryset = super().get_queryset(request)
#         return queryset.filter(question__isnull=False)


# # Admin for Questions
# class QuestionAdmin(admin.ModelAdmin):
#     list_display = ('text', 'form', 'question_type', 'order')
#     list_filter = ('form', 'question_type')
#     list_editable = ('order',)
#     search_fields = ('text',)
#     ordering = ['order']
#     inlines = [OptionInline]

#     actions = ['sort_questions_ascending', 'sort_questions_descending']

#     def sort_questions_ascending(self, request, queryset):
#         """Sort questions in ascending order."""
#         for idx, question in enumerate(queryset.order_by('order'), start=1):
#             if question.pk:  # Ensure the question has been saved
#                 question.order = idx
#                 question.save()
#         self.message_user(request, "Questions sorted in ascending order.")

#     sort_questions_ascending.short_description = "Sort questions in ascending order"

#     def sort_questions_descending(self, request, queryset):
#         """Sort questions in descending order."""
#         for idx, question in enumerate(queryset.order_by('-order'), start=1):
#             if question.pk:  # Ensure the question has been saved
#                 question.order = idx
#                 question.save()
#         self.message_user(request, "Questions sorted in descending order.")

#     sort_questions_descending.short_description = "Sort questions in descending order"


# # Admin for Options
# class OptionAdmin(admin.ModelAdmin):
#     list_display = ('text', 'question', 'order')
#     list_filter = ('question',)
#     list_editable = ('order',)
#     search_fields = ('text',)
#     ordering = ['order']


# # Admin for Forms
# class FormAdmin(admin.ModelAdmin):
#     list_display = ('title',)
#     search_fields = ('title',)
#     inlines = [QuestionInline]

#     def save_model(self, request, obj, form, change):
#         """Ensure the Form instance is saved before adding related objects."""
#         super().save_model(request, obj, form, change)

#     def save_related(self, request, form, formsets, change):
#         """Ensure related objects are processed after the Form instance is saved."""
#         # Save the form first to get the primary key
#         super().save_related(request, form, formsets, change)

#         # Once the Form has been saved, assign an order to each question
#         for question in form.questions.all():
#             if not question.order:  # Set default order if not already assigned
#                 question.order = question.id  # You can assign order based on the id
#                 question.save()


# # Admin for Responses
# class ResponseAdmin(admin.ModelAdmin):
#     list_display = ('form', 'submitted_at')
#     list_filter = ('form', 'submitted_at')
#     search_fields = ('form__title',)


# # Admin for Answers
# class AnswerAdmin(admin.ModelAdmin):
#     list_display = ('response', 'question', 'text_answer')
#     list_filter = ('question__form', 'question__question_type')
#     search_fields = ('response__form__title', 'question__text', 'text_answer')


# # Register models with admin
# admin.site.register(Form, FormAdmin)
# admin.site.register(Question, QuestionAdmin)
# admin.site.register(Option, OptionAdmin)
# admin.site.register(Response, ResponseAdmin)
# admin.site.register(Answer, AnswerAdmin)

from django.contrib import admin
from .models import Form, Question, Option, Response, Answer

# Inline for Questions
class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0
    fields = ('text', 'question_type', 'order')

# Inline for Options
class OptionInline(admin.TabularInline):
    model = Option
    extra = 0
    fields = ('text', 'order')

# Admin for Forms
class FormAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    inlines = [QuestionInline]

# Admin for Questions
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'form', 'question_type', 'order')
    list_filter = ('form', 'question_type')
    list_editable = ('order',)

# Admin for Options
class OptionAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'order')
    list_filter = ('question',)
    list_editable = ('order',)

# Admin for Responses
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('form', 'submitted_at')
    list_filter = ('form', 'submitted_at')

# Admin for Answers
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('response', 'question', 'text_answer')
    list_filter = ('question__form', 'question__question_type')

# Register models with admin
admin.site.register(Form, FormAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Option, OptionAdmin)
admin.site.register(Response, ResponseAdmin)
admin.site.register(Answer, AnswerAdmin)

# from django.contrib import admin
# from .models import Form, Question, Option, Response, Answer

# # Simple admin registrations for all models

# @admin.register(Form)
# class FormAdmin(admin.ModelAdmin):
#     list_display = ('title',)
#     search_fields = ('title',)


# @admin.register(Question)
# class QuestionAdmin(admin.ModelAdmin):
#     list_display = ('text', 'form', 'question_type', 'order')
#     list_filter = ('form', 'question_type')
#     search_fields = ('text',)


# @admin.register(Option)
# class OptionAdmin(admin.ModelAdmin):
#     list_display = ('text', 'question', 'order')
#     search_fields = ('text',)


# @admin.register(Response)
# class ResponseAdmin(admin.ModelAdmin):
#     list_display = ('form', 'submitted_at')


# @admin.register(Answer)
# class AnswerAdmin(admin.ModelAdmin):
#     list_display = ('response', 'question', 'text_answer')
