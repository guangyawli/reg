from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm, ResetRequestForm, ResetPwdForm, ResendConfirmForm, AllLeaderForm
from .models import UserProfile
from django.contrib import messages
from projects.models import JudgerProfile
# import logging
import uuid
from idea.models import Team, TeamMember

# Email
from django.core.mail import EmailMultiAlternatives, get_connection
from accounts.models import MailServer, Emails
from django.template import loader


def index(request):
    if request.user.is_authenticated:
        if request.user.judgerprofile.check_judger:
            return redirect('judge_list')
        check_team = Team.objects.filter(leader=request.user)
        if check_team.exists():
            if request.method == "GET":
                target_team = Team.objects.get(leader=request.user)
                target_members = TeamMember.objects.filter(team__team_name=target_team.team_name)
                form = target_team
                real_member_num = target_members.count()
                if real_member_num == 0:
                    messages.add_message(request, messages.INFO, '沒有成員')
            else:
                error_message = 'request.method POST'

        else:
            error_message = '請新增隊伍'
    else:
        return redirect('Login')

    return render(request, 'accounts/account_index.html', locals())


# def my_profile(request):
#     return render(request, 'accounts/profile.html', locals())


def sign_up(request):
    if request.user.is_authenticated:
        return redirect('account_home')
    else:
        messages.add_message(request, messages.ERROR, '已過註冊開放時間')
        return redirect('home')
        # form = RegisterForm()
        # if request.method == "POST":
        #     form = RegisterForm(request.POST)
        #     if form.is_valid():
        #         username = form.cleaned_data['username']
        #         password = form.cleaned_data['password1']
        #         email = form.cleaned_data['email']
        #         user = User.objects.create(username=username, password=password, email=email, is_active=False)
        #         user.set_password(password)
        #         user.save()
        #         active_key = username
        #         token = '{}'.format(uuid.uuid4().hex[:10])
        #         tprofile, created = UserProfile.objects.get_or_create(user=user, check_code=token)
        #         if created:
        #             tprofile.save()
        #         else:
        #             err_msg = '該帳號已有啟用碼'
        #             messages.add_message(request, messages.ERROR, err_msg)
        #             return redirect('home')
        #
        #         tmp_server = MailServer.objects.get(id=1)
        #
        #         conn = get_connection()
        #         conn.username = tmp_server.m_user  # username
        #         conn.password = tmp_server.m_password  # password
        #         conn.host = tmp_server.m_server  # mail server
        #         conn.open()
        #
        #         target_mails = []
        #         # target_mails.append('gyli@mail.fcu.edu.tw')
        #         target_mails.append(email)
        #         # print(target_mails)
        #         # print(courses.course_id)
        #         # logging.debug(str(target_mails) + str(datetime.now()))
        #
        #         test_from = Emails.objects.get(e_status='register_confirm').e_from
        #         test_title = Emails.objects.get(e_status='register_confirm').e_title
        #         # announcement = Emails.objects.get(e_status='default').e_content
        #         context = {
        #             'coding101_url': request.get_host,
        #             'check_token': token,
        #             'active_key': active_key
        #         }
        #         # print(courses.course_name)
        #         email_template_name = 'accounts/mail_register.html'
        #         t = loader.get_template(email_template_name)
        #
        #         mail_list = target_mails
        #
        #         subject, from_email, to = test_title, test_from, mail_list
        #         html_content = t.render(dict(context))  # str(test_content)
        #         # msg = EmailMultiAlternatives(subject, html_content, from_email, bcc=to)
        #         msg = EmailMultiAlternatives(subject, html_content, from_email, to=to)
        #         msg.attach_alternative(html_content, "text/html")
        #         # msg.attach_file(STATIC_ROOT + 'insights_readme.pdf')
        #         conn.send_messages([msg, ])  # send_messages发送邮件
        #
        #         conn.close()
        #
        #         err_msg = '請至註冊信箱：' + email + ' 收信並點選信中連結啟用帳號'
        #         messages.add_message(request, messages.SUCCESS, err_msg)
        #         return redirect('home')
        #     else:
        #         err_msg = [(k, v[0]) for k, v in form.errors.items()]
        #         for i in range(len(err_msg)):
        #             messages.add_message(request, messages.ERROR, err_msg[i][1])
        #         # messages.get_messages(request)
        #         # return redirect('Register')
        #
        # return render(request, 'accounts/register.html', locals())


def sign_in(request):
    if request.user.is_authenticated:
        return redirect('account_home')
    else:
        form = LoginForm()
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if request.user.is_active:
                    messages.add_message(request, messages.SUCCESS, '登入成功')
                    if JudgerProfile.objects.filter(user=request.user):
                        check = JudgerProfile.objects.get(user=request.user)
                        if check.check_judger is True:
                            return redirect('judge_list')
                        else:
                            return redirect('account_home')
                    else:
                        return redirect('account_home')
                # else:
                #     logout(request, user)
                #     messages.add_message(request, messages.INFO, '請前往註冊信箱，並點擊註冊信連結啟用帳號')
                #     messages.add_message(request, messages.WARNING, '或填寫帳號資料重送認證信')
                #     return redirect('resend_active_letter')
            else:
                try:
                    tmpuser = User.objects.get(username=username)
                    if tmpuser.is_active:
                        messages.add_message(request, messages.ERROR, '密碼錯誤')
                    else:
                        messages.add_message(request, messages.ERROR, '帳號未啟用，請至註冊信箱收取認證信')
                    return redirect('Login')
                except User.DoesNotExist:
                    messages.add_message(request, messages.ERROR, '無此帳號')
                    return redirect('Login')

        return render(request, 'accounts/login.html', locals())


def log_out(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, '登出成功')
    return redirect('home')


def activate_user(request, active_key, token):
    # logging.basicConfig(filename=os.path.join("log_files", 'mail_log'), level=logging.DEBUG)
    try:
        user = User.objects.get(username=active_key, userprofile__check_code=token)
    except User.DoesNotExist:
        messages.add_message(request, messages.ERROR, '該帳號不存在，請重新註冊')
        return redirect('Register')
    if user.is_active:
        messages.add_message(request, messages.SUCCESS, '帳號已啟用')
        return redirect('Login')
    else:
        user.is_active = True
        user.save()
        messages.add_message(request, messages.SUCCESS, '啟用成功')
        return redirect('Login')


def request_reset(request):
    rform = ResetRequestForm()
    if request.method == "POST":
        try:
            user = User.objects.get(username=request.POST['username'])
            active_key = user.username
            token = '{}'.format(uuid.uuid4().hex[:10])
            if user.is_active:
                tprofile,cflag = UserProfile.objects.get_or_create(user=user)
                tprofile.check_code = token
                tprofile.save()
                tmp_server = MailServer.objects.get(id=1)
                conn = get_connection()
                conn.username = tmp_server.m_user  # username
                conn.password = tmp_server.m_password  # password
                conn.host = tmp_server.m_server  # mail server
                conn.open()

                target_mails = []
                # target_mails.append('gyli@mail.fcu.edu.tw')
                target_mails.append(user.email)
                # print(target_mails)
                # print(courses.course_id)
                # logging.debug(str(target_mails) + str(datetime.now()))

                test_from = Emails.objects.get(e_status='password_reset').e_from
                test_title = Emails.objects.get(e_status='password_reset').e_title
                # announcement = Emails.objects.get(e_status='default').e_content
                context = {
                    'coding101_url': request.get_host,
                    'check_token': token,
                    'active_key': active_key
                }
                # print(courses.course_name)
                email_template_name = 'accounts/mail_reset_pwd.html'
                t = loader.get_template(email_template_name)

                mail_list = target_mails

                subject, from_email, to = test_title, test_from, mail_list
                html_content = t.render(dict(context))  # str(test_content)
                # msg = EmailMultiAlternatives(subject, html_content, from_email, bcc=to)
                msg = EmailMultiAlternatives(subject, html_content, from_email, to=to)
                msg.attach_alternative(html_content, "text/html")
                # msg.attach_file(STATIC_ROOT + 'insights_readme.pdf')
                conn.send_messages([msg, ])  # send_messages发送邮件

                conn.close()
                messages.add_message(request, messages.INFO, '請前往註冊信箱收取重置連結')
            else:
                messages.add_message(request, messages.INFO, '請先至註冊信箱啟用該帳號')
        except User.DoesNotExist:
            messages.add_message(request, messages.ERROR, '該帳號不存在')

        return redirect('request_reset')

    context = {
        'target': "要求重置密碼",
        'rform': rform
    }

    return render(request, 'accounts/reset_request.html', context)


def reset_user(request, active_key, token):
    # logging.basicConfig(filename=os.path.join("log_files", 'mail_log'), level=logging.DEBUG)
    try:
        user = User.objects.get(username=active_key, userprofile__check_code=token)
        rform = ResetPwdForm(request.POST, instance=user)
        if request.method == "POST":
            if rform.is_valid():
                password = rform.cleaned_data['password1']
                user.set_password(password)
                user.save()
                err_msg = '密碼重置成功'
                messages.add_message(request, messages.SUCCESS, err_msg)
                return redirect('Login')
            else:
                err_msg = [(k, v[0]) for k, v in rform.errors.items()]
                for i in range(len(err_msg)):
                    messages.add_message(request, messages.ERROR, err_msg[i][1])

                return redirect("reset_user", active_key=active_key, token=token)
        else:
            context = {
                'target': "重置密碼",
                'rform': rform
            }
            return render(request, 'accounts/enter_reset.html', context)
    except User.DoesNotExist:
        messages.add_message(request, messages.ERROR, '該帳號不存在')
        return redirect('request_reset')


def resend_active_letter(request):
    if request.method == "POST":
        try:
            user = User.objects.get(username=request.POST['username'])
            active_key = user.username
            if user.is_active:
                messages.add_message(request, messages.ERROR, '該帳號已啟用')
            else:
                token = '{}'.format(uuid.uuid4().hex[:10])
                tprofile, created = UserProfile.objects.get_or_create(user=user)
                tprofile.check_code = token
                tprofile.save()

                tmp_server = MailServer.objects.get(id=1)

                conn = get_connection()
                conn.username = tmp_server.m_user  # username
                conn.password = tmp_server.m_password  # password
                conn.host = tmp_server.m_server  # mail server
                conn.open()

                target_mails = []
                # target_mails.append('gyli@mail.fcu.edu.tw')
                target_mails.append(user.email)
                # print(target_mails)
                # print(courses.course_id)
                # logging.debug(str(target_mails) + str(datetime.now()))

                test_from = Emails.objects.get(e_status='register_confirm').e_from
                test_title = Emails.objects.get(e_status='register_confirm').e_title
                # announcement = Emails.objects.get(e_status='default').e_content
                context = {
                    'coding101_url': request.get_host,
                    'check_token': token,
                    'active_key': active_key
                }
                # print(courses.course_name)
                email_template_name = 'accounts/mail_register.html'
                t = loader.get_template(email_template_name)

                mail_list = target_mails

                subject, from_email, to = test_title, test_from, mail_list
                html_content = t.render(dict(context))  # str(test_content)
                # msg = EmailMultiAlternatives(subject, html_content, from_email, bcc=to)
                msg = EmailMultiAlternatives(subject, html_content, from_email, to=to)
                msg.attach_alternative(html_content, "text/html")
                # msg.attach_file(STATIC_ROOT + 'insights_readme.pdf')
                conn.send_messages([msg, ])  # send_messages发送邮件

                conn.close()

                err_msg = '請至註冊信箱：' + user.email + ' 收信並點選信中連結啟用帳號'
                messages.add_message(request, messages.SUCCESS, err_msg)
                return redirect('home')
        except User.DoesNotExist:
            messages.add_message(request, messages.ERROR, '該帳號不存在')

            return redirect('resend_active_letter')
    else:
        rform = ResendConfirmForm()
        context = {
            'target': "重寄認證信",
            'rform': rform
        }
        return render(request, 'accounts/reset_request.html', context)


def all_leader_mail(request):
    if request.user.is_superuser:
        if request.method == "POST":
            random_code = 'announcement_' + '{}'.format(uuid.uuid4().hex[:5])
            print(request.POST)
            Emails.objects.create(e_title=request.POST['mail_title'], e_content=request.POST['mail_content'],
                                  e_status=random_code, e_team=-1)
            # all_teams = Team.objects.all()

            # smtp information
            tmp_server = MailServer.objects.get(id=1)
            conn = get_connection()
            conn.username = tmp_server.m_user  # username
            conn.password = tmp_server.m_password  # password
            conn.host = tmp_server.m_server  # mail server
            conn.open()

            alluser = User.objects.all()
            target_mails = []
            target_mails.append('gyli@mail.fcu.edu.tw')
            for tleader in alluser:
                target_mails.append(tleader.email)
            # print(test_mails)
            # print(courses.course_id)
            # logging.debug(str(target_mails) + str(datetime.now()))

            test_from = Emails.objects.get(e_status=random_code).e_from
            test_title = Emails.objects.get(e_status=random_code).e_title
            announcement = Emails.objects.get(e_status=random_code).e_content
            context = {
                'coding101_url': request.get_host,
                'announcement': announcement
            }
            # print(courses.course_name)
            email_template_name = 'accounts/mail_leaders.html'
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
            messages.add_message(request, messages.SUCCESS, '寄送成功')

            rform = AllLeaderForm(request.POST)
            context = {
                'target': "通知信",
                'rform': rform,
            }
        else:
            rform = AllLeaderForm()
            context = {
                'target': "公告",
                'rform': rform
            }

        return render(request, 'accounts/leader_mail_request.html', context)