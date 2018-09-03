from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .forms import TopicForm,EntryForm
from .models import Topic,Entry

# Create your views here.

def index(request):
    """学习笔记的主页"""
    return render(request,'learninglogs/index.html')

@login_required
def topics(request):
    """显示所有的主题"""
    topic = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics':topics}
    return render(request,'learninglogs/topics.html',context)

@login_required
def topic(request,topic_id):
    """显示单个主题及其所有的条目"""
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic':topic,'entries':entries}

    return render(request,'learninglogs/topic.html',context)

@login_required
def new_topic(request):
    """添加新主题"""
    if request.method != 'POST':
        # 未提交数据：创建一个新表单
        form = TopicForm()
    else:
        # POST提交的数据，对数据进行处理
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learninglogs:topics'))

    context = {'form':form}
    return render(request,'learninglogs/new_topic.html',context)

@login_required
def new_entry(request,topic_id):
    """在特定的主题中添加新条目"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        # 未提交数据，创建一个空表单
        form = EntryForm()
    else:
        # POST提交的数据，对数据进行处理
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learninglogs:topic',args=[topic_id]))
    context = {'topic':topic,'form':form}
    return render(request,'learninglogs/new_entry.html',context)

@login_required
def edit_entry(request,entry_id):
    """用户可以编辑既有的条目"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if request.method != 'POST':
        # 初次请求，使用当前条目填充表单
        form = EntryForm(instance=entry)
    else:
        # POST提交的数据，对数据进行处理
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learninglogs:topic',args=[topic.id]))

    context = {'entry':entry,'topic':topic,'form':form}
    return render(request,'learninglogs/edit_entry.html',context)
