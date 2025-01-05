from django.shortcuts import render, get_object_or_404, redirect
from .models import Form, Response, Answer, Question, Option
from collections import Counter

def form_list(request):
    forms = Form.objects.all()
    return render(request, 'form_list.html', {'forms': forms})


def form_detail(request, form_id):
    form = get_object_or_404(Form, id=form_id)
    
    if request.method == 'POST':
        # Initialize a flag to check if all required fields are filled
        all_fields_filled = True
        
        response = Response.objects.create(form=form)
        
        # Iterate through all questions and check if all required fields are filled
        for question in form.questions.all().order_by('order'):
            if question.question_type == 'text':
                text_answer = request.POST.get(f'question_{question.id}')
                if not text_answer:  # If the text answer is empty, set the flag to False
                    all_fields_filled = False
                    break  # No need to check further, stop processing
                Answer.objects.create(response=response, question=question, text_answer=text_answer)
            
            elif question.question_type in ['checkbox', 'dropdown']:
                selected_options = request.POST.getlist(f'question_{question.id}')
                if not selected_options:  # If no options are selected, set the flag to False
                    all_fields_filled = False
                    break  # No need to check further, stop processing
                answer = Answer.objects.create(response=response, question=question)
                for option_id in selected_options:
                    try:
                        option = Option.objects.get(id=option_id)
                        answer.selected_options.add(option)
                    except ObjectDoesNotExist:
                        pass  # Handle missing options gracefully
        
        # If all fields are filled, redirect to the thank you page
        if all_fields_filled:
            return redirect('form_submission_success')
        else:
            # If any field is missing, show an error message and re-render the form
            return render(request, 'form_detail.html', {'form': form, 'error_message': 'Please fill out all fields.'})
    
    return render(request, 'form_detail.html', {'form': form})


def form_submission_success(request):
    return render(request, 'form_submission_success.html')

from collections import defaultdict

def analytics(request, form_id):
    form = get_object_or_404(Form, id=form_id)
    total_responses = form.responses.count()

    question_data = []
    for question in form.questions.all():
        if question.question_type == 'text':
            answers = question.answer_set.values_list('text_answer', flat=True)
            words = ' '.join(answers).split()
            word_count = {}
            for word in words:
                if len(word) >= 5:  # Filter for words of length 5 or more
                    word_count[word] = word_count.get(word, 0) + 1
            sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
            top_words = sorted_words[:5]
            others = sorted_words[5:]
            if others:
                others_count = sum(count for _, count in others)
                top_words.append(('Others', others_count))
            question_data.append({
                'question': question.text,
                'type': 'text',
                'data': top_words
            })
        
        # elif question.question_type == 'checkbox':
        #     options = question.options.all()
        #     option_combinations = defaultdict(int)
        #     for answer in question.answer_set.all():
        #         selected_options = tuple(sorted(option.text for option in answer.selected_options.all()))
        #         option_combinations[selected_options] += 1
        #     sorted_combinations = sorted(option_combinations.items(), key=lambda x: x[1], reverse=True)
        #     top_combinations = sorted_combinations[:5]
        #     others = sorted_combinations[5:]
        #     if others:
        #         others_count = sum(count for _, count in others)
        #         top_combinations.append(('Others', others_count))
        #     question_data.append({
        #         'question': question.text,
        #         'type': 'checkbox',
        #         'data': top_combinations
        #     })
        elif question.question_type == 'checkbox':
            # Handle checkbox questions (option combinations)
            options = question.options.all()
            option_combinations = defaultdict(int)
            for answer in question.answer_set.all():
                selected_options = sorted(option.text for option in answer.selected_options.all())
                selected_options_str = ', '.join(selected_options)  # Join selected options into a single string
                option_combinations[selected_options_str] += 1  # Store as a string
            sorted_combinations = sorted(option_combinations.items(), key=lambda x: x[1], reverse=True)
            top_combinations = sorted_combinations[:5]
            others = sorted_combinations[5:]
            if others:
                others_count = sum(count for _, count in others)
                top_combinations.append(('Others', others_count))
            question_data.append({
                'question': question.text,
                'type': 'checkbox',
                'data': top_combinations
            })
        
        elif question.question_type == 'dropdown':
            option_count = defaultdict(int)
            for answer in question.answer_set.all():
                for option in answer.selected_options.all():
                    option_count[option.text] += 1
            sorted_options = sorted(option_count.items(), key=lambda x: x[1], reverse=True)
            top_options = sorted_options[:5]
            others = sorted_options[5:]
            if others:
                others_count = sum(count for _, count in others)
                top_options.append(('Others', others_count))
            question_data.append({
                'question': question.text,
                'type': 'dropdown',
                'data': top_options
            })

    return render(request, 'analytics.html', {
        'form': form,
        'total_responses': total_responses,
        'question_data': question_data,
    })
