from django.shortcuts import render,redirect,get_object_or_404, get_list_or_404,reverse,render_to_response
from datetime import date 
from datetime import datetime
from django.template import RequestContext
from .models import donate,citizen,region,required,medicine,food,spent_on,stay
from django.db.models import signals
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from time import sleep
import urllib.parse
import pandas as pd
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
import numpy as np
from django.contrib.auth.decorators import user_passes_test
from .forms import SignUpForm
#-----------------------------------index-----------------------------------------
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
        
    return render(request, 'signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/') 

def index(request):
    
    total = amount_sum()
    feedback = feedback_required()
    dff=0
    df=0
    spsum=0
    remain=total
    f=0
    male=0
    female=0
    try:
        feedback = feedback.head(10)
    except:
        pass
    cost = dataframe_spent()
    try:
        cost['date']=cost['date'].astype(str)
        cost=cost.sort_values(by='date', ascending=False) 
    except:
        pass
        
    try:
        df=cost.head(15)
    except:
        pass
    try:
        dff=cost['Total'].sum()
    except:
        pass
    food = 0
    stay =0 
    med =0 
    try:
        food = fooddf()
        stay = staydf()
        med = meddf()
        sp=dataframe_spent()
    except:
        pass
    try:
        spsum=sp['Total'].sum()
        remain=total-spsum
    except:
        pass
    y=people()
    male = 0 
    female =0
    no_of_people=0
    migrated = 0
    f = fund_organization()
    try:
        f = f.sort_values(['amount'],ascending=0)
        f=f.head(5)
    except:
        pass
    
    try:
        male=y['gender'].loc[(y['gender']=='Male')].count()
        if male == 0:
            male=0
        female=y['gender'].loc[(y['gender']=='Female')].count()
        if female == 0:
            female=0
        migrated = y['adhar'].loc[(y['migrated']=='Yes')].count()
        if migrated == 0:
                migrated=0
        no_of_people= y['adhar'].count()
        if no_of_people == 0:
            no_of_people=0
       
        
    except:
        pass

    try:
        query = request.GET.get('search_box', '')
        if query:
            # query example
            results = donate.objects.filter(name__icontains=query)
            result = donate.objects.filter(organization__icontains=query)
            if 1==1:    
                if len(result) > len(results) :
                    s=result
                else:
                    s=results
                return render(request,'search.html',{"results":s,"q":query})
    except:
        pass


    
    return render(request,'admin/index.html',{"total":total,'feedback':feedback,'cost':df,'sum':dff,'food':food,'stay':stay,'med':med,"male":male,"female":female,'migrated':migrated,'no_of_people':no_of_people,'fund_org':f,'spent_total':spsum,'remain':remain})

#----------------------------------functions------------------------------------------


def connectdb():
    from pymongo import MongoClient as client
    connect = client("mongodb://localhost:27017/")
    db=connect.fund
    return db
def sort_feedback():
    try:
        y=connectdb()
        fd=y['fund_required']
        d = {}
        f=[]
        for x in fd.find():
            d=x
            f.append(d)
        df = pd.DataFrame(f)
        df=df.set_index('date')
        df= df.drop('_id',axis=1)
        df = df.drop(['id','feedback'],axis=1)
        df=df.sort_values(['quality'],ascending=False) 
        return df
    except:
        pass
def donatedf():
    try:
        from pymongo import MongoClient as client
        connect = client("mongodb://localhost:27017/")
        db=connect.fund
        fd=db['fund_donate']
        y = []

        for x in fd.find():
            y.append(x)
        df=pd.DataFrame(y)
        return df
    except:
        pass
def amount_sum():
    
        from pymongo import MongoClient as client
        connect = client("mongodb://localhost:27017/")
        db=connect.fund
        fd=db.fund_donate
        y = []

        for x in fd.find():
            y.append(x['amount'])
        z = sum(y)
        return z
    

def place():
    try:
        from pymongo import MongoClient as client
        connect = client("mongodb://localhost:27017/")
        db=connect.fund
        fd= db['fund_region']
        y =[]
        for x in fd.find():
            y.append(x['place'])
        return y
    except:
        pass

def matchadhar():
    try:
        db = connectdb()
        fd = db['fund_citizen']
        y =[]
        for x in fd.find():
            y.append(x['adhar'])
        return y 
    except:
        pass

def flist():
    try:
        db = connectdb()
        fd = db['fund_food']
        y=[]
        for x in fd.find():
            y.append(x['name'])
        return y
    except:
        pass

def mlist():
    try:
        db = connectdb()
        fd = db['fund_medicine']
        y=[]
        for x in fd.find():
            y.append(x['name'])
        return y
    except:
        pass
def slist():
    try:
        db = connectdb()
        fd = db['fund_stay']
        y=[]
        for x in fd.find():
            y.append(x['name'])
        return y
    except:
        pass
def feedback_required():
    try:
        y=connectdb()
        fd=y['fund_required']
        d = {}
        f=[]
        for x in fd.find():
            d=x
            f.append(d)
        df = pd.DataFrame(f)
        df=df.set_index('id')
        df=df.drop('_id',axis=1)
        df['Date']=pd.to_datetime(df['date'], format="%m/%d/%Y")
        df=df.drop('date',axis=1)
        df=df.iloc[::-1]
        
        return df
    except:
        pass

def people():
    try:
        y=connectdb()
        fd=y['fund_citizen']
        d = {}
        f=[]
        for x in fd.find():
            d=x
            f.append(d)
        df = pd.DataFrame(f)
        return df
    except:
        pass
def fooddf():
    try:
        y=connectdb()
        fd=y['fund_food']
        d = {}
        f=[]
        for x in fd.find():
            d=x
            f.append(d)
        df = pd.DataFrame(f)
        df=df.set_index('_id')
        return df
    except:
        pass

def meddf():
    try:
        y=connectdb()
        fd=y['fund_medicine']
        d = {}
        f=[]
        for x in fd.find():
            d=x
            f.append(d)
        df = pd.DataFrame(f)
        df=df.set_index('_id')
        return df
    except:
        pass
def staydf():
    try:
        y=connectdb()
        fd=y['fund_stay']
        d = {}
        f=[]
        for x in fd.find():
            d=x
            f.append(d)
        df = pd.DataFrame(f)
        df=df.set_index('_id')
        df=df.drop(['id'],axis=1)
        return df
    except:
        pass


def requireddf():
    try:
        y=connectdb()
        fd=y['fund_required']
        d = {}
        f=[]
        for x in fd.find():
            d=x
            f.append(d)
        df = pd.DataFrame(f)
        df=df.set_index('date')
        df=df.drop('_id',axis=1)
        return df
    except:
        pass

def costfield():
    try:
            df=requireddf()
            
            df1=fooddf()
            df2=staydf()
            df3=meddf()
            df1=pd.concat([df1,df2])
            df1=pd.concat([df1,df3])
            df1=df1.fillna('Rural Bangalore')
            df=df.rename(columns={"required1":"name"})
            df['cost']=df['name'].map(df1.set_index('name')['cost'])
            df['Total']= df['cost']*df['quality']
            df=df.drop(['cost','place'],axis=1)
            f=df
            g = dataframe_spent()
            try:
                if dataframe_spent()==None:
                    df=f
            
            except ValueError:   
               
                    df = f[~((f.name.isin(g.name))&(f.quality.isin(g.quality))&(f.id.isin(g.id)))]
                    df=df.sort_values(['Total'],ascending=False)
                
            df['date']=date.today()
            df['date']=df['date'].astype(str)
        
            return df
    except:
        pass
       
def fund_organization():
    try:
        y=connectdb()
        fd = y['fund_donate']
        d = {}
        f=[]
        for x in fd.find():
            d=x
            f.append(d)
        df = pd.DataFrame(f)
        df=df.groupby('organization').sum()
        df=df.sort_values('amount',ascending=False)
        df['organization']=df.index
        return df
    except:
        pass

def spent_table():
    try: 
        df=costfield()
        df['id1']=df['id']
        df = df.set_index('id')
        df['id']=df['id1']
        df=df.drop(columns='id1')
        y= connectdb()
        fd=y['fund_spent_on']

        import json
        records = json.loads(df.T.to_json()).values()
        for r in records:
            fd.insert(r)
    except:
        pass

def dataframe_spent():
    l=[]
    try:
        y=connectdb()
        fd=y['fund_spent_on']
        d={}
        l=[]
        for f in fd.find():
            d=f
            l.append(d)
        if len(l)!=0:
            dff=pd.DataFrame(l)
        else:
            dff=0
        return dff
    except:
        df = 0
   
        return df
    
def roughreq():
        try:
            df=requireddf()
            df1=fooddf()
            df2=staydf()
            df3=meddf()
            df1=pd.concat([df1,df2])
            df1=pd.concat([df1,df3])
            df9=df1.drop(columns="place",axis=1)
            df['date']=df.index
            df=df.rename(columns={"required1":"name"})
            df=df.merge(df9,on="name")
            df['Total']=df['quality']*df['cost']
            df=df.drop(columns=['cost'],axis=1)
            return df
        except:
            pass
#-----------------------------renders------------------------------------------------------------------------------
@login_required(login_url='/admin/login/')
def update(request):
   
        total = amount_sum()
        try:
            feedback = feedback_required()
            if feedback==None:
                feedback=[]
            
        except:
            pass
        
        cost = costfield()
        df=cost
       
        try:
            df=df['Total'].sum()
        except:
            pass
        food = 0
        stay = 0
        med = 0
        try:
            food = fooddf()
            stay = staydf()
            med = meddf()
            sp=dataframe_spent()
        except:
            pass
        
        spsum=0
        remain=total
        try:
            spsum=sp['Total'].sum()
            remain=total-spsum
        except:
            pass
        y=people()
        male =0
        female=0
        no_of_people=0
       
        migrated=0
        f = fund_organization()
        try:
            male=y['gender'].loc[(y['gender']=='Male')].count()
            female=y['gender'].loc[y['gender']=='Female'].count()
            migrated = y['adhar'].loc[(y['migrated']=='Yes')].count()
            no_of_people= y['adhar'].count()
            
        except:
            pass
       

        return render(request,'admin/update.html',{"total":total,'feedback':feedback,'cost':cost,'sum':df,'food':food,'stay':stay,'med':med,"male":male,"female":female,'migrated':migrated,'no_of_people':no_of_people,'fund_org':f,'spent_total':spsum,'remain':remain})
@login_required(login_url='/admin/login/')
def submit(request):
        cost = costfield()
        df=cost
        try:
            df=df['Total'].sum()
        except:
            pass
        remain=amount_sum()
        try:
            sp=dataframe_spent()
            total = amount_sum()
            spsum=sp['Total'].sum()
            remain=total-spsum
        except:
            pass
        try:
            if df>remain:
                messages.success(request,'🔴 Funds InSufficiant...')
            elif df<remain:
                try:
                    if request.method == 'GET':
                        spent_table()
                        if 1==1:
                            messages.success(request,'✔️Funds Submitted !!!!')
                except :
                        pass
        except:
            pass               
        
    
    
        return render(request, 'admin/submit.html',{'sum':df})
def dform(request):
    try:
        if request.method == 'POST':
            if request.POST.get('amount') and request.POST.get('email'):
                fund = donate()
                fund.date = datetime.today()
                fund.name = request.POST.get("name")
                fund.email = request.POST.get("email")
                organization = request.POST.get("organization")
                if (organization != ''):
                    fund.organization = organization
                else:
                    messages.error(request,'🔴 Organization is Blank')
                amount = request.POST.get("amount")
                if(amount!=''):
                    fund.amount=amount
                else:
                    messages.error(request,'🔴 Amount is null')
                if(fund.amount and fund.organization):
                    fund.save()
                    messages.success(request,'✔️ Fund saved!!!!')
                else:
                    messages.error(request,'🔴 Not saved')
            
                return HttpResponseRedirect('/')
        
        else:

        
            return render(request , "donate/index.html")
    except:
        pass   

def cform(request):
    try:
        x = place()
        if request.method == 'POST':
            if request.POST.get('Aadhar No'):
                people = citizen()

                people.name = request.POST.get("name")
                adhar = request.POST.get("Aadhar No")
                ng = matchadhar()
                if ((int(adhar) in ng) or (len(adhar)!=12)):
                    messages.error(request, '🔴 Adhar no is duplicated')
                else:
                    people.adhar=adhar
                
                gender = request.POST.get("gender")
                if(gender!='Choose Gender'):
                    people.gender=gender
                else:
                    messages.error(request,'Gender not selected')
                xy = request.POST.get('from')
                xplace = region.objects.get(place=xy)
                if (xplace != "Choose from"):
                    people.place=xplace
                else:
                    messages.error(request,'Select your place in from')
                migrated = request.POST.get("migrated")
                if (migrated=='Choose migrated'):
                    messages.error(request,'🔴 Select The migrate option')
                else:
                    people.migrated=migrated
                if(people.migrated and people.adhar and people.name and people.place):
                    people.save()
                    messages.success(request,'✔️ Saved!!!!!!!!!!')
                return HttpResponseRedirect('/citizen/')
        else:

        
            return render(request , "citizen form/index.html",{"place":x})
    except:
        pass

def  rform(request):
    try:
        x = place()
        return render(request,'feedback/index.html',{'place':x})
    except:
        pass

def fform(request):
    try:
        x = place()
        fo=flist()

        if request.method == 'POST':
            if request.POST.get('place') and request.POST.get('requirement'):
                feed = required()
                feed.date= datetime.today()
                xy = request.POST.get('place')
                xplace = region.objects.get(place=xy)
                feed.place=xplace
                cat=request.POST.get('requirement')
                if(( cat != "Choose requirement") and (cat != '')):
                    feed.required=cat
                cat2=request.POST.get('requirement1')
                if ((cat2 != 'Choose Food Items') and (cat2 != '')):
                    feed.required1=cat2
                quaity = request.POST.get("Quality")
                if(quaity==''):
                    feed.quality=1
                else:
                    feed.quality=quaity
                feed.feedback=request.POST.get('feedback')
                if feed.required1  and feed.required:
                    feed.save()
                    messages.success(request, '✔️ Form submission successful')
                    
                else:
                    messages.error(request, '🔴 Oops, something bad happened')
                    
                    return HttpResponseRedirect('/food/')

                return HttpResponseRedirect('/food/')
            
            
        else:
                return render(request,'feedback/food.html',{"place":x,'food':fo})
    except:
        pass

def mform(request):
    try:
        x = place()
        me=mlist()

        if request.method == 'POST':
            if request.POST.get('place') and request.POST.get('requirement'):
                feed = required()
                feed.date= datetime.today()
                xy = request.POST.get('place')
                xplace = region.objects.get(place=xy)
                feed.place=xplace
                cat=request.POST.get('requirement')
                if ((cat != 'Choose requirement') and (cat != '')):
                    feed.required=cat
                cat1=request.POST.get('requirement1')
                if((cat1!='Choose Medicines')and(cat1!='')):
                    feed.required1=cat1
                quaity = request.POST.get("Quality")
                if(quaity==''):
                    feed.quality=1
                else:
                    feed.quality=quaity
                feed.feedback=request.POST.get('feedback')
                if(feed.required1 and feed.required):
                    feed.save()
                    messages.success(request, '✔️ Form submission successful')
                    
                else:
                    messages.error(request, '🔴 Oops, something bad happened')
                    
                    return HttpResponseRedirect('/medicine')
                return HttpResponseRedirect('/medicine')
        else:
                return render(request,'feedback/medicine.html',{"place":x,'medicine':me})
    except:
        pass


def sfrom(request):
    try:
        x = place()
        me=slist()

        if request.method == 'POST':
            if request.POST.get('place') and request.POST.get('requirement'):
                feed = required()
                feed.date= datetime.today()
                xy = request.POST.get('place')
                xplace = region.objects.get(place=xy)
                feed.place=xplace
                cat=request.POST.get('requirement')
                if((cat != 'Choose requirement')and (cat != '')):
                    feed.required=cat
                feed.required1=request.POST.get('requirement1')
                quaity = request.POST.get("Quality")
                if(quaity==''):
                    feed.quality=1
                else:
                    feed.quality=quaity
                feed.feedback=request.POST.get('feedback')
                if(feed.required):
                    feed.save()
                    messages.success(request, '✔️ Form submission successful')
                    
                else:
                    messages.error(request, '🔴 Oops, something bad happened')
                    
                    return HttpResponseRedirect('/stay')
                return HttpResponseRedirect('/stay')
        else:
                return render(request,'feedback/stay.html',{"place":x,'stay':me})
    except:
        pass

def foodlist(request):
    istekler = food.objects.all()
    return render(request, 'list/foodlist.html', locals())

def requiredlist(request):
    istekler = required.objects.all()
    return render(request, 'list/requiredlist.html', locals())

def staylist(request):
    istekler = stay.objects.all()
    return render(request, 'list/staylist.html', locals())

def medlist(request):
    istekler = medicine.objects.all()
    return render(request, 'list/medlist.html', locals())

def spentlist(request):
    istekler = spent_on.objects.all()
    return render(request, 'list/spentlist.html', locals())

def search(request):
    

    query = request.GET.get('search_box', '')
    if query:
        # query example
        results = donate.objects.filter(name__icontains=query)
        result = donate.objects.filter(organization__icontains=query)
        
        if len(result) > len(results) :
            s=result
        else:
            s=results
    else:
        s = []
    return render(request, 'search.html', {'q':query,'results':s})
#----------------------------------------Show dataframe-----------------------------------
#-------------------------------------Plots-------------------------------------------------------------
from .fusioncharts import FusionCharts
def chart(request):
        try:
            query = request.GET.get('search_box', '')
            if query:
                # query example
                results = donate.objects.filter(name__icontains=query)
                result = donate.objects.filter(organization__icontains=query)
                if 1==1:    
                    if len(result) > len(results) :
                        s=result
                    else:
                        s=results
                    return render(request,'search.html',{"results":s,"q":query})
        except:
            pass
        # Customer
        try:
            dataSource = {}
            dataSource['chart'] = {
                "caption": "Amount Donated by Organization",
                "subcaption":"Donated",
                "showValues": "1",
                "theme": "fusion"
                }
            dataSource['data'] = []
            f = fund_organization()
            f=f.set_index(['id'])
            f=f.groupby(['organization']).sum()
            l=[]
            for x in range(len(f)):
                l.append(x+1)
            f['org']=f.index
            f['id']=l
            f=f.set_index(['id'])

            f=f.to_dict(orient='records')
            
            for key in f:
                data = {}
                data['label'] = key['org']
                data['value'] = key['amount']
                dataSource['data'].append(data)
        except:
            pass
       
        fundsorg = FusionCharts("pie3d", "ex1", "100%", "415", "chart-1", "json", dataSource)
        #_________________________________________________________________________________________________________________
        try:
            total = amount_sum()
            sp=dataframe_spent()
            spsum=0
            remain=0
            try:
                spsum=sp['Total'].sum()
                remain=total-spsum
            except:
                pass
            df1={}
            df1['chart']={
                "caption": "FUNDS Spent",
                "subcaption":"Total funds =  "+str(total),
                "showValues": "1",
                "showPercentInTooltip" : "1",
                "theme": "fusion"
                }
            df1['data']=[{'label':'Spent(till date)','value':str(spsum)},{'label':'Avaliable Funds','value':str(remain)}]
        except:
            pass
        pie3d = FusionCharts("pie3d", "ex2" , "100%", "415", "chart-2", "json",df1)
        # The data is passed as a string in the `dataSource` as parameter.
        #_________________________________________________________________________________________________________________________
        try:
            datasource1={}
            datasource1['chart']={
                "caption": "Funds Received ",
                "subcaption":"(Groupby-Dateseries)",
                "showValues": "1",
                "theme": "fusion,ocean"
                }
            df2 = donatedf()
            df2['date']=df2.date.astype("str")
            df2=df2.groupby(['date']).sum()
            df2 = df2['amount']
            df2 =df2.to_dict()
            datasource1['data']=[]
            for key,value in df2.items():
                data1={}
                data1["label"]=key
                data1['value']=value
                data1['color']="#00BFFF"
                datasource1['data'].append(data1)
        except:
            pass
        
           
        spgraph = FusionCharts("column2d", "ex3" , "550", "415", "chart-3", "json",datasource1)  
        #_____________________________________________________________________________________________________________
        try:
            datasource2={}
            datasource2['chart']={
                "caption": "Funds Received AS per Email ID ",
                "subcaption":"(Groupby-EMAIL)",
                "showValues": "1",
                "theme": "fusion,ocean"
                }
            datasource2['data']=[]
            df3=donatedf()
            print(df3)
            df3 = df3.groupby(['email']).sum()
            df3.index = df3.index
            df3=df3.head(6)
            df3 = df3['amount']
            df3 = df3.to_dict()
            for key,value in df3.items():
                data3={}
                data3['label']=key
                data3['value']=value
                data3['color']="#FFB6C1"
                datasource2['data'].append(data3)
        except:
            pass
        emailgraph = FusionCharts("column2d", "ex4" , "550", "415", "chart-4", "json",datasource2)  
        #______________________________________________________________________________________________________________________________
        try:
            datasource3={}
            datasource3['chart']={
                "caption": "Amount assigned for Food",
        "subcaption": "ASSIGNED",
        "showValues": "1",
        "showpercentvalues": "0",
        "defaultcenterlabel": "Food",
        "aligncaptionwithcanvas": "0",
        "captionpadding": "0",
        "decimals": "1",
        
        "theme": "fusion"
                }
            datasource3['data']=[]
            df4=fooddf()
            df4 = df4.groupby('name').sum()
            df4 = df4['cost']
            df4=df4.to_dict()
            for key,value in df4.items():
                data4={}
                data4['label']=key
                data4['value']=value
                datasource3['data'].append(data4)
        except:
            pass
            
        foodgraph=FusionCharts("doughnut2d", "ex5" , "550", "400", "chart-5", "json",datasource3) 
        #__________________________________________________________________________________________________________________
        try:
            datasource4={}
            datasource4['chart']={
                "caption": "Amount asigned for Medicines",
        "subcaption": "ASSIGNED",
        "showValues": "1",
        "showpercentvalues": "0",
        "defaultcenterlabel": "MEDKITS",
        "aligncaptionwithcanvas": "0",
        "captionpadding": "0",
        "decimals": "1",
        
        "theme": "fusion"
                }
            datasource4['data']=[]
            df5=meddf()
            df5 = df5.groupby('name').sum()
            df5 = df5['cost']
            df5=df5.to_dict()
            for key,value in df5.items():
                data5={}
                data5['label']=key
                data5['value']=value
                data5['color']="#006BF7"
                datasource4['data'].append(data5)
        except:
            pass
            
        medgraph=FusionCharts("column3d", "ex6" , "1110", "400", "chart-6", "json",datasource4) 
        #____________________________________________________________________________________________________________
        try:
            datasource5={}
            datasource5['chart']={
                "caption": "Amount asigned for Stay",
        "subcaption": "ASSIGNED",
        "showValues": "1",
        "showpercentvalues": "0",
        "defaultcenterlabel": "Stay",
        "aligncaptionwithcanvas": "0",
        "captionpadding": "0",
        "decimals": "1",
        
        "theme": "fusion"
                }
            datasource5['data']=[]
            df6=staydf()
            df6 = df6.groupby('name').sum()
            df6 = df6['cost']
            df6=df6.to_dict()
            for key,value in df6.items():
                data6={}
                data6['label']=key
                data6['value']=value
                datasource5['data'].append(data6)
        except:
            pass
        
        staygraph=FusionCharts("doughnut2d", "ex7" , "550", "400", "chart-7", "json",datasource5) 
        
        
        return render(request, 'plot/ch.html', {'output': fundsorg.render(),'output2':pie3d.render(),"spgraph":spgraph.render(),'egraph':emailgraph.render(),'fgraph':foodgraph.render(),'medgraph':medgraph.render(),"staygraph":staygraph.render()})
#________________________________________________________________________________________________________________________________-
def chart2(request):
    try:
            query = request.GET.get('search_box', '')
            if query:
                # query example
                results = donate.objects.filter(name__icontains=query)
                result = donate.objects.filter(organization__icontains=query)
                if 1==1:    
                    if len(result) > len(results) :
                        s=result
                    else:
                        s=results
                    return render(request,'search.html',{"results":s,"q":query})
    except:
        pass
    try:
        try:
            th = fooddf()
            th1 = staydf()
            th2 = meddf()
            th3 = dataframe_spent()
            food=pd.merge(th3,th,on='name')
            medd=pd.merge(th3,th2,on='name')
            stayy = pd.merge(th3,th1,on='name')
            foodt=food['Total'].sum()
            meddt=medd['Total'].sum()
            stayt=stayy['Total'].sum()
        except:
            pass
        df1={}
        df1['chart']={
                "caption": "Amount Spent based on category",
                "subcaption":"Total Amount Spent = "+str(foodt+meddt+stayt),
                "showValues": "1",
                "showpercentvalues": "0",
            "defaultcenterlabel": "Spent",
            "aligncaptionwithcanvas": "0",
            "captionpadding": "0",
            "decimals": "1",
            "theme" : "fusion",
                }
        df1['data']=[{'label':'Food','value':str(foodt)},{'label':'Med','value':str(meddt)},{'label':'Stay','value':str(stayt)}]
    except:
        pass
    Total = FusionCharts("pyramid", "ex1" , "550", "405", "chart-1", "json",df1)
    #___________________________________________________________________________________________________________________________________
    try:
        try:
            df = dataframe_spent()
            df['date']=df['date'].astype(str)
            datedf=df.groupby(['date']).sum()
            datedf=datedf['Total']
            datedf = datedf.to_dict()
        except:
            pass
        df2={}
        df2['chart']={
                "caption": "Amount Spent based on Date",
                "subcaption":"Total Amount Spent = "+str(foodt+meddt+stayt),
                "showValues": "1",
                "showpercentvalues": "0",
            "defaultcenterlabel": "Spent",
            "yaxisname": "Amount",
            "xaxisname":"Dates",
            "anchorradius": "5",
            "aligncaptionwithcanvas": "0",
            "captionpadding": "0",
            "decimals": "1",
            "theme" : "fusion",
                }
        df2['data']=[]
        for key,value in datedf.items():
            d22={}
            d22['label']=key
            d22['value']=value
            d22['color']="#FF5A87"
            df2['data'].append(d22)
    except:
        pass
    dTotal = FusionCharts("spline", "ex2" , "550", "405", "chart-2", "json",df2)  
    #_____________________________________________________________________________________________________________________-
    try:
        try:
            datafr = dataframe_spent()
            datafr['date'] = datafr['date'].astype(str)
            datafr = dataframe_spent().groupby(['name']).sum()
            datafr = datafr.sort_values(by=['Total'],ascending=0)
            datafr = datafr['Total']
            datafr = datafr.to_dict()
        except:
            pass
        df3={}
        df3['chart']={
                "caption": "Amount Spent based on Items",
                "subcaption":"Total Amount Spent = "+str(foodt+meddt+stayt),
                "showValues": "1",
                "showpercentvalues": "0",
            "defaultcenterlabel": "Spent",
            "aligncaptionwithcanvas": "0",
            "captionpadding": "0",
            "decimals": "1",
            "theme" : "fusion",
                }
        df3['data']=[]
        for key,value in datafr.items():
            datah={}
            datah['label']=key
            datah['value']=value
            datah['color']="#F067FE"
            df3['data'].append(datah)
    except:
        pass
        
    itotal = FusionCharts("bar2d", "ex3" , "550", "405", "chart-3", "json",df3) 
    #______________________________________________________________________________________________________________________________
    try:
        try:
            dfy = roughreq()
            dfy=dfy.groupby(['date']).sum()
            dfy = dfy['Total']
            dfy = dfy.to_dict()
        except:
            pass
        df4={}
        df4['chart']={
                "caption": "Amount Required based on Date",
                "subcaption":"required",
                "showValues": "1",
                "showpercentvalues": "0",
            "yaxisname": "Amount",
            "xaxisname":"Dates",
            "anchorradius": "3",
            "aligncaptionwithcanvas": "0",
            "captionpadding": "0",
            "decimals": "1",
            "theme" : "fusion",
                }
        df4['data']=[]
        for key,value in dfy.items():
            dfi={}
            dfi['label']=str(key).replace("00:00:00","")
            dfi['value']=value
            dfi['color']="#FE67A5"
            df4['data'].append(dfi)
    except:
        pass
    dtotalf =  FusionCharts("spline", "ex4" , "550", "405", "chart-4", "json",df4) 
    #_________________________________________________________________________________________________________________________________________
    try:
        try:
            fd = dataframe_spent()
            fd = fd.groupby(['name']).sum()  
            fd = fd.drop(['id'],axis=1)
            fdt = fd['Total'].to_dict()
            fdq = fd['quality'].to_dict()
        except:
            pass
        df5={}
        df5['chart']={
                "caption": "Amount Spent for quatity vs amount on Items",
                "subcaption":"Quatity vs Amount",
                "showValues": "1",
                "showpercentvalues": "0",
            
            "aligncaptionwithcanvas": "0",
            "captionpadding": "0",
            "decimals": "1",
            "theme" : "fusion",
                }
        df5['categories']=[]
        df51=[]

        for key,value in fdt.items():
            df511={}
            df511['label']=key
            
            df51.append(df511)
    
        df5['categories']=[{"category":df51}]
        df5['dataset']=[]
        df52=[]
        for key,value in fdt.items():
            df522={}
            
            df522['value']=str(value)
            df52.append(df522)
        df53=[]
        
        for key,value in fdq.items():
            df5222={}
        
            df5222['value']=str(value)
            df53.append(df5222)
        df5['dataset']=[{"seriesname": "Total Amount","data":df52},{"seriesname": "Quanity","data":df53}]
    except:
        pass
    totalf =  FusionCharts("mscolumn2d", "ex5" , "1110", "400", "chart-5", "json",df5) 
            
    
    return render(request, "plot/chart.html",{'output':Total.render(),'output2':dTotal.render(),'output3':itotal.render(),"output4":dtotalf.render(),"output5":totalf.render()})
        
#__________________________________________________________________________________________________________________________________
@login_required(login_url='/admin/login/')
def adchart(request):
        # Customer
        dataSource = {}
        dataSource['chart'] = {
            "caption": "Amount Donated by Organization",
            "subcaption":"Donated",
            "showValues": "1",
            "theme": "fusion"
            }
        dataSource['data'] = []
        try:
            f = fund_organization()
            f=f.set_index(['id'])
            f=f.groupby(['organization']).sum()
            l=[]
            for x in range(len(f)):
                l.append(x+1)
            f['org']=f.index
            f['id']=l
            f=f.set_index(['id'])

            f=f.to_dict(orient='records')
        except:
            pass
        try:
            for key in f:
                data = {}
                data['label'] = key['org']
                data['value'] = key['amount']
                dataSource['data'].append(data)
        except:
            pass
       
        fundsorg = FusionCharts("pie3d", "ex1", "102%", "415", "chart-1", "json", dataSource)
        #_________________________________________________________________________________________________________________
        
        total = amount_sum()
        sp=dataframe_spent()
        spsum=0
        remain=0
        try:
            spsum=sp['Total'].sum()
            remain=total-spsum
        except:
            pass
        df1={}
        df1['chart']={
            "caption": "FUNDS Spent",
            "subcaption":"Total funds =  "+str(total),
            "showValues": "1",
            "showPercentInTooltip" : "1",
            "theme": "fusion"
            }
        df1['data']=[{'label':'Spent(till date)','value':str(spsum)},{'label':'Avaliable Funds','value':str(remain)}]
        pie3d = FusionCharts("pie3d", "ex2" , "102%", "415", "chart-2", "json",df1)
        # The data is passed as a string in the `dataSource` as parameter.
        #_________________________________________________________________________________________________________________________
        datasource1={}
        datasource1['chart']={
            "caption": "Funds Received ",
            "subcaption":"(Groupby-Dateseries)",
            "showValues": "1",
            "theme": "fusion,ocean"
            }
        try:
            df2 = donatedf()
            df2['date']=df2.date.astype("str")
            df2=df2.groupby(['date']).sum()
            df2 = df2['amount']
            df2 =df2.to_dict()
        except:
            pass
        datasource1['data']=[]
        try:
            for key,value in df2.items():
                data1={}
                data1["label"]=key
                data1['value']=value
                data1['color']="#00BFFF"
                datasource1['data'].append(data1)
        except:
            pass
        
           
        spgraph = FusionCharts("column2d", "ex3" , "550", "415", "chart-3", "json",datasource1)  
        #_____________________________________________________________________________________________________________
        datasource2={}
        datasource2['chart']={
            "caption": "Funds Received AS per Email ID ",
            "subcaption":"(Groupby-EMAIL)",
            "showValues": "1",
            "theme": "fusion,ocean"
            }
        datasource2['data']=[]
        try:
            df3=donatedf()
            df3 = df3.groupby(['email']).sum()
            df3.index = df3.index.str.replace("@gmail.com","")
            df3=df3.head(6)
            df3 = df3['amount']
            df3 = df3.to_dict()
            for key,value in df3.items():
                data3={}
                data3['label']=key
                data3['value']=value
                data3['color']="#FFB6C1"
                datasource2['data'].append(data3)
        except:
            pass
        emailgraph = FusionCharts("column2d", "ex4" , "550", "415", "chart-4", "json",datasource2)  
        #______________________________________________________________________________________________________________________________
        datasource3={}
        datasource3['chart']={
            "caption": "Amount assigned for Food",
    "subcaption": "ASSIGNED",
    "showValues": "1",
    "showpercentvalues": "0",
    "defaultcenterlabel": "Food",
    "aligncaptionwithcanvas": "0",
    "captionpadding": "0",
    "decimals": "1",
    
    "theme": "fusion"
            }
        datasource3['data']=[]
        try:
            df4=fooddf()
            df4 = df4.groupby('name').sum()
            df4 = df4['cost']
            df4=df4.to_dict()
            for key,value in df4.items():
                data4={}
                data4['label']=key
                data4['value']=value
                datasource3['data'].append(data4)
        except:
            pass
        
        foodgraph=FusionCharts("doughnut2d", "ex5" , "550", "400", "chart-5", "json",datasource3) 
        #__________________________________________________________________________________________________________________
        datasource4={}
        datasource4['chart']={
            "caption": "Amount asigned for Medicines",
    "subcaption": "ASSIGNED",
    "showValues": "1",
    "showpercentvalues": "0",
    "defaultcenterlabel": "MEDKITS",
    "aligncaptionwithcanvas": "0",
    "captionpadding": "0",
    "decimals": "1",
    
    "theme": "fusion"
            }
        datasource4['data']=[]
        try:
            df5=meddf()
            df5 = df5.groupby('name').sum()
            df5 = df5['cost']
            df5=df5.to_dict()
            for key,value in df5.items():
                data5={}
                data5['label']=key
                data5['value']=value
                data5['color']="#006BF7"
                datasource4['data'].append(data5)
        except:
            pass
        
        medgraph=FusionCharts("column3d", "ex6" , "1110", "400", "chart-6", "json",datasource4) 
        #____________________________________________________________________________________________________________
        datasource5={}
        datasource5['chart']={
            "caption": "Amount asigned for Stay",
    "subcaption": "ASSIGNED",
    "showValues": "1",
    "showpercentvalues": "0",
    "defaultcenterlabel": "Stay",
    "aligncaptionwithcanvas": "0",
    "captionpadding": "0",
    "decimals": "1",
    
    "theme": "fusion"
            }
        datasource5['data']=[]
        try:
            df6=staydf()
            df6 = df6.groupby('name').sum()
            df6 = df6['cost']
            df6=df6.to_dict()
            for key,value in df6.items():
                data6={}
                data6['label']=key
                data6['value']=value
                datasource5['data'].append(data6)
        except:
            pass
        
        staygraph=FusionCharts("doughnut2d", "ex7" , "550", "400", "chart-7", "json",datasource5) 
        
        
        return render(request, 'plot/adminch.html', {'output': fundsorg.render(),'output2':pie3d.render(),"spgraph":spgraph.render(),'egraph':emailgraph.render(),'fgraph':foodgraph.render(),'medgraph':medgraph.render(),"staygraph":staygraph.render()})
#____________________________________________________________________________________________________________________________
@login_required(login_url='/admin/login/')
def adchart2(request):
    th =0 
    th1=0
    th2=0
    th3=0
    foodt = 0
    meddt =0 
    stayt =0 
    
    
    th = fooddf()
    th1 = staydf()
    th2 = meddf()
    th3 = dataframe_spent()
    try:
            food=pd.merge(th3,th,on='name')
            medd=pd.merge(th3,th2,on='name')
            stayy = pd.merge(th3,th1,on='name')
            foodt=food['Total'].sum()
            meddt=medd['Total'].sum()
            stayt=stayy['Total'].sum()
    except:
            pass
    df1={}
    df1['chart']={
                "caption": "Amount Spent based on category",
                "subcaption":"Total Amount Spent = "+str(foodt+meddt+stayt),
                "showValues": "1",
                "showpercentvalues": "0",
            "defaultcenterlabel": "Spent",
            "aligncaptionwithcanvas": "0",
            "captionpadding": "0",
            "decimals": "1",
            "theme" : "fusion",
                }
    df1['data']=[{'label':'Food','value':str(foodt)},{'label':'Med','value':str(meddt)},{'label':'Stay','value':str(stayt)}]
    
    Total = FusionCharts("pyramid", "ex1" , "550", "405", "chart-1", "json",df1)
    #___________________________________________________________________________________________________________________________________
   
    datedf =0 
    try:
            dfdataf=dataframe_spent()
            dfdataf['date']=dfdataf['date'].astype(str)
            datedf=dfdataf.groupby(['date']).sum()
            datedf=datedf['Total']
            datedf = datedf.to_dict()
    except:
            pass
    df2={}
    df2['chart']={
                "caption": "Amount Spent based on Date",
                "subcaption":"Total Amount Spent = "+str(foodt+meddt+stayt),
                "showValues": "1",
                "showpercentvalues": "0",
            "defaultcenterlabel": "Spent",
            "yaxisname": "Amount",
            "xaxisname":"Dates",
            "anchorradius": "5",
            "aligncaptionwithcanvas": "0",
            "captionpadding": "0",
            "decimals": "1",
            "theme" : "fusion",
                }
    df2['data']=[]
    try:
        for key,value in datedf.items():
                d22={}
                d22['label']=key
                d22['value']=value
                d22['color']="#FF5A87"
                df2['data'].append(d22)
    except:
        pass
    
    dTotal = FusionCharts("spline", "ex2" , "550", "405", "chart-2", "json",df2)  
    #_____________________________________________________________________________________________________________________-
   
    
    try:
            datafr = dataframe_spent().groupby(['name']).sum()
            datafr = datafr.sort_values(by=['Total'],ascending=0)
            datafr = datafr['Total']
            datafr = datafr.to_dict()
    except:
            pass
    df3={}
    df3['chart']={
                "caption": "Amount Spent based on Items",
                "subcaption":"Total Amount Spent = "+str(foodt+meddt+stayt),
                "showValues": "1",
                "showpercentvalues": "0",
            "defaultcenterlabel": "Spent",
            "aligncaptionwithcanvas": "0",
            "captionpadding": "0",
            "decimals": "1",
            "theme" : "fusion",
                }
    df3['data']=[]
    try:
        for key,value in datafr.items():
                datah={}
                datah['label']=key
                datah['value']=value
                datah['color']="#F067FE"
                df3['data'].append(datah)
    except:
        pass
        
    itotal = FusionCharts("bar2d", "ex3" , "550", "405", "chart-3", "json",df3) 
    #______________________________________________________________________________________________________________________________
    
    try:
            dfy = roughreq()
            dfy['date']=dfy['date'].astype(str)
            dfy=dfy.groupby(['date']).sum()
            dfy = dfy['Total']
            dfy = dfy.to_dict()
    except:
            pass
    df4={}
    df4['chart']={
                "caption": "Amount Required based on Date",
                "subcaption":"required",
                "showValues": "1",
                "showpercentvalues": "0",
            "yaxisname": "Amount",
            "xaxisname":"Dates",
            "anchorradius": "3",
            "aligncaptionwithcanvas": "0",
            "captionpadding": "0",
            "decimals": "1",
            "theme" : "fusion",
                }
    df4['data']=[]
    try:
        for key,value in dfy.items():
                dfi={}
                dfi['label']=str(key).replace("00:00:00","")
                dfi['value']=value
                dfi['color']="#FE67A5"
                df4['data'].append(dfi)
    except:
        pass
    
    dtotalf =  FusionCharts("spline", "ex4" , "550", "405", "chart-4", "json",df4) 
    #_________________________________________________________________________________________________________________________________________
   
    fdt =0
    fdq =0 
    try:
            fd = dataframe_spent()
            fd = fd.groupby(['name']).sum()  
            fd = fd.drop(['id'],axis=1)
            fdt = fd['Total'].to_dict()
            fdq = fd['quality'].to_dict()
    except:
            pass
    df5={}
    df5['chart']={
                "caption": "Amount Spent for quatity vs amount on Items",
                "subcaption":"Quatity vs Amount",
                "showValues": "1",
                "showpercentvalues": "0",
            
            "aligncaptionwithcanvas": "0",
            "captionpadding": "0",
            "decimals": "1",
            "theme" : "fusion",
                }
    df5['categories']=[]
    df51=[]
    try:
        for key,value in fdt.items():
                df511={}
                df511['label']=key
                
                df51.append(df511)
    except:
        pass
    df5['categories']=[{"category":df51}]
    df5['dataset']=[]
    df52=[]
    try:
        for key,value in fdt.items():
                df522={}
                
                df522['value']=str(value)
                df52.append(df522)
    except:
        pass
    df53=[]
    try:   
        for key,value in fdq.items():
                df5222={}
            
                df5222['value']=str(value)
                df53.append(df5222)
    except:
        pass
    df5['dataset']=[{"seriesname": "Total Amount","data":df52},{"seriesname": "Quanity","data":df53}]
    
    totalf =  FusionCharts("mscolumn2d", "ex5" , "1110", "400", "chart-5", "json",df5) 
            
    
    return render(request, "plot/adminchart.html",{'output':Total.render(),'output2':dTotal.render(),'output3':itotal.render(),"output4":dtotalf.render(),"output5":totalf.render()})
