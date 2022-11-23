from datetime import date

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import pandas as pd
from django.template import loader

opcostICE = []
opcostEV = []

@login_required()
def fuelCost(fuelType, urban, suburban, highway, driverType, mileage):
    df = pd.read_excel("compareApp/data files/Petrol diesel data.xlsx")
    cost = 0
    typeOfFuel = ""
    if fuelType == 'Diesel':
        df1 = df.drop(['Petrol'], axis=1)
        typeOfFuel = 'Diesel'
    else:
        df1 = df.drop(['Diesel'], axis=1)
        typeOfFuel = 'Petrol'

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
        cost = cost + (df2[typeOfFuel].iloc[0] * fuelRequired)
        opcostICE.append(cost)
    return cost

@login_required()
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

    for i in range(1, 6):
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

@login_required
def form(request):
    if request.method == "POST":
        df = pd.read_excel("compareApp/data files/ICE_FINAL.xlsx")
        df1 = pd.read_excel("compareApp/data files/EV_FINAL.xlsx")
        urban = int(request.POST['urban'])
        suburban = int(request.POST['suburban'])
        highway = int(request.POST['highway'])

        speedOn = request.POST['avgspddrvr']
        driverType = ""

        if speedOn == 'normal':
            driverType = "normal"
        else:
            driverType = "aggressive"

        capital = request.POST['capital']
        area = request.POST['areas']
        # indexing error aa rha hai bcz hame radio button ki value mein bhi same wahi value daalni hai jo humne label mein daali hai like 4-8 price range
        df2 = df.loc[df['Price Range'] == capital]
        df3 = df1.loc[df1['Price Range'] == capital]

        fuelType = str(df2.iloc[:, 2])
        mileage = int(df2.iloc[:, 3])

        batteryCapacity = int(df2.iloc[:, 3])
        drivingRange = int(df3.iloc[:, 2])

        opCostICE = fuelCost(fuelType, urban, suburban, highway, driverType, mileage)
        opCostEV = chargeCost(urban, suburban, highway, driverType, drivingRange, batteryCapacity)

        stri = str(opCostICE) + "  " + str(opCostEV)
        return HttpResponse(stri)
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
