import datetime

from .models import People
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.


from django.http import HttpResponse


def people(request, ic):

    print(ic)
    person = People.objects.get(IcNo=ic)
    return render(request, 'App_Pkob/peopleInfo.html', context={'person': person})


def penghulu(request):
    name = "zhamri che ani"
    village = "Merbok"
    return render(request, 'App_Pkob/Penghulu.html', context={'name': name, 'village': village})


def peopleinfo_report(request):
    i = 0;
    current = datetime.datetime.now().year
    year = (People.objects.values_list('IcNo', flat=True))
    year2 = []
    for yeart in year:

        test = yeart[-4]
        if test == "0":
            print(yeart)
            year2.append(("20" + str(yeart)[:2]).replace(",", ""))
            print(year2)
        elif test == '5' or test == "6" or test == '7':
            year2.append(("19" + str(yeart)[:2]).replace(",", ""))
            print(datetime.datetime.now().month)

    year2[:] = [current - int(getyear) for getyear in year2]
    print(year2);
    people_list = People.objects.all()
    print(people_list);
    return render(request, 'App_Pkob/peopleInfo_report.html', context={'people_list': people_list, 'year2': year2})


def edit(request):
    if request.method == "POST":
        person = People.objects.get(IcNo=request.POST['icNo'])
        person.Phone = request.POST['pNum']
        person.save()
        return redirect('peopleinfo')
    else:
        print("not successfull")


def delete(request, ic):
    print("deleted")
    person = People.objects.get(IcNo=ic)
    person.delete()
    messages.info(request, " Delete " + ic + " successful")
    return redirect('peopleinfo')


def register(request):
    if request.method == 'POST':
        print(request.POST)

        full_name = request.POST['fullname']
        ic = request.POST['icNo']
        phone_num = request.POST['pNum']
        ic[-4]
        value = ic[-4] != '5'
        print(value)


        if People.objects.filter(IcNo=ic).exists():
                messages.info(request, 'Person identity card number already exist in the system')
                return redirect('register')
        elif ic[-4] == '0' or ic[-4] == '5' or ic[-4] == '6' or ic[-4] == '7':
                print("hey1")
                people_ = People.objects.create(IcNo=ic, Name=full_name, Phone=phone_num)
                people_.save()
                return redirect('register')
        else:
                messages.info(request, 'Invalid Ic')
                return redirect('register')
    else:
        return render(request, 'App_Pkob/Register.html')