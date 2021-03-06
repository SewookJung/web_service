import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Count, Q
from django.contrib.auth import authenticate

from datetime import datetime, timedelta
from django.utils import timezone

from member.models import Member
from common.models import Client, Product
from .models import Report
from .forms import ReportForm
from utils.constant import REPORT_PERMISSION_DEFAULT, REPORT_PERMISSION_EXCEPT, REPORT_DEFAULT_ID, REPORT_DEFAULT_SELECT


@login_required
def weekly_main(request, **kwargs):
    if not request.session['member_dept'] in REPORT_PERMISSION_DEFAULT:
        return redirect('weekly_permission')

    else:
        sales = Member.objects.filter(
            Q(dept__regex=r"^사업") | Q(dept="총괄본부") 
            )
        date_now = datetime.now()
        if not kwargs:
            if request.session['member_dept'] in REPORT_PERMISSION_EXCEPT:
                selected_id = REPORT_DEFAULT_ID
                selected_all = REPORT_DEFAULT_SELECT
            else:
                selected_id = request.session['id']
                selected_all = REPORT_DEFAULT_SELECT

        else:
            selected_id = int(kwargs['selected_id'])
            selected_all = int(kwargs['selected_all'])

        # 7은 공용변수로 기술 한다.
        # 가장 최근 날짜 가져오기 (weekday() + 7) / 0:월, .... 6:일요일
        current_week = date_now.weekday()
        last_monday = datetime.now() - timedelta(current_week + 7)
        if selected_all == REPORT_DEFAULT_SELECT:
            reports = Report.objects.values('client_id', 'product_id').filter(
                created_at__range=(last_monday.strftime("%Y-%m-%d 12:00:00"), date_now), member_id=selected_id).distinct()

        else:
            reports = Report.objects.values('client_id', 'product_id').filter(
                member_id=selected_id).distinct()

        clinets_reports_array = []
        for report in reports:
            client_reports = Report.objects.filter(member=selected_id,
                                                   client_id=report['client_id'], product_id=report['product_id']).order_by('-created_at')
            support_items = client_reports.values(
                'id', 'support_comment', 'comments', 'sales_type', 'created_at', 'support_date', 'client_manager')
            rework_client = {'client_id': report['client_id'], 'client_name': client_reports[0].client_name, 'product_name': client_reports[0].product_name, 'product_id': report['product_id'],
                             'support_items': support_items}
            clinets_reports_array.append(rework_client)
        return render(request, 'weekly/weekly_main.html', {"sales": sales, "selected_all": selected_all, "selected_id": selected_id, "last_monday": last_monday, "reports": clinets_reports_array, 'permission': REPORT_PERMISSION_DEFAULT})


@login_required
def weekly_add(request):
    form = ReportForm()
    products = Product.objects.values('id',
                                      'name', 'makers', 'level').order_by('makers', 'level')
    return render(request, 'weekly/weekly_add.html', {"products": products, 'form': form, 'permission': REPORT_PERMISSION_DEFAULT})


@login_required
def weekly_add_apply(request):
    if request.method == "POST":
        try:
            report = Report(client_id=request.POST['client'], member_id=request.session['id'], product_id=request.POST['product_id'], client_manager=request.POST['client_manager'],
                            sales_type=request.POST['sales_type'], support_comment=request.POST['weekly_comments'], support_date=request.POST['report_date'], comments=request.POST['etc_comments'])
            report.save()
            return redirect('weekly_main')
        except:
            pass
        return redirect('weekly_main')


@login_required
def weekly_detail(request, **kwargs):
    client_id = kwargs['client_id']
    product_id = kwargs['product_id']
    selected_id = int(kwargs['selected_id'])
    reports = Report.objects.filter(
        client_id=client_id, product_id=product_id, member_id=selected_id).order_by('-created_at')
    support_items = reports.values('support_comment', 'created_at')
    rework_client = {'client_id': client_id, 'client_name': reports[0].client_name, 'product_name': reports[0].product_name, 'product_id': product_id,
                     'support_items': support_items, 'member_id': selected_id}
    form = ReportForm()
    products = Product.objects.values(
        'id', 'name', 'makers', 'level').order_by('makers', 'level')
    reporter = Member.objects.get(id=selected_id)
    return render(request, 'weekly/weekly_detail.html', {"report": rework_client, "form": form, 'login_id': request.session['id'], 'products': products, 'reporter': reporter, 'permission': REPORT_PERMISSION_DEFAULT})


@login_required
def weekly_detail_apply(request, client_id):

    report = Report(client_id=client_id, member_id=request.session['id'], product_id=request.POST['product'], client_manager=request.POST['client_manager'],
                    sales_type=request.POST['sales_type'], support_comment=request.POST['weekly_comments'], support_date=request.POST['report_date'], comments=request.POST['etc_comments'])
    report.save()
    return redirect('weekly_main')


@login_required
def weekly_report_detail(request, report_id):
    report = Report.objects.get(id=report_id)
    products = Product.objects.values(
        'id', 'name', 'makers', 'level').order_by('makers', 'level')
    form = ReportForm()
    reporter = Member.objects.get(id=report.member_id)
    return render(request, 'weekly/weekly_report_detail.html', {"report": report, "form": form, 'login_id': request.session['id'], 'products': products, 'reporter': reporter, 'permission': REPORT_PERMISSION_DEFAULT})


@login_required
def weekly_report_detail_apply(request, report_id):
    report = Report.objects.get(id=report_id)
    report.client_id = request.POST['client_id']
    report.member_id = request.session['id']
    report.product_id = request.POST['product']
    report.client_manager = request.POST['client_manager']
    report.sales_type = request.POST['sales_type']
    report.support_comment = request.POST['weekly_comments']
    report.support_date = request.POST['report_date']
    report.comments = request.POST['etc_comments']
    report.save()
    return redirect('weekly_main')


@login_required
def weekly_delete(request, pk):
    report = Report.objects.get(pk=pk).delete()
    return redirect("weekly_main")
