from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from idea.models import Team, TeamMember
from projects.models import TeamScore, JudgerProfile, FinalTeamScore
from projects.forms import JudgeForm, CheckTeamForm
from accounts.forms import OnlyLeaderForm
from django.contrib import messages

import uuid
# Email
from django.core.mail import EmailMultiAlternatives, get_connection
from accounts.models import MailServer, Emails
from django.template import loader


def index(request):
    return render(request, 'projects/index.html', locals())


def rated_projects(request):
    return render(request, 'projects/rated-projects.html', locals())


@login_required
def judge_list(request):
    if request.user.is_superuser or request.user.judgerprofile.check_judger:
        if not JudgerProfile.objects.filter(user=request.user):
            JudgerProfile.objects.get_or_create(user=request.user, judger_realname=request.user.username)

        if request.user.is_superuser:
            target_teams = Team.objects.filter(stu_check=True).exclude(team_group=None).order_by('id')
            # for target_team in target_teams:
            #     target_score = TeamScore.objects.filter(team__team_name=target_team.team_name,
            #                                             judger_name='superuser')
            #     if not target_score:
            #         TeamScore.objects.get_or_create(team=target_team,
            #                                         judger_name='superuser')
        else:
            target_teams = Team.objects.filter(team_group=request.user.judgerprofile.judger_group).order_by('id')
            for target_team in target_teams:
                target_score = TeamScore.objects.filter(team__team_name=target_team.team_name,
                                                        judger_name=request.user.judgerprofile.judger_realname)
                if not target_score:
                    TeamScore.objects.get_or_create(team=target_team,
                                                    judger_name=request.user.judgerprofile.judger_realname)

        return render(request, 'projects/judge_team_list.html', {'target_teams': target_teams,
                                                                 'coding101_url': request.get_host()})
    else:
        return redirect('home')


@login_required
def judge_detail(request, judge_id):
    if request.user.is_superuser or request.user.judgerprofile.check_judger:
        id_list = []
        target_teams = Team.objects.filter(team_group=request.user.judgerprofile.judger_group).order_by('id')
        for target in target_teams:
            id_list.append(target.id)
        target_team = Team.objects.get(id=judge_id)
        # target_score = TeamScore.objects.filter(team__team_name=target_team.team_name,
        #                                         judger_name=request.user.judgerprofile.judger_realname)
        # if not target_score:
        #     TeamScore.objects.get_or_create(team=target_team,
        #                                     judger_name=request.user.judgerprofile.judger_realname)
        #     target_score = TeamScore.objects.filter(team__team_name=target_team.team_name,
        #                                             judger_name=request.user.judgerprofile.judger_realname)
        if request.user.is_superuser:
            target_score = TeamScore.objects.filter(team__team_name=target_team.team_name)
            target_members = TeamMember.objects.filter(team=target_team)
            if request.method == "POST":
                judge = JudgeForm(request.POST, instance=target_score[0])
                stu_check = CheckTeamForm(request.POST, instance=target_team)
                mail_leader_form = OnlyLeaderForm(request.POST)
                if judge.is_valid():
                    judge.save()
                    total_team = TeamScore.objects.get(team__team_name=target_team.team_name,
                                                       judger_name='superuser')
                    total_team.total_score = total_team.score_applicability + total_team.score_creativity \
                                             + total_team.score_challenge + total_team.score_completion
                    total_team.judger_name = 'superuser'
                    total_team.save()
                else:
                    err_msg = [(k, v[0]) for k, v in judge.errors.items()]
                    for i in range(len(err_msg)):
                        messages.add_message(request, messages.ERROR, err_msg[i][1])

                if stu_check.is_valid():
                    stu_check.save()
                    messages.add_message(request, messages.SUCCESS, '儲存成功')

                if mail_leader_form.is_valid() and request.POST['mail_content2']:
                    random_code = 'inform_' + '{}'.format(uuid.uuid4().hex[:5])
                    Emails.objects.create(e_title=request.POST['mail_title2'], e_team=judge_id,
                                                       e_content=request.POST['mail_content2'], e_status=random_code)

                    # smtp information
                    tmp_server = MailServer.objects.get(id=1)
                    conn = get_connection()
                    conn.username = tmp_server.m_user  # username
                    conn.password = tmp_server.m_password  # password
                    conn.host = tmp_server.m_server  # mail server
                    conn.open()

                    target_mails = []
                    target_mails.append('gyli@mail.fcu.edu.tw')
                    target_mails.append(target_members[0].email_addr)

                    test_from = Emails.objects.get(e_status=random_code).e_from
                    test_title = Emails.objects.get(e_status=random_code).e_title
                    announcement = Emails.objects.get(e_status=random_code).e_content
                    context = {
                        'coding101_url': request.get_host,
                        'announcement': announcement
                    }

                    email_template_name = 'projects/mail_only_leader.html'
                    t = loader.get_template(email_template_name)

                    mail_list = target_mails

                    subject, from_email, to = test_title, test_from, mail_list
                    html_content = t.render(dict(context))  # str(test_content)
                    msg = EmailMultiAlternatives(subject, html_content, from_email, bcc=to)
                    # msg = EmailMultiAlternatives(subject, html_content, from_email, to=to)
                    msg.attach_alternative(html_content, "text/html")
                    # msg.attach_file(STATIC_ROOT + 'insights_readme.pdf')
                    conn.send_messages([msg, ])  # send_messages发送邮件

                    conn.close()

                return redirect('judge_detail', str(judge_id))
            else:
                mail_leader_form = OnlyLeaderForm()
                judge = JudgeForm(instance=target_score[0])
                stu_check = CheckTeamForm(instance=target_team)
        else:
            target_score = TeamScore.objects.filter(team__team_name=target_team.team_name,
                                                    judger_name=request.user.judgerprofile.judger_realname)
            if request.method == "POST":
                judge = JudgeForm(request.POST, instance=target_score[0])
                if judge.is_valid():
                    judge.save()
                    messages.add_message(request, messages.SUCCESS, '儲存成功')
                    total_team = TeamScore.objects.get(team__team_name=target_team.team_name,
                                                       judger_name=request.user.judgerprofile.judger_realname)
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
            last_mails = Emails.objects.filter(e_team=judge_id)

            if last_mails:
                return render(request, 'projects/judge_team.html', {'files': target_team, 'id_list': id_list,
                                                                    'coding101_url': request.get_host(),
                                                                    'judge': judge,
                                                                    'stu_check': stu_check,
                                                                    'target_members': target_members,
                                                                    'mail_leader_form': mail_leader_form,
                                                                    'last_mails': last_mails})
            else:
                return render(request, 'projects/judge_team.html', {'files': target_team, 'id_list': id_list,
                                                                    'coding101_url': request.get_host(),
                                                                    'judge': judge,
                                                                    'stu_check': stu_check,
                                                                    'target_members': target_members,
                                                                    'mail_leader_form': mail_leader_form})

        else:
            return render(request, 'projects/judge_team.html', {'files': target_team, 'id_list': id_list,
                                                                'coding101_url': request.get_host(),
                                                                'judge': judge,
                                                                'stu_check': stu_check})

    else:
        return redirect('home')


@login_required
def super_list(request):
    if request.user.is_superuser:
        if not JudgerProfile.objects.filter(user=request.user):
            JudgerProfile.objects.get_or_create(user=request.user, judger_realname=request.user.username)
        wrong_ids = []
        target_teams = Team.objects.filter(stu_check=True).exclude(team_group=None).order_by('id')
        for target_team in target_teams:
            target_final, cflag = FinalTeamScore.objects.get_or_create(team=target_team)
            score_data = TeamScore.objects.filter(team=target_team)

            if score_data.count() == 2:
                target_final.score_applicability = ((float(score_data[0].score_applicability) +
                                                    float(score_data[1].score_applicability)) / 2)
                target_final.score_creativity = ((float(score_data[0].score_creativity) +
                                                 float(score_data[1].score_creativity)) / 2)
                target_final.score_challenge = ((float(score_data[0].score_challenge) +
                                                float(score_data[1].score_challenge)) / 2)
                target_final.score_completion = ((float(score_data[0].score_completion) +
                                                 float(score_data[1].score_completion)) / 2)
                target_final.total_score = target_final.score_applicability+target_final.score_creativity + \
                                           target_final.score_challenge+target_final.score_completion
                target_final.save()
            elif score_data.count() == 0:
                wrong_ids.append(target_team.team_name)
        # print(wrong_ids)
        # if wrong_ids:
        #     messages.add_message(request, messages.ERROR, wrong_ids)
        final_teams = FinalTeamScore.objects.all()
        return render(request, 'projects/super_team_list.html', {'target_teams': final_teams,
                                                                 'coding101_url': request.get_host(),
                                                                 'wrong_ids': wrong_ids})
    else:
        return redirect('home')

