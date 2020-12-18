from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from idea.models import Team
# Create your views here.


def index(request):
    return render(request, 'projects/index.html', locals())


def rated_projects(request):
    return render(request, 'projects/rated-projects.html', locals())


@login_required
def judge_list(request):
    if request.user.is_superuser or request.user.judgerprofile.check_judger:
        if request.user.is_superuser:
            target_teams = Team.objects.all().order_by('id')
        else:
            target_teams = Team.objects.filter(team_group=request.user.judgerprofile.judger_group).order_by('id')
        return render(request, 'projects/judge_team_list.html', {'target_teams': target_teams,
                                                                 'coding101_url': request.get_host()})
    else:
        return redirect('home')


@login_required
def judge_detail(request, judge_id):
    if request.user.is_superuser or request.user.judgerprofile.check_judger:
        if request.user.is_superuser:
            id_list = []
            target_teams = Team.objects.all().order_by('id')
            for target in target_teams:
                id_list.append(target.id)
            print(id_list)
            target_team = Team.objects.get(id=judge_id)

        else:
            id_list = []
            target_teams = Team.objects.filter(team_group=request.user.judgerprofile.judger_group).order_by('id')
            for target in target_teams:
                id_list.append(target.id)
            print(id_list)
            target_team = Team.objects.get(team_group=request.user.judgerprofile.judger_group, id=judge_id)

        return render(request, 'projects/judge_team.html', {'files': target_team, 'id_list': id_list})
    else:
        return redirect('home')
