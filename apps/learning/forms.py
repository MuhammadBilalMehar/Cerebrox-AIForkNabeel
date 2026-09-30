from django import forms
from apps.accounts.forms import StyledFormMixin
from .models import Course, Topic


class CourseForm(StyledFormMixin, forms.ModelForm):
    """Student-owned course. `student` is set in the view, never exposed here."""
    topics_raw = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 4}),
        help_text='Add one topic name per line or separated by commas.'
    )

    class Meta:
        model = Course
        fields = ('name', 'description', 'icon', 'topics_raw')


class TopicForm(StyledFormMixin, forms.ModelForm):
    """Topic within one of the student's own courses. `course` is set in the view."""
    class Meta:
        model = Topic
        fields = ('name', 'description')


class NotesGenerateForm(StyledFormMixin, forms.Form):
    LENGTH_CHOICES = [('short', 'Short'), ('medium', 'Medium'), ('long', 'Long')]
    length = forms.ChoiceField(choices=LENGTH_CHOICES, initial='medium')


class NotesSectionForm(StyledFormMixin, forms.Form):
    LENGTH_CHOICES = [('short', 'Short'), ('medium', 'Medium'), ('long', 'Long')]
    course = forms.ModelChoiceField(queryset=Course.objects.none(), label='Course')
    topic = forms.ModelChoiceField(queryset=Topic.objects.none(), label='Topic', required=False)
    topic_name = forms.CharField(max_length=150, required=False, label='Or enter a topic name')
    length = forms.ChoiceField(choices=LENGTH_CHOICES, initial='medium')

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['course'].queryset = Course.objects.filter(student=user)
            self.fields['topic'].queryset = Topic.objects.filter(course__student=user)
