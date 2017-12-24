from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone
import subprocess

from .models import *



def check():
   
    returncode=subprocess.call("python main.py 1>main.dat ",shell=True)
    returncode=subprocess.call("del main.py",shell=True)
    with open("main.dat","r") as f:
        s=""
        for line in f:
            s+=line
    returncode=subprocess.call("del main.dat",shell=True)
    return s
    
class IndexView(generic.ListView):
    template_name = 'testwork/index.html'
    context_object_name = 'latest_problem_list'
    

    def get_queryset(self):
        """
        Return the last five published problems (not including those set to be
        published in the future).
        """
        return Problem.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Problem
    template_name = 'testwork/detail.html'
    def get_queryset(self):
        """
        Excludes any problems that aren't published yet.
        """
        return Problem.objects.filter(pub_date__lte=timezone.now())
"""
def results(request, problem_id):
    response = "You're looking at the results of problem %s."
    return HttpResponse(response % problem_id)
"""

class ResultsView(generic.DetailView):
    model = Problem
    template_name = 'testwork/results.html'
    
"""
def vote(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    try:
        selected_choice = problem.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the problem voting form.
        return render(request, 'testwork/detail.html', {
            'problem': problem,
            'error_message': "You didn't select a choice.",
        })
    else:
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('testwork:results', args=(problem.id,)))
"""


def vote(request,problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    print(type(str(problem.answer_set.get())),type(request.POST["vote"]))
    print(request.POST["vote"])
    
    stra=request.POST["vote"]
    strs=stra.split('\n')
    print(strs)
    f=open("main.py","w")
    f.writelines(strs)
    f.close()
    r=check()
    
    ans = problem.choice_set.get()
    print("r {0}".format(r))
    ans.votes = (str(r)==(str(problem.answer_set.get())+"\n"))
    ans.save()
    return HttpResponseRedirect(reverse('testwork:results', args=(problem.id,)))
    
def toIndex(request,problem_id):
    if request.method == 'POST':
        return HttpResponseRedirect(reverse('testwork:index'))

        