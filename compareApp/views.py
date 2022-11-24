from datetime import date

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

from django.contrib import messages
import pandas as pd

from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from .forms import NewUserForm

opcostICE = []
opcostEV = []
capitalICE=0
ownershipICE=0
maintainenceICE=0
resaleICE=0
insuranceICE=0
opCostICE1=0

capitalEV=0
ownershipEV=0
maintainenceEV=0
resaleEV=0
insuranceEV=0
opCostEV1=0
drivingRange=0


@login_required()
def fuelCost(fuelType, urban, suburban, highway, driverType, mileage, area):
    cost = 0
    if str(fuelType) == 'Diesel':
        df1 = pd.read_excel('compareApp/data files/Diesel data final.xlsx')
    else:
        df1 = pd.read_excel('compareApp/data files/Petrol diesel data.xlsx')

    ufactor = 0.12
    sfactor = 0.197
    hfactor = 0.169

    if driverType == 'normal':
        afactor = 0
    else:
        afactor = 0.22

    fuelRequiredU = urban / mileage
    fuelRequiredU = fuelRequiredU + (fuelRequiredU) * ufactor
    fuelRequiredSu = suburban / mileage
    fuelRequiredSu = fuelRequiredSu + (fuelRequiredSu) * sfactor
    fuelRequiredH = highway / mileage
    fuelRequiredH = fuelRequiredH + (fuelRequiredH) * hfactor

    fuelRequired = fuelRequiredU + fuelRequiredSu + fuelRequiredH
    fuelRequired = fuelRequired + (fuelRequired) * afactor

    fuelRequired = fuelRequired * 365

    for i in range(0, 6):
        year = 2022 + i
        df2 = df1.loc[df1['Date'] == year]
        if str(area) == 'Delhi':
            cost = cost + (df2['Delhi'].iloc[0] * fuelRequired)
        elif str(area) == 'Mumbai':
            cost = cost + (df2['Mumbai'].iloc[0] * fuelRequired)
        elif str(area) == 'Chennai':
            cost = cost + (df2['Chennai'].iloc[0] * fuelRequired)
        else:
            cost = cost + (df2['Kolkata'].iloc[0] * fuelRequired)
        opcostICE.append(cost)
    return cost


def chargeCost(urban, suburban, highway, driverType, drivingRange, batteryCapacity, area):
    df1 = pd.read_excel("compareApp/data files/Electricity Prices.xlsx")
    cost = 0
    ufactor = 0.12
    sfactor = 0.197
    hfactor = 0.169

    location = ""

    if driverType == 'normal':
        afactor = 0
    else:
        afactor = 0.22

    if str(area) == 'Delhi':
        location = 'Delhi'
    elif str(area) == "Mumbai":
        location = 'Mumbai'
    elif str(area) == 'Chennai':
        location = "Chennai"
    else:
        location = 'Kolkata'

    powerRequiredU = urban * batteryCapacity / drivingRange
    powerRequiredU = powerRequiredU + (powerRequiredU) * ufactor
    powerRequiredSu = suburban * batteryCapacity / drivingRange
    powerRequiredSu = powerRequiredSu + (powerRequiredSu) * sfactor
    powerRequiredH = highway * batteryCapacity / drivingRange
    powerRequiredH = powerRequiredH + (powerRequiredH) * hfactor

    powerRequired = powerRequiredU + powerRequiredSu + powerRequiredH
    powerRequired = powerRequired + (powerRequired) * afactor
    powerRequired = powerRequired * 365

    for i in range(1, 6):
        year = 2022 + i
        df2 = df1.loc[df1['Year'] == year]
        cost = cost + (df2[location].iloc[0] * powerRequired)
        opcostEV.append(cost)
    return cost

costs_ice = [capitalICE, opcostICE, insuranceICE, maintainenceICE, resaleICE]
costs_ev = [capitalEV, opcostEV, insuranceEV, maintainenceEV, resaleEV]

def chargeCost(urban, suburban, highway, driverType, drivingRange, batteryCapacity):
    df1 = pd.read_excel("compareApp/data files/Electricity Prices.xlsx")
    cost = 0
    ufactor = 0.12
    sfactor = 0.197
    hfactor = 0.169

    if driverType == 'normal':
        afactor = 0
    else:
        afactor = 0.22

    powerRequiredU = urban * batteryCapacity / drivingRange
    powerRequiredU = powerRequiredU + (powerRequiredU) * ufactor
    powerRequiredSu = suburban * batteryCapacity / drivingRange
    powerRequiredSu = powerRequiredSu + (powerRequiredSu) * sfactor
    powerRequiredH = highway * batteryCapacity / drivingRange
    powerRequiredH = powerRequiredH + (powerRequiredH) * hfactor

    powerRequired = powerRequiredU + powerRequiredSu + powerRequiredH
    powerRequired = powerRequired + (powerRequired) * afactor
    powerRequired = powerRequired * 365

    for i in range(1, 7):
        year = 2022 + i
        df2 = df1.loc[df1['Year'] == year]
        cost = cost + (df2['Delhi'].iloc[0] * powerRequired)
        opcostEV.append(cost)
    return cost


def index(request):
    year = date.today().year
    context = {
        'year': year
    }
    return render(request, 'compareApp/index.html', context)



def form(request):
    if request.method == "POST":
        # df = pd.read_excel("compareApp/data files/ICE_FINAL.xlsx")
        # df1 = pd.read_excel("compareApp/data files/EV_FINAL.xlsx")
        # urban = int(request.POST['urban'])
        # suburban = int(request.POST['suburban'])
        # highway = int(request.POST['highway'])
        #
        # speedOn = request.POST['avgspddrvr']
        # driverType = ""
        #
        # if speedOn == 'normal':
        #     driverType = "normal"
        # else:
        #     driverType = "aggressive"
        #
        # capital = request.POST['capital']
        # area = request.POST['areas']
        # # indexing error aa rha hai bcz hame radio button ki value mein bhi same wahi value daalni hai jo humne label mein daali hai like 4-8 price range
        # df2 = df.loc[df['Price Range'] == capital]
        # df3 = df1.loc[df1['Price Range'] == capital]
        #
        # fuelType = str(df2.iloc[:, 2])
        # mileage = int(df2.iloc[:, 3])
        # capitalICE=int(df2.iloc[:, 10])
        # maintainenceICE=int(df2.iloc[:, 9])
        # insuranceICE=int(df2.iloc[:, 8])
        # resaleICE=int(df2.iloc[:, 7])
        #
        #
        # batteryCapacity = int(df2.iloc[:, 3])
        # drivingRange = int(df3.iloc[:, 2])
        # capitalEV = int(df2.iloc[:, 10])
        # maintainenceEV = int(df2.iloc[:, 9])
        # insuranceEV = int(df2.iloc[:, 8])
        # resaleEV = int(df2.iloc[:, 7])
        #
        # print(area)
        #
        # opCostICE1 = fuelCost(fuelType, urban, suburban, highway, driverType, mileage, area)
        # opCostEV1 = chargeCost(urban, suburban, highway, driverType, drivingRange, batteryCapacity, area)
        #
        # ownershipEV=capitalEV+maintainenceEV+opCostEV1+insuranceEV-resaleEV
        # ownershipICE=capitalICE+maintainenceICE+opCostICE1+insuranceICE-resaleICE
        #
        # print(opCostICE1)
        # stri = str(opCostICE1) + "  " + str(opCostEV1)
        #
        # lstEV=list(capitalEV, opCostEV1, insuranceEV, maintainenceEV, resaleEV)
        # lstICE=list(capitalICE, opCostICE1, insuranceICE, maintainenceICE, resaleICE)

        # operating_line_plot(opcostICE, opcostEV)
        # cost_break_pie_ev(lstEV)
        # ownership_cost_compare(ownershipICE, ownershipEV)
        # costs_compare_bar(lstICE)
        # ev_efficiency_reduction(drivingRange)
        from .dashboard import graphsPlot
        graphsPlot()
        return render(request, 'compareApp/compare.html')

    else:
        return render(request, 'compareApp/Form.html')

def about(request):
    year = date.today().year
    context = {
        'year': year
    }
    return render(request, 'compareApp/about.html', context)


def signUp(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        myuser = User.objects.create_user(username, email, password)
        myuser.save()
        messages.success(request, " Your account has been successfully created")
        return redirect('home')

    else:
        return HttpResponse("404 - Not found")


def contact(request):
    year = date.today().year
    context = {
        'year': year
    }
    return render(request, 'compareApp/contact.html', context)


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "registration/password_reset_email"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="registration/password_reset.html",
                  context={"password_reset_form": password_reset_form})


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("main:homepage")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="registration/register.html", context={"register_form": form})
