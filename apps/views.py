# -*- coding:utf-8 -*-
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render, render_to_response
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from apps.models import User
from django.db import connection, transaction
import re, urllib, urllib2, time, base64, os
from bs4 import BeautifulSoup
from Crypto.Cipher import AES

def make_secret(id):
    return id[0:2] + "linux for human" + id[2:4] + "hello" + id[4:8] + "ok" + id[8:]

def pad(s):
    return s + (32 - len(s) % 32) * 'c'

def EncodeAES(c, s):
    return base64.b64encode(c.encrypt(pad(s)))

def DecodeAES(c, e):
    return c.decrypt(base64.b64decode(e)).rstrip('c')

def index(request):
    value = dict()
    if not 'user_num' in request.POST:
        return render(request, 'apps/login.html', {})
    else:
        try :
            user = User.objects.get(user_num=request.POST['user_num'])
            secret = make_secret(request.POST['user_num'])
            cipher = AES.new(secret)
        except :
            value['error'] = u'학번이나 패스워드가 잘못되었어요.'
            return render(request, 'apps/login.html', value)

        if DecodeAES(cipher, user.password) == request.POST['password']:
            request.session.set_expiry(300)
            request.session['user_num'] = user.user_num
            request.session['is_delay'] = user.is_delay
            value['flush'] = u'로그인되었습니다.'
        else:
            value['error'] = u'패스워드가 잘못되었어요.'
        return render_to_response('apps/login.html', value, context_instance=RequestContext(request))

def check_usernum(user_id, password):
    check_url = 'https://information.hanyang.ac.kr/ansan/jsp/common/LoginHandlerPortalHanyang.jsp'
    values = {"id":user_id, "password":password, "returnURL":"/ansan/index.jsp", "siteSub":"Y", "failURL":"/ansan/jsp/common/LoginForm.jsp", "gubun":"STU_EMP"}
    param = urllib.urlencode(values)
    request = urllib2.Request(check_url, param)
    response = urllib2.urlopen(request)
    cookie = response.headers.get('Set-Cookie')
    r = response.read()
    soup = BeautifulSoup(r)
    is_hyu_student = False
    if len(soup.find_all("input", {"name":"code"})) == 1:
        is_hyu_student = True
    return is_hyu_student

@transaction.commit_on_success
def join(request):
    if not 'user_num' in request.POST:
        return render(request, 'apps/join.html', {})
    else :
        values = {}
        if len(request.POST['user_num']) != 10 :
            values['error'] = u'학번은 10글자여야 합니다 :('
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", request.POST['mail']):
            values['error'] = u'메일형식이 잘못되었어요 :('
        else:
            cursor = connection.cursor()
            select_query = "select user_num from apps_user where user_num = '%s'" % (request.POST['user_num'])
            cursor.execute(select_query)
            if cursor.fetchone() != None:
                values['error'] = u'이미 가입하셨어요 :)'
            else:
                secret = make_secret(request.POST['user_num'])
                cipher = AES.new(secret)
                if check_usernum(request.POST['user_num'], request.POST['password']):
                    password_encoded = EncodeAES(cipher, request.POST['password'])

                    insert_query = "insert into apps_user(user_num, password, mail, pub_date, is_delay) values('%s', '%s', '%s', '%s', 0)" % (request.POST['user_num'], password_encoded, request.POST['mail'], time.strftime('%Y-%m-%d %X'))
                    cursor.execute(insert_query)
                    values['flash'] = u'회원가입 되었습니다 :)'
                    return render(request, 'apps/login.html', {})
                else:
                    values['error'] = u'학번 혹은 비밀번호를 잘못 입력하셨어요.'
        return render(request, 'apps/join.html', values)

# @login_required()
def logout(request):
    value = dict()
    try:
        del request.session['user_num']
        del request.session['is_delay']
        value['flush'] = u"로그아웃되었습니다"
    except KeyError:
        value['error'] = u"비정상적인 접근입니다. ㅃㅃ"
    return render(request, 'apps/login.html', {})

# @login_required()
@transaction.commit_on_success
def do_delay(request):
    user_num = request.session['user_num']
    cursor = connection.cursor()
    select_query = "select is_delay from apps_user where user_num = '%s'" % (user_num)
    value = {}
    value['flush'] = u'로그인되었습니다.'
    cursor.execute(select_query)
    if cursor.fetchone()[0] == 1:
        do_delay_query = "update apps_user set is_delay = 0 where user_num = '%s'" % (user_num)
        cursor.execute(do_delay_query)
        request.session['is_delay'] = 0
        return render_to_response('apps/login.html', value, context_instance=RequestContext(request))
    else :
        do_delay_query = "update apps_user set is_delay = 1 where user_num = '%s'" % (user_num)
        cursor.execute(do_delay_query)
        request.session['is_delay'] = 1
        return render_to_response('apps/login.html', value, context_instance=RequestContext(request))
