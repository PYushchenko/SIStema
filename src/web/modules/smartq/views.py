# -*- coding: utf-8 -*-

import collections
import datetime
import json
import random
import types
import uuid

from django import forms
from django import shortcuts
from django.db import models
from django.http import response
import jinja2

from modules.smartq import api

heap_template_html = """
    <p>
        Постройте кучу минимумов из элементов:
        {% for x in data.heap_elements %}<b>{{ x }}</b>{% if not loop.last %}, {% endif %}{% endfor %}.
    </p>
    <div style="position: relative; width: 600px;">
        <canvas id="canvas-{{ short_name }}" width="800" height="400" style="width: 100%; border: 1px solid #ddd;"></canvas>
        <div id="overlay-{{ short_name }}" style="width: 100%; position: absolute; top: 0; left: 0;">
        {% for field in form %}
            {{ field }}
        {% endfor %}
        </div>
    </div>
"""

# TODO: shouldn't depend on field ids
heap_template_js = """
(function() {
    function draw_heap(canvas, overlay, n) {
        var depth = Math.floor(1 + Math.log2(n));
        var ctx = canvas.getContext('2d');
        var canvas_width = canvas.width;
        var canvas_height = canvas.height;
        var overlay_width = canvas.offsetWidth;
        var overlay_height = canvas.offsetHeight;
        var canvas_to_overlay = overlay_width / canvas_width;

        var levels = [];
        for (var i = 0; i <= depth; ++i) {
            levels.push(i * canvas_height / (depth + 1));
        }

        var nodes = {};
        var level = 0, level_size = 0, j = 0;
        for (var i = 1; i <= n; ++i, ++j) {
            if (!(i & (i - 1))) {
                level_size = 1 << level;
                level++;
                j = 0;
                var node_width = canvas_width / level_size;
            }

            var x = node_width * (0.5 + j);
            var y = levels[level];
            nodes[i] = {x: x, y: y};

            if (i > 1) {
                var parent_node = nodes[Math.floor(i / 2)];
                ctx.moveTo(parent_node.x, parent_node.y);
                ctx.lineTo(x, y);
            }

            input = document.getElementById('id_{{ short_name }}-element_' + i);
            input.style['text-align'] = 'center';
            input.style.width = '4em';
            input.style.position = 'absolute';
            input.style.top = y * canvas_to_overlay - input.offsetHeight / 2 + 'px';
            input.style.left = x * canvas_to_overlay - input.offsetWidth / 2 + 'px';
        }

        ctx.stroke();
    }

    var canvas = document.getElementById('canvas-{{ short_name }}');
    var overlay = document.getElementById('overlay-{{ short_name }}');
    draw_heap(canvas, overlay, {{ data.heap_elements|length }});
})();
"""

# TODO: what demanding single instances of Generator and Checker instead of
#       making their names fixed? Can be changed later if neccessary.
heap_code = """
import random
import re

class Generator(api.Generator):
    def __init__(self):
        self.size = 10

    def generate(self):
        elements = random.sample(range(100), self.size)

        regexp = '|'.join(map(str, elements))
        answer_fields = [api.AnswerFieldSpec.text(validation_regexp=regexp)
                         for _ in elements]

        return api.GeneratedQuestionData(
            answer_fields=answer_fields,
            heap_elements=elements)


class Checker(api.Checker):
    def __init__(self):
        pass

    def check(self, generated_question_data, answer):
        elements = generated_question_data.heap_elements
        regexp = '|'.join(str(x) for x in elements)
        for x in answer:
            if not re.fullmatch(regexp, x):
                self.message = 'Число {} не содержится среди данных элементов'.format(x)
                return self.Result.PE

        answer_heap = list(map(int, answer))
        if sorted(elements) != sorted(answer_heap):
            self.message = 'Набор элементов кучи не совпадает с заданным набором элементов'
            return self.Result.PE

        print(answer_heap)
        for i in range(1, len(answer_heap)):
            child = answer_heap[i]
            parent = answer_heap[(i + 1) // 2 - 1]
            if child < parent:
                self.message = 'Число {x} меньше {y}, но является при этом его потомком'.format(x=child, y=parent)
                return self.Result.WA

        self.message = ''
        return self.Result.OK
"""


class Question(models.Model):
    # TODO: two formats of short_name (modules and urls)
    short_name = models.CharField(max_length=100, unique=True)

    template_html = models.TextField()

    template_css = models.TextField(blank=True, default='')

    template_js = models.TextField(blank=True, default='')

    # TODO(Artem Tabolin): consider adding version control
    code = models.TextField()

    compiled_code = models.BinaryField(blank=True)

    created_date = models.DateTimeField(auto_now_add=True)

    modified_date = models.DateTimeField(auto_now=True)

    _implementation_cache = {}
    _template_cache = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seed = None
        self._generator = None

    @property
    def _implementation(self):
        module = self._implementation_cache.get(self.short_name)
        if module is None or module.modified_date < self.modified_date:
            module = types.ModuleType(name=self.short_name)
            module.api = api
            # TODO: add safety layer
            exec(self.code, module.__dict__)  # TODO: use compiled_code
            module.modified_date = self.modified_date

            self._implementation_cache[self.short_name] = module

        return module

    def save(self, *args, **kwargs):
        # TODO: validate the code
        super().save(*args, **kwargs)

    def generate_with_seed(self, seed):
        seed = str(seed)[:100]

        # TODO(artemtab): how it behaves when there are several threads?
        # TODO(artemtab): most probably we need strong consistency
        state = random.getstate()
        random.seed(seed)
        # TODO: run in a separate thread and enforce TL
        data = self._implementation.Generator().generate()
        random.setstate(state)

        # TODO: replace with objects.create
        return GeneratedQuestion(
            base_question=self,
            seed=seed,
            data_json=json.dumps(data.__dict__))


# TODO: better API for forms
class GeneratedQuestion(models.Model):
    base_question = models.ForeignKey(Question)

    seed = models.CharField(max_length=100)

    data_json = models.CharField()

    # TODO: what about custom manager which is doing serialization itself?

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        data_dict = json.loads(self.data_json)
        self.data = api.GeneratedQuestionData(**data_dict)

        self.form_type = make_form_type(self.base_question.short_name,
                                        self.data.answer_fields)
        self.form = self.form_type()

    def html(self):
        context = {
            'short_name': self.base_question.short_name,
            'data': self.data,
            'form': self.form,
        }

        # TODO: add cache layer
        return jinja2.Template(self.base_question.template_html).render(context)

    def css(self):
        context = {
            'short_name': self.base_question.short_name,
            'data': self.data,
            'form': self.form,
        }

        # TODO: add cache layer
        return jinja2.Template(self.base_question.template_css).render(context)

    def js(self):
        context = {
            'short_name': self.base_question.short_name,
            'data': self.data,
            'form': self.form,
        }

        # TODO: add cache layer
        return jinja2.Template(self.base_question.template_js).render(context)

    def check(self, answer_values):
        # TODO: add safety layer
        checker = self.base_question._implementation.Checker()
        status = checker.check(self.data, answer_values)
        # TODO: remove this dirty hack
        checker.status = status
        return checker


def make_form_type(prefix, field_specs):
    fields = {}
    field_order = []

    for i, spec in enumerate(field_specs):
        # TODO: add prefix to name
        field_name = 'element_' + str(i + 1)
        prefixed_name = '-'.join([prefix, field_name])

        field = None
        if spec['type'] == api.AnswerFieldSpec.Type.TEXT:
            # TODO: custom widgets for regexp check?
            # TODO: min_length, max_length
            # TODO: mutiline
            field = forms.CharField()

        if spec['type'] == api.AnswerFieldSpec.Type.INTEGER:
            # TODO: custom widgets for regexp check?
            field = forms.IntegerField(
                min_value=spec.get('min_value'),
                max_value=spec.get('max_value'))

        if field is None:
            # TODO: what is the right thing to do here?
            raise Exception('Unknown field type')

        fields[field_name] = field
        field_order.append(field_name)

    return type('SmartQForm', (forms.BaseForm,), {
        'default_renderer': 'django.forms.renderers.Jinja2',
        'base_fields': fields,
        'field_order': field_order,
        'prefix': prefix,
    })


def heap(request, seed='100500'):
    question = Question(
        short_name='build_heap',
        template_html=heap_template_html,
        template_js=heap_template_js,
        code=heap_code,
        modified_date=datetime.datetime.now())

    generated_question = question.generate_with_seed(seed)

    status = 'NA'

    if request.method == 'POST':
        form = generated_question.form_type(request.POST)
        if form.is_valid():
            answer_values = [form.cleaned_data[name]
                             for name in form.field_order]
            result = generated_question.check(answer_values)
            status = '{}: {}'.format(repr(result.status), result.message)
            generated_question.form = form

    return shortcuts.render(request, 'smartq/question.html', {
        'question': generated_question,
        'status': status,
    })