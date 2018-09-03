from django import forms

from .models import Topic,Entry

class TopicForm(forms.ModelForm):
    """添加新主题"""
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text':''}

class EntryForm(forms.ModelForm):
    """添加新条目"""
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text':''}
        widgets = {'text':forms.Textarea(attrs={'cols':80})}