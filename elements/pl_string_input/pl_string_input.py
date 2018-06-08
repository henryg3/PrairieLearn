import lxml.html
from html import escape
import chevron
import math
import prairielearn as pl
import numpy as np
import random


def prepare(element_html, element_index, data):
    element = lxml.html.fragment_fromstring(element_html)
    required_attribs = ['answers_name']
    optional_attribs = ['weight', 'correct_answer', 'label', 'suffix', 'display', 'remove_leading_trailing' , 'remove_between_spaces', 'allow_blank']
    pl.check_attribs(element, required_attribs, optional_attribs)

    name = pl.get_string_attrib(element, 'answers_name')
    correct_answer = pl.get_string_attrib(element, 'correct_answer', None)

    if correct_answer is not None:
        if name in data['correct_answers']:
            raise Exception('duplicate correct_answers variable name: %s' % name)
        data['correct_answers'][name] = correct_answer


def render(element_html, element_index, data):
    element = lxml.html.fragment_fromstring(element_html)
    name = pl.get_string_attrib(element, 'answers_name')
    label = pl.get_string_attrib(element, 'label', None)
    suffix = pl.get_string_attrib(element, 'suffix', None)
    display = pl.get_string_attrib(element, 'display', 'inline')
    remove_leading_trailing =  pl.get_string_attrib(element, 'remove_leading_trailing', False)
    remove_between_spaces = pl.get_string_attrib(element, 'remove_between_spaces', False)
    allow_blank = pl.get_string_attrib(element, 'allow_blank', False)

    if data['panel'] == 'question':
        editable = data['editable']
        raw_submitted_answer = data['raw_submitted_answers'].get(name, None)

        # Get info strings
        info_params = {'format': True}
        with open('pl_string_input.mustache', 'r', encoding='utf-8') as f:
            info = chevron.render(f, info_params).strip()
        with open('pl_string_input.mustache', 'r', encoding='utf-8') as f:
            info_params.pop('format', None)
            info_params['shortformat'] = True
            shortinfo = chevron.render(f, info_params).strip()

        html_params = {
            'question': True,
            'name': name,
            'label': label,
            'suffix': suffix,
            'remove_leading_trailing': remove_leading_trailing,
            'remove_between_spaces': remove_between_spaces,
            'editable': editable,
            'info': info,
            'shortinfo': shortinfo,
            'uuid': pl.get_uuid()
        }

        partial_score = data['partial_scores'].get(name, {'score': None})
        score = partial_score.get('score', None)
        if score is not None:
            try:
                score = float(score)
                if score >= 1:
                    html_params['correct'] = True
                elif score > 0:
                    html_params['partial'] = math.floor(score * 100)
                else:
                    html_params['incorrect'] = True
            except Exception:
                raise ValueError('invalid score' + score)

        if display == 'inline':
            html_params['inline'] = True
        elif display == 'block':
            html_params['block'] = True
        else:
            raise ValueError('method of display "%s" is not valid (must be "inline" or "block")' % display)
        if raw_submitted_answer is not None:
            html_params['raw_submitted_answer'] = escape(raw_submitted_answer)
        with open('pl_string_input.mustache', 'r', encoding='utf-8') as f:
            html = chevron.render(f, html_params).strip()

    elif data['panel'] == 'submission':
        parse_error = data['format_errors'].get(name, None)
        html_params = {
            'submission': True,
            'label': label,
            'parse_error': parse_error,
            'uuid': pl.get_uuid()
        }

        if parse_error is None:
            # Get submitted answer, raising an exception if it does not exist
            a_sub = data['submitted_answers'].get(name, None)
            if a_sub is None:
                raise Exception('submitted answer is None')

            # If answer is in a format generated by pl.to_json, convert it
            # back to a standard type (otherwise, do nothing)
            a_sub = pl.from_json(a_sub)

            html_params['suffix'] = suffix
            html_params['a_sub'] = a_sub
        else:
            raw_submitted_answer = data['raw_submitted_answers'].get(name, None)
            if raw_submitted_answer is not None:
                html_params['raw_submitted_answer'] = escape(raw_submitted_answer)

        partial_score = data['partial_scores'].get(name, {'score': None})
        score = partial_score.get('score', None)
        if score is not None:
            try:
                score = float(score)
                if score >= 1:
                    html_params['correct'] = True
                elif score > 0:
                    html_params['partial'] = math.floor(score * 100)
                else:
                    html_params['incorrect'] = True
            except Exception:
                raise ValueError('invalid score' + score)

        with open('pl_string_input.mustache', 'r', encoding='utf-8') as f:
            html = chevron.render(f, html_params).strip()
    elif data['panel'] == 'answer':
        a_tru = pl.from_json(data['correct_answers'].get(name, None))
        if a_tru is not None:
            html_params = {'answer': True, 'label': label, 'a_tru': a_tru, 'suffix': suffix}
            with open('pl_string_input.mustache', 'r', encoding='utf-8') as f:
                html = chevron.render(f, html_params).strip()
        else:
            html = ''
    else:
        raise Exception('Invalid panel type: %s' % data['panel'])

    return html


def parse(element_html, element_index, data):
    element = lxml.html.fragment_fromstring(element_html)
    name = pl.get_string_attrib(element, 'answers_name')
    # Get allow_blank option
    allow_blank = pl.get_string_attrib(element, 'allow_blank', False)

    # Get submitted answer or return parse_error if it does not exist
    a_sub = data['submitted_answers'].get(name, None)
    if a_sub is None:
        data['format_errors'][name] = 'No submitted answer.'
        data['submitted_answers'][name] = None
        return

    try:
        # check if answer is left blank
        if not a_sub:
            if not allow_blank:
                raise ValueError('invalid submitted answer (left blank)')
        data['submitted_answers'][name] = pl.to_json(a_sub)
    except Exception:
        data['format_errors'][name] = 'Invalid format. The submitted answer was left blank.'
        data['submitted_answers'][name] = None


def grade(element_html, element_index, data):
    element = lxml.html.fragment_fromstring(element_html)
    name = pl.get_string_attrib(element, 'answers_name')

    # Get weight
    weight = pl.get_integer_attrib(element, 'weight', 1)

    # Get remove_between_spaces option
    remove_between_spaces = pl.get_string_attrib(element, 'remove_between_spaces', False)

    # Get remove_leading_trailing option
    remove_leading_trailing = pl.get_string_attrib(element, 'remove_leading_trailing', False)

    # Get true answer (if it does not exist, create no grade - leave it
    # up to the question code)
    a_tru = pl.from_json(data['correct_answers'].get(name, None))
    if a_tru is None:
        return

    # Get submitted answer (if it does not exist, score is zero)
    a_sub = data['submitted_answers'].get(name, None)
    if a_sub is None:
        data['partial_scores'][name] = {'score': 0, 'weight': weight}
        return
    # If submitted answer is in a format generated by pl.to_json, convert it
    # back to a standard type (otherwise, do nothing)
    a_sub = pl.from_json(a_sub)

    # Remove the leading and trailing characters
    if (remove_leading_trailing):
        a_sub = a_sub.strip()

    # Remove the blank spaces between characters
    if (remove_between_spaces):
        a_sub = a_sub.replace(" ","")

    if a_tru == a_sub:
        data['partial_scores'][name] = {'score': 1, 'weight': weight}
    else:
        data['partial_scores'][name] = {'score': 0, 'weight': weight}


def test(element_html, element_index, data):
    element = lxml.html.fragment_fromstring(element_html)
    name = pl.get_string_attrib(element, 'answers_name')
    weight = pl.get_integer_attrib(element, 'weight', 1)
    # Get allow_blank option
    allow_blank = pl.get_string_attrib(element, 'allow_blank', False)

    # Get correct answer
    a_tru = data['correct_answers'][name]

    # If correct answer is in a format generated by pl.to_json, convert it
    # back to a standard type (otherwise, do nothing)
    a_tru = pl.from_json(a_tru)

    result = random.choices(['correct', 'incorrect'], [5, 5])[0]

    if result == 'correct':
        data['raw_submitted_answers'][name] = a_tru
        data['partial_scores'][name] = {'score': 1, 'weight': weight}
    elif result == 'incorrect':
        data['raw_submitted_answers'][name] = a_tru + str((random.randint(1, 11) * random.choice([-1, 1])))
        data['partial_scores'][name] = {'score': 0, 'weight': weight}
    # No test for 'invalid' implemented at this time
    else:
        raise Exception('invalid result: %s' % result)
