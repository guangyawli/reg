from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from idea.models import Team, TeamMember
from projects.models import TeamScore, JudgerProfile
from projects.forms import JudgeForm, CheckTeamForm
from django.contrib import messages
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

        for target_team in target_teams:
            target_score = TeamScore.objects.filter(team__team_name=target_team.team_name)
            if not target_score:
                TeamScore.objects.get_or_create(team=target_team)

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
            target_team = Team.objects.get(id=judge_id)
            target_score = TeamScore.objects.filter(team__team_name=target_team.team_name)
            target_members = TeamMember.objects.filter(team=target_team)
            if not target_score:
                create_score, cflag = TeamScore.objects.get_or_create(team=target_team)
                target_score = TeamScore.objects.filter(team__team_name=target_team.team_name)
            if request.method == "POST":
                judge = JudgeForm(request.POST, instance=target_score[0])
                stu_check = CheckTeamForm(request.POST, instance=target_team)
                if judge.is_valid():
                    judge.save()
                    total_team = TeamScore.objects.get(team__team_name=target_team.team_name)
                    total_team.total_score = total_team.score_applicability + total_team.score_creativity \
                                             + total_team.score_challenge + total_team.score_completion
                    total_team.judger_name = request.user.judgerprofile.judger_realname
                    total_team.save()
                else:
                    err_msg = [(k, v[0]) for k, v in judge.errors.items()]
                    for i in range(len(err_msg)):
                        messages.add_message(request, messages.ERROR, err_msg[i][1])

                if stu_check.is_valid():
                    stu_check.save()
                    messages.add_message(request, messages.SUCCESS, '儲存成功')

                return redirect('judge_detail', str(judge_id))
            else:
                judge = JudgeForm(instance=target_score[0])
                stu_check = CheckTeamForm(instance=target_team)
        else:
            id_list = []
            target_teams = Team.objects.filter(team_group=request.user.judgerprofile.judger_group).order_by('id')
            for target in target_teams:
                id_list.append(target.id)
            target_team = Team.objects.get(team_group=request.user.judgerprofile.judger_group, id=judge_id)
            target_score = TeamScore.objects.filter(team__team_name=target_team.team_name)
            if not target_score:
                create_score, cflag = TeamScore.objects.get_or_create(team=target_team)
                target_score = TeamScore.objects.filter(team__team_name=target_team.team_name)
            if request.method == "POST":
                judge = JudgeForm(request.POST, instance=target_score[0])
                if judge.is_valid():
                    judge.save()
                    messages.add_message(request, messages.SUCCESS, '儲存成功')
                    total_team = TeamScore.objects.get(team__team_name=target_team.team_name)
                    total_team.total_score = total_team.score_applicability + total_team.score_creativity \
                                             + total_team.score_challenge + total_team.score_completion
                    total_team.judger_name = request.user.judgerprofile.judger_realname
                    total_team.save()
                else:
                    err_msg = [(k, v[0]) for k, v in judge.errors.items()]
                    for i in range(len(err_msg)):
                        messages.add_message(request, messages.ERROR, err_msg[i][1])

                    return redirect('judge_detail', str(judge_id))
            else:
                judge = JudgeForm(instance=target_score[0])
            stu_check = CheckTeamForm(instance=target_team)
        if request.user.is_superuser:
            return render(request, 'projects/judge_team.html', {'files': target_team, 'id_list': id_list,
                                                                'coding101_url': request.get_host(),
                                                                'judge': judge,
                                                                'stu_check': stu_check,
                                                                'target_members': target_members})
        else:
            return render(request, 'projects/judge_team.html', {'files': target_team, 'id_list': id_list,
                                                                'coding101_url': request.get_host(),
                                                                'judge': judge,
                                                                'stu_check': stu_check})

    else:
        return redirect('home')
