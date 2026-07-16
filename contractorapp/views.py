from django.shortcuts import render,redirect
from django.contrib import messages
from mainapp.models import*
from homeownerapp.models import*
from .models import *
from decimal import Decimal
# Create your views here.

def contractordash(request):
    if not 'contractorid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    contractorid = request.session.get('contractorid')
    contractor = UserInfo.objects.filter(email=contractorid).first()
    context = {
        'name':contractor.name,
        'contractorid':contractorid
    }
    return render(request,'contractordash.html',context)



def contractorlogout(request):
    if 'contractorid' in request.session:
        del request.session['contractorid']
        messages.success(request,"You are logged out")
        return redirect('login')
    else:
        return redirect('login')
    
def contractorprofile(request):
    if not 'contractorid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    contractorid = request.session.get('contractorid')
    contractor = UserInfo.objects.filter(email=contractorid).first()
    context = {
        'name':contractor.name, 
        'contractor':contractorid,
        'contractor':contractor
    }
    return render(request,'contractorprofile.html',context)

def contractoredit(request):
    if not 'contractorid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    contractorid = request.session.get('contractorid')
    contractor = UserInfo.objects.filter(email=contractorid).first()
    context = {
        'name':contractor.name,
        'contractor':contractorid,
        'contractor':contractor
    }
    if request.method == "POST":
        name = request.POST.get('name')
        contactno = request.POST.get('contactno')
        address = request.POST.get('address')
        bio = request.POST.get('bio')
        profile = request.FILES.get('profile')
        contractor.name =name
        contractor.contactno =contactno
        contractor.address =address
        contractor.bio =bio
        if profile:
            contractor.picture =profile
        contractor.save()
        messages.success(request,"Your profile has been updated successfully")
        return redirect('contractorprofile') 
    return render(request,'contractoredit.html',context)

def changepasswordco(request):
    if not 'contractorid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('contractorlogin')
    contractorid = request.session.get('contractorid')
    if request.method == 'POST':
        oldpwd = request.POST.get('oldpwd')  
        newpwd = request.POST.get('newpwd')  
        confirmpwd = request.POST.get('confirmpwd')
        try:
            contractor = LoginInfo.objects.get(username=contractorid)
            if contractor.password != oldpwd:
                messages.error(request,"Old password is incorrect")
                return redirect('changepassword')
            elif newpwd !=confirmpwd:
                messages.error(request,"New password and confirm password is not same")
                return redirect('changepassword')
            elif contractor.password == newpwd:
                messages.error(request,"New password is same as old password")
            else:
                contractor.password = newpwd
                contractor.save()
                messages.success(request,"Password changed successfully")
                return redirect('contractordash')
        except LoginInfo.DoesNotExist:
            messages.error(request,"Something went wrong")
            return redirect('adminlogin')        
    return render(request, 'changepasswordco.html',{'contractorid':contractorid})

def contractorviewprojects(request):
    if not 'contractorid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    contractorid = request.session.get('contractorid')
    contractor = UserInfo.objects.filter(email=contractorid).first()
    projects =Project.objects.filter(contractor=None)
    context = {
        'name':contractor.name,
        'contractorid':contractorid,
        'projects':projects
    }
    return render(request,'contractorviewprojects.html',context)


def applyproject(request,id):
    if not 'contractorid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    contractorid = request.session.get('contractorid')
    contractor = UserInfo.objects.filter(email=contractorid).first()
    project = Project.objects.get(id=id)
    context = {
        'name':contractor.name,
        'contractorid':contractorid,
        'project':project 
    }
    application = ContractorApplication.objects.filter(project=project,contractor=contractor)
    if application.exists():
        messages.warning(request ,"You have already applied for this project")
        return redirect('contractorviewprojects')
    if request.method =='POST':
        proposal_text = request.POST.get('proposal_text')
        design_file = request.FILES.get('design_file')
        estimated_budget = request.POST.get('estimated_budget')
        try: 
            estimated_budget = Decimal(estimated_budget)
        except:
            messages.error (request,"Invalid estimated budget") 
            return redirect('contractorviewprojects')  
        estimated_duration = request.POST.get('estimated_duration')
        app = ContractorApplication (
            contractor=contractor,
            project=project,
            proposal_text = proposal_text, 
            design_file = design_file,
            estimated_budget = estimated_budget,
            estimated_duration =  estimated_duration
        )
        app.save()
        messages.success(request,"Project Application submitted Successfully")
        return redirect('contractorviewprojects')

    return render(request,'applyproject.html',context)

def contractorapplications(request):
    if not 'contractorid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    contractorid = request.session.get('contractorid')
    contractor = UserInfo.objects.filter(email=contractorid).first()
    applications = ContractorApplication.objects.filter(contractor=contractor)
    context = {
        'name':contractor.name,
        'contractorid':contractorid,
        'applications':applications
    }
    return render(request,'contractorapplications.html',context)

def assignedprojects(request):
    if not 'contractorid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    contractorid = request.session.get('contractorid')
    contractor = UserInfo.objects.filter(email=contractorid).first()
    projects = Project.objects.filter(contractor=contractor)
    context = {
        'name':contractor.name,
        'contractorid':contractorid,
        'projects':projects
    }
    return render(request,'assignedprojects.html',context)

def addprogress(request,id):
    if not 'contractorid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    contractorid = request.session.get('contractorid')
    contractor = UserInfo.objects.filter(email=contractorid).first()
    project = Project.objects.get(id=id)
    context = {
        'name':contractor.name,
        'contractorid':contractorid,
        'project':project
    }
    if request.method == 'POST':
        update_text = request.POST.get('update_text')
        image = request.FILES.get('image')
        progress_percent = int(request.POST.get('progress_percent'))
        pu = ProgressUpdate(
            project=project,
            update_text=update_text,
            image=image,
            progress_percent=progress_percent,
            updated_by = contractor,
        )
        if progress_percent > 100:
            messages.error(request,"Progress can not be more than 100%")
            return redirect('addprogress',id=id)
        elif progress_percent<0 or progress_percent<project.progress:
           messages.error(request,"Progress can not be less than 0% or less than previous progress")
           return redirect('addprogress',id=id) 
        if progress_percent == 100:
            project.status = 'completed'
        project.progress = progress_percent
        project.save()
        pu.save()
        messages.success(request,"Updated Successfully")
        return redirect('assignedprojects')
    return render(request,'addprogress.html',context)