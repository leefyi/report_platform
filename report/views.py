from django.shortcuts import render
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from .models import ReportInfo, ReportDetail, ReportUser
from .serializers import ReportInfoSerializer
from rest_framework.generics import ListCreateAPIView
from django.contrib.auth.decorators import login_required
import json
import datetime
from datetime import timedelta, timezone
import logging
from .echarts import generate_bar, generate_line, generate_pie, generate_river, generate_timecost_line
import sys
# Create your views here.
logger = logging.getLogger(__name__)


def user_login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(
                username=cd['username'],
                password=cd['password'])

            if user:
                login(request, user)
                return render(request, 'home.html')
            else:
                return HttpResponse(
                    'Sorry. Your username or password is not right.')
        else:
            return HttpResponse('Invalid login')
    if request.method == 'GET':
        login_form = LoginForm()
        return render(request, 'login.html', {'form': login_form})


@login_required(login_url='/report/login/')
def user_logout(request):
    logout(request)
    return render(request, 'logout.html')


@login_required(login_url='/report/login/')
def reportDetail(request):
    """测试报告详情列表"""
    info = ReportInfo.objects.all()
    nowt = datetime.datetime.now()
    today = nowt.strftime('%Y-%m-%d')
    tomorrow = (nowt + timedelta(days=1)).strftime('%Y-%m-%d')
    today_info = ReportInfo.objects.filter(
        case_date__gt=today).filter(
        case_date__lt=tomorrow)
    logging.info(today_info)
    names = ['全部', '成功', '失败', '跳过']
    info_list = (info for info in today_info)
    sum = 0
    suc = 0
    fail = 0
    skip = 0
    for s in info_list:
        sum += s.case_sum
        suc += s.case_pass_sum
        fail += s.case_fail_sum
        skip += s.case_skip_sum

    values = [sum, suc, fail, skip]
    generate_bar(names, values)

    all_info = ReportInfo.objects.all().order_by('case_date')
    attr = []
    v = []
    fail_dict = {}
    for item in all_info:
        fmt_date = (item.case_date).strftime('%Y-%m-%d')
        cnt = item.case_fail_sum
        if fmt_date in fail_dict:
            fmt_sum = fail_dict.get(fmt_date)
            fmt_sum += cnt
            fail_dict[fmt_date] = fmt_sum
        else:
            fail_dict[fmt_date] = cnt
    logging.info('dict:', fail_dict)
    for fk, fv in fail_dict.items():
        attr.append(fk)
        v.append(fv)

    generate_line(attr, v)

    return render(request, "report.html",
                  {"report": ReportInfo.objects.order_by("-case_date")})


@login_required(login_url='/report/login/')
def reportMore(request):
    """测试报告更多图标"""
    info_update = ReportInfo.objects.all()
    nowt = datetime.datetime.now()
    today = nowt.strftime('%Y-%m-%d')
    tomorrow = (nowt + timedelta(days=1)).strftime('%Y-%m-%d')
    today_info = ReportInfo.objects.filter(
        case_date__gt=today).filter(
        case_date__lt=tomorrow)
    logging.info(today_info)
    names = ['全部', '成功', '失败', '跳过']
    info_list = (info for info in today_info)
    sum = 0
    suc = 0
    fail = 0
    skip = 0
    for s in info_list:
        sum += s.case_sum
        suc += s.case_pass_sum
        fail += s.case_fail_sum
        skip + +s.case_skip_sum
    values = [sum, suc, fail, skip]
    # 柱状图

    generate_bar(names, values, 1000, 500)
    logging.info('sum: ' + str(sum))

    all_info = ReportInfo.objects.all().order_by('case_date')
    attr = []
    v = []
    fail_dict = {}
    # 要把当日的各种fail case数目加起来
    # dict  日期（YYYY-mm-dd）:数目
    for item in all_info:
        fmt_date = (item.case_date).strftime('%Y-%m-%d')
        cnt = item.case_fail_sum
        if fmt_date in fail_dict:
            fmt_sum = fail_dict.get(fmt_date)
            fmt_sum += cnt
            fail_dict[fmt_date] = fmt_sum
        else:
            fail_dict[fmt_date] = cnt

    for fk, fv in fail_dict.items():
        attr.append(fk)
        v.append(fv)

    # 折线图
    generate_line(attr, v, 1000, 700)

    # 饼状图
    generate_pie(names[1:], values[1:], [50, 75])

    # 河流图
    name = ['Mac', 'Linux', 'Windows']
    data = []
    for info in all_info:
        temp = []
        temp.append(info.case_date)
        temp.append(info.case_fail_sum)
        temp.append(info.platform_name)
        data.append(temp)
    generate_river(name, data)

    return render(request, "more.html")


@login_required(login_url='/report/login/')
def reportCaseInfo(request):
    """
    每个用例详细测试报告信息，包含截图，每步用例步骤耗时
    :param request:
    :return:
    """
    uuid = request.GET.get("id", None)
    logging.info('uuid:', uuid)
    case_name = request.GET.get("case_name", None)
    caseInfo = ReportDetail.objects.filter(report_uuid=uuid,
                                           case_name=case_name)
    caseTime = 0
    for c in caseInfo:
        if c.case_step_time:
            caseTime = c.case_step_time
        else:
            caseTime = 0
    caseHistory = ReportDetail.objects.filter(case_name=case_name).order_by('report_create_time')
    caseVol = {}
    for case in caseHistory:
        if case.report_create_time and case.case_step_time:
            k = case.report_create_time
            ktime = k.strftime('%Y-%m-%d %H:%M:%S')
            logging.info('k:', ktime)
            stime = case.case_step_time
            caseVol[ktime] = stime
    attr = []
    values = []
    for k, v in caseVol.items():
        attr.append(k)
        values.append(v)
    generate_timecost_line(attr, values)
    logging.info('case vol:', list(caseVol.items()))
    return render(request,
                  "reportCaseInfo.html",
                  {"reportCaseInfo": caseInfo[0],
                   "caseTimeAll": caseTime,
                   "caseTimeK": caseVol.keys(),
                   "caseTimeV": caseVol.values()})


@login_required(login_url='/report/login/')
def reportCount(request):
    """
    详细测试报告统计
    :param request:
    :return:
    """
    uuid = request.GET.get("id", None)
    reportInfo = ReportDetail.objects.filter(report_uuid=uuid)
    reportError = ReportDetail.objects.filter(report_uuid=uuid, result='2')
    reportDetails = ReportInfo.objects.filter(report_uuid=uuid)
    phone = set([r.phone_name for r in reportInfo])
    if uuid:
        suc = reportDetails[0].case_pass_sum
        fail = reportDetails[0].case_fail_sum
        skip = reportDetails[0].case_skip_sum
        attr = ['成功', '失败', '跳过']
        v = [suc, fail, skip]

        generate_pie(attr, v, [20, 40])
        return render(request,
                      "reportCount.html",
                      {"reportInfo": reportInfo,
                       "reportError": reportError,
                       "phone": phone,
                       "reportDetail": reportDetails})
    else:
        return render(request, "page_500.html")


class reportInfoListView(ListCreateAPIView):
    """
    测试报告统计信息
    """

    def get_queryset(self):
        queryset = ReportInfo.objects.order_by("-id")[:7][::-1]
        return queryset

    serializer_class = ReportInfoSerializer
