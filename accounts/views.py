from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm, ResetRequestForm, ResetPwdForm
from .models import UserProfile
from django.contrib import messages
# import logging
import uuid

# Email
from django.core.mail import EmailMultiAlternatives, get_connection
from accounts.models import MailServer, Emails
from django.template import loader


def index(request):
    return render(request, 'index.html', locals())


def my_profile(request):
    return render(request, 'accounts/profile.html', locals())


def sign_up(request):
    # logging.basicConfig(filename=os.path.join(MEDIA_ROOT, 'mail_log'), level=logging.DEBUG)

    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            user = User.objects.create(username=username, password=password, email=email, is_active=False)
            user.set_password(password)
            user.save()
            active_key = username
            token = '{}'.format(uuid.uuid4().hex[:10])
            tprofile, created = UserProfile.objects.get_or_create(user=user, check_code=token)
            if created:
                tprofile.save()
            else:
                err_msg = '該帳號已有啟用碼'
                messages.add_message(request, messages.ERROR, err_msg)
                return redirect('home')

            tmp_server = MailServer.objects.get(id=1)

            conn = get_connection()
            conn.username = tmp_server.m_user  # username
            conn.password = tmp_server.m_password  # password
            conn.host = tmp_server.m_server  # mail server
            conn.open()

            target_mails = []
            # target_mails.append('gyli@mail.fcu.edu.tw')
            target_mails.append(email)
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

            err_msg = '請至註冊信箱：'+email + ' 收信並點選信中連結啟用帳號'
            messages.add_message(request, messages.ERROR, err_msg)
            return redirect('home')
        else:
            err_msg = form.errors
            messages.add_message(request, messages.ERROR, err_msg)
            # messages.get_messages(request)
            return redirect('Register')

    return render(request, 'accounts/register.html', locals())


def sign_in(request):
    # err_msg = ''
    form = LoginForm()
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.user.is_active:
                messages.add_message(request, messages.SUCCESS, '登入成功')
                return redirect('home')
            else:
                logout(request, user)
                messages.add_message(request, messages.INFO, '請前往註冊信箱，並點擊註冊信連結啟用帳號')
        else:
            messages.add_message(request, messages.ERROR, '登入失敗，帳號未啟用或無此帳號')

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
    print(request.POST)
    rform = ResetRequestForm()
    if request.method == "POST":
        print(request.POST['username'])
        try:
            user = User.objects.get(username=request.POST['username'])
            active_key = user.username
            token = '{}'.format(uuid.uuid4().hex[:10])
            if user.is_active:
                tprofile = UserProfile.objects.get(user=user)
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
                err = rform.errors
                messages.add_message(request, messages.ERROR, err)
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
