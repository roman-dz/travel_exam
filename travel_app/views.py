from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.registration_validator(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        )
        request.session['user_id'] = user.id
        request.session['greeting'] = user.first_name
    return redirect('/addtrip')

def login(request):
    errors = User.objects.login_validator(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(email=request.POST['login_email'])
        request.session['user_id'] = user.id
        request.session['greeting'] = user.first_name
    return redirect('/travel')

def all_plans(request):
    if "user_id" not in request.session:
        return redirect('/')
    else:
        context = {
            'all_plans': Plan.objects.all(),
            'this_user': User.objects.get(id=request.session['user_id'])
        }
        return render(request, 'all_plans.html', context)

def create_first(request):
    if "user_id" not in request.session:
        return redirect('/')
    else:
        return render(request, 'add_plan.html')

def create_plan(request):
    errors = Plan.objects.travel_plan_validator(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/addtrip')
    else:
        user = User.objects.get(id=request.session["user_id"])
        plan = Plan.objects.create(
            destination = request.POST['destination'],
            description = request.POST['description'],
            date_from = request.POST['date_from'],
            date_to = request.POST['date_to'],
            creator = user
        )
        user.joined_plans.add(plan)  # Use the below statement to make the user auto-join travel plan upon plan creation

        return redirect(f'/travel')

def one_plan(request, plan_id):
    context = {
        'plan': Plan.objects.get(id=plan_id),
        'current_user': User.objects.get(id=request.session['user_id']),
        # 'date_from': Plan.objects.get('date_from'),
        # 'date_to': Plan.objects.get('date_to'),
    }
    return render(request, "one_plan.html", context)

def update(request, plan_id):
    plan = Plan.objects.get(id=plan_id)
    plan.plan_description = request.POST['description']
    plan.save()

    return redirect(f"/travel/{plan_id}")

def delete(request, plan_id):
    plan = Plan.objects.get(id=plan_id)
    plan.delete()

    return redirect('/travel')

# def joined(request, plan_id):
#     user = User.objects.get(id=request.session["user_id"])  # get the one user
#     plan = Plan.objects.get(id=plan_id)  # get the one plan
#     user.joined_plans.add(plan)  # join user to the plan
#                                   # remove other users from the same plan

#     return redirect(f'/plans/{plan_id}')

# New code
def joined(request, plan_id):
    user = User.objects.get(id=request.session["user_id"])
    plan = Plan.objects.get(id=plan_id)
    
    for user_joined in plan.joined_by.all():
        user_joined.joined_plans.remove(plan)
    
    user.joined_plans.add(plan)

    return redirect('/travel')
############

def unjoined(request, plan_id):
    user = User.objects.get(id=request.session["user_id"])
    plan = Plan.objects.get(id=plan_id)
    user.joined_plans.remove(plan)

    return redirect('/travel')

def logout(request):
    request.session.flush()

    return redirect('/')