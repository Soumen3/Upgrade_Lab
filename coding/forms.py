from django import forms
from .models import Problem, TestCase, CodeSnippet

class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ['title', 'description', 'difficulty_level', 'sample_input', 'sample_output', 'tags']
        help_texts = {
            'sample_input': 'Provide sample input in JSON format. e.g. [{"input1": "value1"}, {"input2": "value2"}]',
            'sample_output': 'Provide sample output in JSON format. ["output1", "output2"]'
        }

class TestCaseForm(forms.ModelForm):
    class Meta:
        model = TestCase
        fields = ['input_data', 'expected_output']
        help_texts = {
            'input_data': 'Provide input data in JSON format. e.g. [{"input1": "value1"}, {"input2": "value2"}]',
            'expected_output': 'Provide expected output in JSON format. ["output1", "output2"]'
        }