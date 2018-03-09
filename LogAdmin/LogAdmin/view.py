# -*- coding: utf-8 -*-
from django.shortcuts import render,redirect, HttpResponse
from LogAdmin import models
from django.contrib import auth
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import  paramiko
import json
import re,sys
from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
####### User Admin ##########
def login_page(request):
    return render(request, 'LogAdmin/login.html')


#登录跳转
def login_handle(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(username=username,password=password)
    print user
    if user:
        login(request,user)
        project = models.Project.objects.all()
        host = models.Host.objects.all()
        app = models.Application.objects.all()
        if user.is_superuser:
            permission = '管理员'
        else:
            permission = '普通用户'
        return render(request, 'LogAdmin/index.html', {'project': project, 'host': host, 'app': app,'username':username,'permission':permission})
    else:
        return render(request, 'LogAdmin/login.html')

#注册
def ajax_register(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    print username,password
    user = User.objects.create_user(username=username, password=password)
    user.save()
    return HttpResponse('注册成功！')

#注销
def logoutuser(request):
    print 'aaaaaaaaaaaaaaa'
    logout(request)
    return render(request, 'LogAdmin/login.html')



    ############################ Index #################
@login_required
def index_handle(request):
    project = models.Project.objects.all()
    host = models.Host.objects.all()
    app = models.Application.objects.all()
    #     strp = ','.join([str(i['pname']) for i in [pname for pname in i.project.values('pname')]])
    return render(request, 'LogAdmin/index.html', {'project': project, 'host': host, 'app': app})

##############工具函数##############################

#检验ip是否合法
def checkip(ip):
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(ip):
        return True
    else:
        return False

def SearchLog(ip, url, secret):
    pkey = secret
    print pkey
    key = paramiko.RSAKey.from_private_key_file(pkey)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ip, port=22, username="root", pkey=key)

    cmd = 'ls ' + url +'|grep -E *.log$'
    stdin, stdout, stderr = ssh.exec_command(cmd)
    a = []
    for i in stdout:
        a.append(str(i).strip('\n'))
    ssh.close()
    return a

def AwkLog(ip,logpath,secret,concurrency):
    pkey = secret
    key = paramiko.RSAKey.from_private_key_file(pkey)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ip, port=22, username="root", pkey=key)
    cmd="awk '{ print $1,$4}' "+logpath+" |sort -n|uniq -c|awk '$1 > "+concurrency +"'|awk 'NR>1'"
    stdin,stdout,stderr=ssh.exec_command(cmd)
    a=[]
    for i in stdout:
        line=str(i).split()
        dict={'count':line[0],'ip':line[1],'time':line[2].strip('[')}
        a.append(dict)
    print a
    ssh.close()
    return a

def GrepLog(ip,logpath,secret,string,row):
    pkey = secret
    key = paramiko.RSAKey.from_private_key_file(pkey)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ip, port=22, username="root", pkey=key)
    cmd ='tail -'+row+" "+logpath+'|awk '+'\'/'+string+'/\''
    # cmd = "grep "+string+" "+logpath
    print cmd
    stdin,stdout,stderr=ssh.exec_command(cmd)
    a=[]
    for i in stdout:
         a.append('<br>'+str(i).replace(string,"<span class=\"keyword\">"+string+"</span>"))
    ssh.close()
    grepstr=''.join(a)
    print grepstr
    return grepstr


#检验数据是否存在
# def checkdata(model,field,str):
#     try:
#
#         models.model.objects.get(field=str)
#         print 'aaaaaaaaaaa'
#         return True
#     except ObjectDoesNotExist:
#         return False


#检验url是否在该应用上是否存在，不存在返回True
# def checkpath(ip,url):
#      secret=str(models.Host.objects.filter(ip=ip)[0].secret)
#      ip=str(ip )
#      ssh = paramiko.SSHClient()
#      ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#      ssh.connect(ip, 22, "root",secret)
#      cmd = 'cd ' + url
#      print cmd
#      stdin, stdout, stderr = ssh.exec_command(cmd)
#      if stderr.readlines():
#          return True
#      else:
#          return False
#      ssh.close()




#################### ajax ###############

###############用户模块######################
def ajax_addUser(request):
    passwd = str(request.POST.get('password'))
    name = str(request.POST.get('username'))
    permi=request.POST.get('permi')
    print str(permi)
    if User.objects.filter(username=name):
        res='用户已经存在'
    else:
        if permi=='管理员':
            print '管理员创建中'
            User.objects.create_superuser(name,'',passwd)
        else:
            User.objects.create_user(username=name,password=passwd)
        res='添加成功'
    return JsonResponse({'res': res})

def ajax_revUser(request):
    passwd=str(request.POST.get('password'))
    username=str(request.POST.get('username'))
    permi=str(request.POST.get('permi'))
    if permi=='管理员':
        flag=True
    else:
        flag=False
    user=User.objects.get(username=username)
    userid=user.id
    if User.objects.filter(username=username) and not User.objects.filter(id=userid):
        res='修改失败，用户名冲突'
    else:
        print flag
        User.objects.filter(id=userid).update(username=username,is_superuser=flag)
        if passwd:
            user.set_password(passwd)
            user.save()
        res='修改成功'
    return JsonResponse({'res':res})


def ajax_delUser(request):
    username=str(request.POST.get('username'))
    user=User.objects.get(username=username)
    user.delete()
    res='删除成功'
    return JsonResponse({'res':res})


## 修改用户密码
def ajax_revPasswd(request):
    username = str(request.POST.get('username'))
    oldpasswd = str(request.POST.get('oldpasswd'))
    newpasswd = str(request.POST.get('newpasswd'))
    print username, oldpasswd, newpasswd
    userres = authenticate(username=username, password=oldpasswd)
    if userres:
        user=User.objects.get(username=username)
        print ('修改前：'+User.objects.get(username=username).password)
        user.set_password(newpasswd)
        user.save()
        print ('修改后：'+User.objects.get(username=username).password)
    else:
       res = '原密码错误'

    return JsonResponse({'res': res})

##################项目模块############################
def ajax_revPro(request):
    proid=str(request.POST.get('proid'))
    proname=str(request.POST.get('proname'))
    if models.Project.objects.filter(pname=proname) and not models.Project.objects.filter(pname=proname).filter(PID=proid):
        res='项目名冲突!'
    else:
        models.Project.objects.filter(PID=proid).update(pname=proname)
        res='修改成功！'
    return JsonResponse({'res': res})

def ajax_addPro(request):
    proname=str(request.POST.get('proname'))
    print '================='+proname+'=========================='
    if models.Project.objects.filter(pname=proname):
        res='项目名已经存在！'
    else:
        models.Project.objects.create(pname=proname)
        res='添加成功!'
    return JsonResponse({'res': res})

def ajax_delPro(request):
    proid=str(request.POST.get('proid'))
    models.Project.objects.filter(PID=proid).delete()
    res='删除成功!'
    return JsonResponse({'res': res})




########################主机模块#######################
#添加主机
def ajax_addHost(request):
    hostname = str(request.POST.get('hostname'))
    hostip = str(request.POST.get('hostip'))
    hostsecret = str(request.POST.get('hostsecret'))
    if models.Host.objects.filter(ip=hostip):
        res='ip已经存在！'
    elif not checkip(hostip):
        res='ip不合法！'
    elif models.Host.objects.filter(hostname=hostname):
        res='主机名已经存在！'
    else:
        res='添加成功'
        models.Host.objects.create(hostname=hostname, ip=hostip, secret=hostsecret)
    return JsonResponse({'res': res})

#修改主机ip和name
def ajax_revHost(request):
    hostid = str(request.POST.get('hostid'))
    hostname = str(request.POST.get('hostname'))
    hostip = str(request.POST.get('hostip'))
    hostsecret = str (request.POST.get('hostsecret'))
    if models.Host.objects.filter(ip=hostip) and not models.Host.objects.filter(ip=hostip).filter(HID=hostid):  #判断除自己外有无ip冲突
        res = 'ip冲突！'
    else:
        if models.Host.objects.filter(hostname=hostname) and not models.Host.objects.filter(hostname=hostname).filter(HID=hostid):
            res = '主机名冲突!'
        else:
            if checkip(hostip):
                res='修改成功！'
                models.Host.objects.filter(HID=hostid).update(hostname=hostname, ip=hostip,secret=hostsecret)
            else:
                res='ip不合法！'
    return JsonResponse({'res':res})


#删除主机
def ajax_delHost(request):
    hostid=str(request.POST.get('hostid'))
    models.Host.objects.filter(HID=hostid).delete()
    return JsonResponse({'res':'删除成功'})

#刷新
def ajax_refOption(request):
    option=str(request.POST.get('option'))
    if option=='refHost':
        host_result=models.Host.objects.all().values()
        print ('开始转换===========================')
        result=[i for i in host_result]
        for i in result:
            i['HID']=str(i['HID'])
            i['hostname']=str(i['hostname'])
            i['ip']=str(i['ip'])
            i['secret']=str(i['secret'])
            i['hostname']=str(i['hostname'])
    if option=='refApp':
        result=[]
        app_result=models.Application.objects.all().values()
        app=[i for i in app_result]
        for i in app:
           hostname = models.Host.objects.get(HID=i['host_id']).hostname
           pname = models.Project.objects.get(PID=i['project_id']).pname
           tname = models.AppType.objects.get(TID=i['apptype_id']).tname
           dict={}
           dict={'AID':str(i['AID']),'logpath':str(i['logpath']),'aname':str(i['aname']),'hostname':hostname,'pname':pname,'tname':tname}
           result.append(dict)
    if option=='ProTab':
        pname_result=models.Project.objects.values('pname')
        result=[i for i in pname_result]
        for i in result:
            i['pname']=str(i['pname'])
    if option=='refPro':
        pro_result=models.Project.objects.values()
        result=[i for i in pro_result]
        print result
        for i in result:
            i['PID']=str(i['PID'])
            i['pname']=str(i['pname'])
            i['createtime']=str(i['createtime']).split()[0]
        print result
    if option=='refUser':
        user_result=User.objects.values()
        result=[i for i in user_result]
        for i in result:
            i['username']=str(i['username'])
            i['last_login']=str(i['last_login']).split('.')[0]
            if i['is_superuser']:
                i['is_superuser']='管理员'
            else:
                i['is_superuser']='普通用户'
    return JsonResponse({'res':result})


#刷新下拉框
def ajax_getSelect(request):
    host=models.Host.objects.all().values()
    shost=[i for i in host]
    project=models.Project.objects.all().values()
    sproject=[i for i in project]
    apptype=models.AppType.objects.all().values()
    sapptype=[i for i in apptype]
    return JsonResponse({'host':shost,'project':sproject,'apptype':sapptype})

#添加应用判断
def ajax_addApp(request):
    hostname=str(request.POST.get('host'))
    logpath=str(request.POST.get('logpath'))
    pname=request.POST.get('project')
    appname = str(request.POST.get('appname'))
    tname = str(request.POST.get('apptype'))
    appres = models.Application.objects.filter(aname=appname)
    if models.Application.objects.filter(aname=appname):
        res='该应用已经存在!'
    else:
        print pname,hostname,tname
        project = models.Project.objects.get(pname=pname)
        host = models.Host.objects.get(hostname=hostname)
        print 'aaaaaaaaaaaaaaaaaaaa'
        apptype = models.AppType.objects.get(tname=tname)
        models.Application.objects.create(aname=appname,logpath=logpath,project=project,host=host,apptype=apptype)
        res='创建成功'
    return JsonResponse({'res':res})

def ajax_revApp(request):
    appid = str(request.POST.get('appid'))
    appname = str(request.POST.get('appname'))
    hostname = str(request.POST.get('hostname'))
    projectname = str(request.POST.get('project'))
    logpath = str(request.POST.get('logpath'))

    typename = str(request.POST.get('typename'))
    print typename


    if models.Application.objects.filter(aname=appname) and not models.Application.objects.filter(aname=appname).filter(AID=appid):
        res='应用名冲突'
    else:
        host = models.Host.objects.get(hostname=hostname)
        project = models.Project.objects.get(pname=projectname)
        apptype = models.AppType.objects.get(tname=typename)
        app = models.Application.objects.get(AID=appid)
        app.host=host
        app.project=project
        app.aname=appname
        app.logpath=logpath
        app.apptype=apptype
        app.save()
        res='修改成功'
        print appid, appname, hostname, projectname, logpath

    return JsonResponse({'res':res})

#删除应用
def ajax_delApp(request):
    appid=str(request.POST.get('appid'))

    models.Application.objects.filter(AID=appid).delete()
    return JsonResponse({'res':'删除成功'})





######################日志管理模块#####################

###获取日志awk信息
def ajax_refAwk(request):
    aname=request.POST.get('aname')
    logname=request.POST.get('logname')
    counts=request.POST.get('counts')
    app=models.Application.objects.get(aname=aname)
    path=app.logpath+logname

    a=AwkLog(app.host.ip,path,app.host.secret,counts)
    print type(a)
    return JsonResponse({'res':a})




###获取日志控制台信息
def ajax_refLog(request):
    aname = request.POST.get('aname')
    logname=request.POST.get('logname')
    row=request.POST.get('logrow')
    app=models.Application.objects.get(aname=aname)
    pkey =app.host.secret
    ip=app.host.ip
    key = paramiko.RSAKey.from_private_key_file(pkey)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ip, port=22, username="root", pkey=key)
    path=app.logpath+logname
    cmd='tail -'+row+' '+path
    print cmd
    stdin, stdout, stderr = ssh.exec_command(cmd)
    logdetail ='<br>'.join(stdout.readlines())
    ssh.close()
    return JsonResponse({'res':logdetail})


def ajax_grepLog(request):
    aname=request.POST.get('aname')
    logname=request.POST.get('logname')
    keyword=request.POST.get('keyword')
    greprow=request.POST.get('greprow')
    app=models.Application.objects.get(aname=aname)
    path = app.logpath + logname
    a=GrepLog(app.host.ip,path,app.host.secret,keyword,greprow)
    return JsonResponse({'res': a})




#项目跳app
def ajax_showAppul(request):
    pname=request.POST.get('pname')
    project=models.Project.objects.get(pname=pname)
    app_result=project.application_set.values('aname')
    result=[i for i in app_result]
    print result
    for i in result:
        i['aname']=str(i['aname'])
    return JsonResponse({'res': result})


#app跳log
def ajax_showLogul(request):
    aname=request.POST.get('aname')
    print aname
    app=models.Application.objects.get(aname=aname)
    aid=app.AID
    ip=app.host.ip
    secret=app.host.secret
    logpath=app.logpath
    apptype=app.apptype.tname
    print 'aaaaaaaaaaa'
    result=SearchLog(ip,logpath,secret)
    print apptype
    return JsonResponse({'res':result,'aid':aid,'apptype':apptype})

#log跳logDetail
def ajax_showLogDetail(request):
    aid=request.GET.get('aid')
    app=models.Application.objects.get(AID=aid)
    logname=request.GET.get('logname')
    apptype=app.apptype.tname
    print aid

    return render(request, 'LogAdmin/logDetail.html',{'app':app,'logname':logname,'apptype':apptype})














######## LogAdmin##########



    # print '=== 111==='
    # message = request.websocket.wait()
    # while True:
    #     flag=request.websocket.has_messages()
    #     line=stdout.readline()
    #     print message
    #     if line:
    #         line=str(line)
    #         request.websocket.send(line)
    #     if flag :
    #         print ('===================跳出循环===================')
    #         break
