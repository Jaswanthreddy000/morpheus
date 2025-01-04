from django.shortcuts import render, get_object_or_404, redirect
from .models import Form, Response, Answer, Question, Option

def form_list(request):
    forms = Form.objects.all()
    return render(request, 'form_list.html', {'forms': forms})

def form_detail(request, form_id):
    form = get_object_or_404(Form, id=form_id)
    if request.method == 'POST':
        response = Response.objects.create(form=form)
        for question in form.questions.all():
            if question.question_type == 'text':
                Answer.objects.create(response=response, question=question, text_answer=request.POST.get(f'question_{question.id}'))
            elif question.question_type in ['checkbox', 'dropdown']:
                answer = Answer.objects.create(response=response, question=question)
                selected_options = request.POST.getlist(f'question_{question.id}')
                for option_id in selected_options:
                    answer.selected_options.add(Option.objects.get(id=option_id))
        return redirect('thank_you')
    return render(request, 'form_detail.html', {'form': form})

def thank_you(request):
    return render(request, 'thank_you.html')



def form_analytics(request, form_id):
    form = get_object_or_404(Form, id=form_id)
    total_responses = form.responses.count()

    question_data = []
    for question in form.questions.all():
        if question.question_type == 'text':
            answers = question.answer_set.values_list('text_answer', flat=True)
            words = ' '.join(answers).split()
            word_count = {}
            for word in words:
                if len(word) >= 5:
                    word_count[word] = word_count.get(word, 0) + 1
            sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
            question_data.append({
                'question': question.text,
                'type': 'text',
                'data': sorted_words[:5]
            })
        elif question.question_type == 'checkbox':
            options = question.options.all()
            option_count = {option.text: 0 for option in options}
            for answer in question.answer_set.all():  # Update here
                for option in answer.selected_options.all():
                    option_count[option.text] += 1
            sorted_options = sorted(option_count.items(), key=lambda x: x[1], reverse=True)
            question_data.append({
                'question': question.text,
                'type': 'checkbox',
                'data': sorted_options[:5]
            })
        elif question.question_type == 'dropdown':
            options = question.options.all()
            option_count = {option.text: 0 for option in options}
            for answer in question.answer_set.all():
                for option in answer.selected_options.all():
                    option_count[option.text] += 1
            sorted_options = sorted(option_count.items(), key=lambda x: x[1], reverse=True)
            question_data.append({
                'question': question.text,
                'type': 'dropdown',
                'data': sorted_options[:5]
            })

    return render(request, 'form_analytics.html', {
        'form': form,
        'total_responses': total_responses,
        'question_data': question_data,
    })
