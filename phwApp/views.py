from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate
from django.db.models import Q
from datetime import datetime
# Create your views here.

def home(request):
    return render(request, "index.html")

def login(request):
    if request.POST:
        uname = request.POST["uname"]
        pwd = request.POST["pass"]
        user = authenticate(username=uname, password=pwd)
        if user is None:
            messages.info(request, 'Username or password is incorrect')
        else:
            userdata = User.objects.get(username=uname)
            if userdata.is_superuser == 1:
                return redirect("/adminhome")
            elif userdata.is_staff == 1:
                request.session["email"]=uname
                if userdata.first_name == 'Doctor':
                    r = Doctor.objects.get(email=uname)
                    request.session["id"]=r.id
                    request.session["name"]=r.name
                    return redirect("/dochome")
                else:
                    r = Expert.objects.get(email=uname)
                    request.session["id"]=r.id
                    request.session["name"]=r.name
                    return redirect("/experthome")
            else:
                request.session["email"] = uname
                r = Registration.objects.get(email=uname)
                request.session["id"] = r.id
                request.session["name"] = r.name
                return redirect("/userhome")

    return render(request, "login.html")


def registration(request):
    if request.POST:
        name = request.POST["name"]
        email = request.POST["email"]
        age = request.POST["age"]
        gender = request.POST["gender"]
        pwd = request.POST["psw"]
        print(email)
        user = User.objects.filter(username=email).exists()
        print(user)
        if not user:
            try:

                u = User.objects.create_user(
                    username=email, password=pwd, is_superuser=0, is_active=1, is_staff=0, email=email)
                u.save()
                r = Registration.objects.create(
                    name=name, email=email, password=pwd, user=u,age=age,gender=gender)
                r.save()
            except:
                messages.info(request, 'Sorry some error occured')
            else:
                messages.info(request, "Registration Succesful")
        else:
            messages.info(request, 'User already registered')
    return render(request, "registration.html")

def docreg(request):
    if request.POST:
        name = request.POST['name']
        address = request.POST['address']
        phone = request.POST['phone']
        qual = request.FILES['qual']
        exp = request.POST['exp']
        email = request.POST['email']
        specialization = request.POST['specialization']
        pwd = request.POST['psw']
        user = authenticate(username=email, password=pwd)
        if user is None:
            try:
                u = User.objects.create_user(
                        password=pwd, username=email,first_name="Doctor",is_active=0,is_staff=1)
                u.save()
                r = Doctor.objects.create(
                    name=name, address=address, phone=phone, email=email, qualification=qual, experience=exp,user=u,specialization=specialization)
                r.save()
            except:
                messages.info(request, 'Sorry some error occured')
        else:
            messages.info(request, 'User registered')
    data = Doctor.objects.filter(user__is_active=True)
    return render(request, 'docreg.html', {"data": data})


def adminhome(request):
    return render(request, "adminhome.html")

def adminUsers(request):
    data = Registration.objects.all().order_by("-id")
    return render(request, "adminUsers.html", {"data": data})

def adminExpert(request):
    data = Expert.objects.filter(user__is_active=1).order_by("-id")
    dataIn = Expert.objects.filter(user__is_active=0)
    return render(request, "adminExpert.html", {"data": data, "dataIn":dataIn})

def adminUpdateExpert(request):
    id = request.GET['id']
    status = request.GET['status']
    user = User.objects.get(id=id)
    user.is_active = status
    user.save()
    return redirect("/adminExpert")

def adminDoctors(request):
    data = Doctor.objects.filter(user__is_active=1).order_by("-id")
    dataIn = Doctor.objects.filter(user__is_active=0)
    return render(request, "adminDoctors.html", {"data": data, "dataIn":dataIn})

def adminUpdateDoctors(request):
    id = request.GET['id']
    status = request.GET['status']
    user = User.objects.get(id=id)
    user.is_active = status
    user.save()
    return redirect("/adminDoctors")

def adminBlogs(request):
    data = Blogs.objects.all().order_by("-id")
    if "search" in request.POST:
        search = request.POST['search']
        data = Blogs.objects.filter(Q(title__contains=search) | Q(desc__contains=search)).order_by("-id")
    return render(request,"adminBlogs.html", {"data":data})

def adminViewBlog(request):
    id = request.GET['post']
    data = Blogs.objects.get(id=id)
    comments = Comments.objects.filter(blog=id)
    return render(request,"adminViewBlog.html", {"data":data, "comments": comments})

def adminDeleteBlog(request):
    id = request.GET['id']
    data = Blogs.objects.get(id=id)
    data.delete()
    return redirect("/adminBlogs")

def adminReports(request):
    data = Booking.objects.filter()
    data2 = Booking.objects.filter(status='Paid')
    count2 = len(data2)
    total = count2 * 500
    total = f"Rs.{total}/-"
    if request.POST:
        sDate = request.POST['sDate']
        eDate = request.POST['eDate']
        doc = request.POST['doc']
        status = request.POST['status']
        data = Booking.objects.filter(Q(bookeddate__range=(sDate, eDate)) & Q(docid__name__contains=doc) & Q(status__contains=status) )
        flag = False
        for d in data:
            if d.status == 'Paid':
                flag = True
        if status == 'Paid' or flag:
            count = len(data)
            total = count * 500
            total = f"Rs.{total}/-"
        else:
            total = "-"
    return render(request,"adminReports.html", {"data":data, "total":total})

def experthome(request):
    name = request.session["name"]
    return render(request,"experthome.html", {"name":name})

def expreg(request):
    if request.POST:
        name=request.POST["name"]
        con=request.POST["con"]
        email=request.POST["email"]
        add=request.POST["add"]
        psw=request.POST["psw"]
        lic=request.FILES["lic"]
        user=Registration.objects.filter(email=email).exists()
        if user:
            messages.info(request,"User already exists")
        else:
            try:
                u=User.objects.create_user(username=email,email=email,password=psw,is_staff=True,is_active=0)
                u.save()
            except Exception as e:
                messages.info(request,e)
            else:
                try:
                    s=Expert.objects.create(name=name,con=con,email=email,psw=psw,lic=lic,add=add,user=u)
                    s.save()
                except Exception as e:
                    messages.info(request,e)
                else:
                    messages.info(request,"Registered successfully")
    return render(request,"expertreg.html")

def expertVideo(request):
    uid=request.session["id"]
    expert = Expert.objects.get(id=uid)
    if request.POST:
        name=request.POST["uname"]
        ing=request.FILES["file"]
    
        user=Videos.objects.filter(title=name).exists()
        if user:
            messages.info(request,"Video already exists")
        else:
            try:
                u=Videos.objects.create(title=name,file=ing,expert=expert)
                u.save()
            except Exception as e:
                messages.info(request,e)
            else:
                messages.info(request,"Added successfully")
    dta=Videos.objects.filter(expert=expert)
    return render(request,"expertVideo.html",{"dta":dta})

def expertTips(request):
    uid=request.session["id"]
    expert = Expert.objects.get(id=uid)  
    if request.POST:
        name=request.POST["uname"]
        desc=request.POST["desc"]
        try:
            u=Tips.objects.create(title=name,desc=desc,expert=expert)
            u.save()
        except Exception as e:
            messages.info(request,e)
        else:
            messages.info(request,"Added successfully")
    dta=Tips.objects.filter(expert=expert)
    return render(request,"expertTips.html",{"dta":dta})

def expertRemoveVideo(request):
    id = request.GET['id']
    vid = Videos.objects.get(id=id)
    vid.delete()
    return redirect("/expertVideo")

def expertRemoveTips(request):
    id = request.GET['id']
    vid = Tips.objects.get(id=id)
    vid.delete()
    return redirect("/expertTips")

def expertblogs(request):
    uid = request.session['id']
    user = Expert.objects.get(id=uid)
    data = Blogs.objects.exclude(expert=uid).order_by("-id")
    if 'title' in request.POST:
        title = request.POST['title']
        desc = request.POST['desc']
        ins = Blogs.objects.create(expert=user,title=title,desc=desc)
        ins.save()
    if "search" in request.POST:
        search = request.POST['search']
        data = Blogs.objects.filter(Q(title__contains=search) | Q(desc__contains=search)).exclude(expert=uid).order_by("-id")
    return render(request,"expertblogs.html", {"data":data})

def expertviewblog(request):
    uid = request.session['id']
    user = Expert.objects.get(id=uid)
    id = request.GET['post']
    data = Blogs.objects.get(id=id)
    if request.method == "POST":
        comment = request.POST['comment']
        db = Comments.objects.create(comment=comment, blog=data, expert=user)
        db.save()
        
    comments = Comments.objects.filter(blog=id)
    return render(request,"expertviewblog.html", {"data":data, "comments": comments})


def expertChats(request):
    uid = request.session["id"]
    chats = Chat.objects.filter(expert=uid).values("user")
    s = set()
    for c in chats:
        s.add(c['user'])
    print(s)
    ops = Registration.objects.filter(user__is_active=1)
    return render(request, "expertChats.html", {"s":s,"ops":ops})

def expertChat(request):
    uid = request.session["id"]
    eid = request.GET['id']
    do = Registration.objects.get(id=eid)
    url = request.GET['url']
    op = Expert.objects.get(id=uid)
    if request.method == "POST":
        msg = request.POST['msg']
        db = Chat.objects.create(expert=op, user=do, message=msg, sendby='Expert')
        db.save()
    messages = Chat.objects.filter(expert=op, user=do)
    return render(request, "expertChat.html", {"messages":messages, "url":url})
























def userhome(request):
    name = request.session['name']
    uid = request.session["id"]
    user = Registration.objects.get(id=uid)
    data = ''
    fjs = ''
    wjs = ''
    sjs = ''
    reqCal = ''
    age = ''
    if Request.objects.filter(user__id=uid).exists():
        data=Request.objects.filter(user__id=uid).order_by("-id")[0]
        reqCal = int(data.reqCal)
        age = int(user.age)
        fjs = FoodJournals.objects.filter(user=user).order_by("-id")
        wjs = WorkoutJournals.objects.filter(user=user).order_by("-id")
        sjs = SleepJournals.objects.filter(user=user).order_by("-id")
    return render(request, "userhome.html",{"name":name,"fjs":fjs, "wjs":wjs,"sjs":sjs, "reqCal":reqCal, "age":age})

def userreq(request):
    uid = request.session["id"]
    user = Registration.objects.get(id=uid)
    gender = user.gender
    age = user.age
    if request.POST:
        height = int(request.POST['height'])
        weight = int(request.POST['weight'])
        goal = request.POST['goal']
        healthStatus = request.POST['healthStatus']
        activeStatus = request.POST['activeStatus']
        heightMeter = height / 100
        bmi = weight / (heightMeter ** 2)
        bmi = round(bmi,2)
        print("BMI: ", bmi)

        bmr = 0
        if gender == 'Male':
            bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        else:
            bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
        bmr = round(bmr, 2)
        print("BMR: ", bmr)

        calorie = 0

        if activeStatus == "Moderately active (3-5 days/week)":
            calorie = int(bmr * 1.55)
        elif activeStatus == "Very active (6-7 days/week)":
            calorie = int(bmr * 1.725)
        elif activeStatus == "Super active (twice/day)":
            calorie = int(bmr * 1.9)
        print(calorie)
        
        reqCal = 0
        if goal == 'Weight Loss':
            reqCal = calorie - 500
        elif goal == 'Weight Gain':
            reqCal = calorie + 500
        else:
            reqCal = calorie + 500
        print("Required Calorie:", reqCal)
        data = Request.objects.create(user=user,height=height,weight=weight,healthstat=healthStatus,bmi=bmi,bmr=bmr,goal=goal,activeStatus=activeStatus,reqCal=reqCal)
        data.save()
        return redirect("/userviewreq")
    return render(request, "userreq.html")

def userviewreq(request):
    uid=request.session["id"]
    data=Request.objects.filter(user__id=uid).order_by("-id")
    return render(request,"userviewreq.html",{"data":data})

def userexercise(request):
    data=Videos.objects.all()
    return render(request,"userexercise.html",{"data":data})

def userTips(request):
    data=Tips.objects.all()
    return render(request,"userTips.html",{"data":data})

def userjournal(request):
    return render(request,"userjournal.html")

def userfj(request):
    uid=request.session["id"]
    user = Registration.objects.get(id=uid)
    req = 0
    reqCal = 0
    if Request.objects.filter(user=user).exists():
        req = Request.objects.filter(user=user).order_by("-id")[0]
        reqCal = int(req.reqCal)
    
    if request.POST:
        calorie = int(request.POST['calorie'])
        current_date = datetime.now().date()
        if FoodJournals.objects.filter(date=current_date,user=user).exists():
            fj = FoodJournals.objects.get(date=current_date,user=user)
            dayCal = int(fj.calorieIntake)
            tCal = dayCal + calorie
            if reqCal >= tCal:
                status = "Calorie in control"
            else:
                status = "Calorie exceeded"
            fj.calorieIntake = tCal
            fj.status = status
            fj.save()
        else:
            if reqCal >= calorie:
                status = "Calorie in control" 
            else:
                status = "Calorie exceeded"
            fj = FoodJournals.objects.create(user=user,calorieIntake=calorie,status=status)
            fj.save()
    data = FoodJournals.objects.filter(user=user).order_by("-id")
    return render(request,"userfj.html",{"data":data})

def userwj(request):
    uid=request.session["id"]
    user = Registration.objects.get(id=uid)
    if request.POST:
        duration = request.POST['duration']
        workouts = request.POST['workouts']
        wk = WorkoutJournals.objects.create(user=user,workouts=workouts,duration=duration)
        wk.save()
    data = WorkoutJournals.objects.filter(user=user).order_by("-id")
    return render(request,"userwj.html",{"data":data})

def usersj(request):
    uid=request.session["id"]
    user = Registration.objects.get(id=uid)
    age = int(user.age)
    print(age)
    if request.POST:
        duration = int(request.POST['duration'])
        current_date = datetime.now().date()
        if SleepJournals.objects.filter(date=current_date,user=user).exists():
            sj = SleepJournals.objects.get(date=current_date,user=user)
            cuDur = int(sj.duration)
            totalDuration = cuDur + duration
            if age > 6 and 12 >= age:
                if totalDuration >= 9 and totalDuration <= 12:
                    status = "Adequate Sleep"
                else:
                    status = "Improper Sleep"
            elif age > 13 and 18 >= age:
                if totalDuration >= 8 and totalDuration <= 10:
                    status = "Adequate Sleep"
                else:
                    status = "Improper Sleep"
            elif age > 18 and 64 >= age:
                if totalDuration >= 7 and totalDuration <= 9:
                    status = "Adequate Sleep"
                else:
                    status = "Improper Sleep"
            elif age > 65:
                if totalDuration >= 7 and totalDuration <= 8:
                    status = "Adequate Sleep"
                else:
                    status = "Improper Sleep"
            else:
                if totalDuration >= 12 and totalDuration <= 16:
                    status = "Adequate Sleep"
                else:
                    status = "Improper Sleep"

            sj.duration = totalDuration
            sj.status = status
            sj.save()
        else:
            if age > 6 and 12 >= age:
                if duration >= 9 and duration <= 12:
                    status = "Adequate Sleep"
                else:
                    status = "Improper Sleep"
            elif age > 13 and 18 >= age:
                if duration >= 8 and duration <= 10:
                    status = "Adequate Sleep"
                else:
                    status = "Improper Sleep"
            elif age > 18 and 64 >= age:
                if duration >= 7 and duration <= 9:
                    status = "Adequate Sleep"
                else:
                    status = "Improper Sleep"
            elif age > 65:
                if duration >= 7 and duration <= 8:
                    status = "Adequate Sleep"
                else:
                    status = "Improper Sleep"
            else:
                if duration >= 12 and duration <= 16:
                    status = "Adequate Sleep"
                else:
                    status = "Improper Sleep"

            sj = SleepJournals.objects.create(user=user,duration=duration,status=status)
            sj.save()
    data = SleepJournals.objects.filter(user=user).order_by("-id")
    return render(request,"usersj.html",{"data":data})

def usermj(request):
    uid=request.session["id"]
    user = Registration.objects.get(id=uid)
    if request.POST:
        desc = request.POST['desc']
        report = request.FILES['report']
        wk = MedicalJournals.objects.create(user=user,desc=desc,report=report)
        wk.save()
    data = MedicalJournals.objects.filter(user=user).order_by("-id")
    return render(request,"usermj.html",{"data":data})

def check(request):
    return render(request,"check.html")

def userblogs(request):
    uid = request.session['id']
    user = Registration.objects.get(id=uid)
    data = Blogs.objects.exclude(user=uid).order_by("-id")
    if 'title' in request.POST:
        title = request.POST['title']
        desc = request.POST['desc']
        ins = Blogs.objects.create(user=user,title=title,desc=desc)
        ins.save()
    if "search" in request.POST:
        search = request.POST['search']
        data = Blogs.objects.filter(Q(title__contains=search) | Q(desc__contains=search)).exclude(user=uid).order_by("-id")
    return render(request,"userblogs.html", {"data":data})

def userviewblog(request):
    uid = request.session['id']
    user = Registration.objects.get(id=uid)
    id = request.GET['post']
    data = Blogs.objects.get(id=id)
    if request.method == "POST":
        comment = request.POST['comment']
        db = Comments.objects.create(comment=comment, blog=data, user=user)
        db.save()

    comments = Comments.objects.filter(blog=id)
    return render(request,"userviewblog.html", {"data":data, "comments": comments})

def userdocs(request):
    data = Doctor.objects.filter(user__is_active=1)
    if request.POST:
        search = request.POST['search']
        data = Doctor.objects.filter(Q(user__is_active=1) & Q(Q(name__contains=search) | Q(specialization__contains=search)))

    return render(request, "userdocs.html", {"data":data})

def userExperts(request):
    data = Expert.objects.filter(user__is_active=1)
    if request.POST:
        search = request.POST['search']
        data = Expert.objects.filter(Q(user__is_active=1) & Q(name__contains=search))
    return render(request, "userExperts.html", {"data":data})

def userChat(request):
    uid = request.session["id"]
    eid = request.GET['id']
    do = Registration.objects.get(id=uid)
    url = request.GET['url']
    op = Expert.objects.get(id=eid)
    if request.method == "POST":
        msg = request.POST['msg']
        db = Chat.objects.create(expert=op, user=do, message=msg, sendby='User')
        db.save()
    messages = Chat.objects.filter(expert=op, user=do)
    return render(request, "userChat.html", {"messages":messages, "url":url})

def userviewdocdetails(request):
    uid = request.session['id']
    user = Registration.objects.get(id=uid)
    id = request.GET['id']
    data = Doctor.objects.get(id=id)
    if request.POST:
        bookingdate = request.POST['bookingdate']
        time = request.POST['time']
        token = int(1)
        if Booking.objects.filter(docid=data,bookingdate=bookingdate).exists():
            getTok = Booking.objects.filter(docid=data,bookingdate=bookingdate).order_by("-id")[0]
            cToken = int(getTok.token)
            token += cToken
        req = Booking.objects.create(regid=user,docid=data,bookingdate=bookingdate,time=time,token=token)
        req.save()
        return redirect("/userbookings")
    return render(request, "userviewdocdetails.html", {"data":data})

def userbookings(request):
    uid = request.session['id']
    data = Booking.objects.filter(regid=uid).exclude(status="Paid")
    return render(request, "userbookings.html", {"data":data})

def userhistory(request):
    uid = request.session['id']
    data = Booking.objects.filter(regid=uid,status="Paid")
    return render(request, "userhistory.html", {"data":data})

def userviewpres(request):
    id = request.GET['id']
    data = Prescription.objects.filter(bid=id)
    return render(request, "userviewpres.html", {"data":data})

def userpayment(request):
    id = request.GET['id']
    bok = Booking.objects.get(id=id)
    if request.POST:
        pay = Payment.objects.create(bid=bok,status='Payment Complted')
        pay.save()
        bok.status = 'Paid'
        bok.save()
        return redirect("/userhistory")
    return render(request, "userpayment.html")



def dochome(request):
    uid = request.session['id']
    name = Doctor.objects.get(id=uid)
    return render(request, "dochome.html", {"name":name.name})

def docbookings(request):
    uid = request.session['id']
    data = Booking.objects.filter(docid=uid).exclude(status="Paid")
    return render(request, "docbookings.html", {"data":data})

def dochistory(request):
    uid = request.session['id']
    data = Booking.objects.filter(docid=uid,status="Paid")
    return render(request, "dochistory.html", {"data":data})

def docupdatestatus(request):
    id = request.GET['id']
    status = request.GET['status']
    bok = Booking.objects.get(id=id)
    bok.status = status
    bok.save()
    return redirect("/docbookings")

def docaddpres(request):
    uid = request.session['id']
    id = request.GET['id']
    bok = Booking.objects.get(id=id)
    if request.POST:
        prescription = request.POST['prescription']
        diagnosis = request.POST['diagnosis']
        req = Prescription.objects.create(prescription=prescription, diagnosis=diagnosis,bid=bok)
        req.save()
        bok.status = 'Consulted'
        bok.save()
        return redirect("/docbookings")
    data = Prescription.objects.filter(bid__regid=bok.regid)
    return render(request, "docaddpres.html", {"data":data})

def docviewpres(request):
    id = request.GET['id']
    data = Prescription.objects.filter(bid=id)
    return render(request, "docviewpres.html", {"data":data})

def docreports(request):
    uid = request.session['id']
    data = Booking.objects.filter(docid=uid)
    if request.POST:
        sDate = request.POST['sDate']
        eDate = request.POST['eDate']
        status = request.POST['status']
        data = Booking.objects.filter(Q(bookeddate__range=(sDate, eDate)) & Q(docid=uid) & Q(status__contains=status) )
    cou = 0
    for d in data:
        if d.status == 'Paid':
            cou += 1
    total = cou * 500
    total = f"RS. {total}/-"
    return render(request,"docreports.html", {"data":data, "total":total})





































































































