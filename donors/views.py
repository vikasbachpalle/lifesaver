from django.shortcuts import render, redirect
from .models import Donor
from django.contrib import messages

def home_redirect(req):
    return redirect('registerdonor')

def registerdonor(req):
    if req.method == 'POST':
        try:
            a = int(req.POST.get('donorid'))
        except:
            messages.error(req, "Enter valid numeric Donor ID")
            return render(req, 'registerdonor.html')

        b = req.POST.get('name')
        c = req.POST.get('password')
        d = req.POST.get('bloodgroup')
        e = req.POST.get('place')
        f = req.POST.get('phno')

        if not (a and b and c and d and e and f):
            messages.error(req, "Please fill all fields")
            return render(req, 'registerdonor.html')

        # check duplicate id
        if Donor.objects.filter(donorid=a).exists():
            messages.error(req, "Donor ID already exists")
            return render(req, 'registerdonor.html')

        d1 = Donor(donorid=a, name=b, password=c, bloodgroup=d, place=e, phno=f)
        d1.save()
        messages.success(req, "Registered Successfully")
        return render(req, 'registerdonor.html', {'message': 'Registered Successfully'})

    return render(req, 'registerdonor.html')


def searchdonor(req):
    data = []
    if req.method == 'POST':
        bg = req.POST.get('bloodgroup')
        if bg:
            data = Donor.objects.filter(bloodgroup__iexact=bg)
    return render(req, 'searchdonor.html', {'data': data})


def donors_list(req):
    # recent 10 donors
    data = Donor.objects.all().order_by('-created_at')[:50]
    return render(req, 'donors_list.html', {'data': data})


def donor_login(req):
    if req.method == 'POST':
        try:
            did = int(req.POST.get('donorid'))
        except:
            messages.error(req, "Invalid ID")
            return render(req, 'login.html')

        pwd = req.POST.get('password')
        try:
            d = Donor.objects.get(donorid=did)
            if d.password == pwd:
                # set session
                req.session['donorid'] = d.donorid
                req.session['donorname'] = d.name
                return redirect('profile')
            else:
                messages.error(req, "Wrong password")
        except Donor.DoesNotExist:
            messages.error(req, "Donor not found")

    return render(req, 'login.html')


def donor_logout(req):
    try:
        del req.session['donorid']
        del req.session['donorname']
    except:
        pass
    return redirect('donor_login')


def profile(req):
    donorid = req.session.get('donorid')
    if not donorid:
        return redirect('donor_login')

    try:
        d = Donor.objects.get(donorid=donorid)
    except Donor.DoesNotExist:
        return redirect('donor_login')

    return render(req, 'profile.html', {'d': d})


def update_profile(req):
    donorid = req.session.get('donorid')
    if not donorid:
        return redirect('donor_login')

    d = Donor.objects.get(donorid=donorid)

    if req.method == 'POST':
        d.name = req.POST.get('name')
        d.bloodgroup = req.POST.get('bloodgroup')
        d.place = req.POST.get('place')
        d.phno = req.POST.get('phno')
        # password change optional
        pwd = req.POST.get('password')
        if pwd:
            d.password = pwd
        d.save()
        messages.success(req, "Profile updated")
        return redirect('profile')

    return render(req, 'update_profile.html', {'d': d})
