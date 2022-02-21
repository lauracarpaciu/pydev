from django.shortcuts import render,get_object_or_404
from .models import Countrie, Department, Employee, Job_History, Job, Location, Region
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.db.models import Q
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
def home(request):
    regions_list = Region.objects.all()
    countries_list = Countrie.objects.all()
    locations_list = Location.objects.all()
    departments_list = Department.objects.all()
    employees_list = Employee.objects.all()
    jobs_list = Job.objects.all()
    job_history_list = Job_History
    
    context = {
        'title': 'Articles',
        'regions_list': regions_list,
        'countries_list': countries_list,
        'locations_list': locations_list,
        'departments_list': departments_list,
        'employees_list': employees_list,
        'jobs_list': jobs_list,
        'job_history_list': job_history_list
    }
    
    return render(request, 'kb/home.html', context)


def search(request):
    template='kb/home.html'

    query=request.GET.get('q')

    result=Employee.objects.filter(Q(first_name__icontains=query) | Q(author__username__icontains=query) | Q(content__icontains=query))
    paginate_by=2
    context={ 'posts':result }
    return render(request,template,context)


def about(request):
    # return HttpResponse('<h1> About knowledge base</h1>')
    context = {'title': 'About KB'}
    return render(request, 'kb/about.html', context)


class ArticleListView(ListView):
    model = Employee
    template_name = 'kb/home.html'  
    context_object_name = 'employees_list'
    ordering = ['-date_posted']
    paginate_by = 2

class UserArticleListView(ListView):
    model = Employee
    template_name = 'kb/user_posts.html' 
    context_object_name = 'employees_list'
    paginate_by = 2

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Employee.objects.filter(author=user).order_by('-date_posted')

class ArticleDetailView(DetailView):
    model = Employee
    template_name = 'kb/post_detail.html'



class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Employee
    fields = ['date_posted','content','file','first_name','last_name','email','phone_number','hire_date','salary','departments','jobs','commission_pct']
    success_url = reverse_lazy('post-create')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Employee
    fields = ['date_posted','content','file','first_name','last_name','email','phone_number','hire_date','salary','departments','jobs','commission_pct']
    success_url = reverse_lazy('post-update')

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Employee
    success_url = 'post-delete'
    template_name = 'kb/post_confirm_delete.html'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False       



