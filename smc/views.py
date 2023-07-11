from django.shortcuts import render, redirect
from .models import MenuItem, Student, Transaction
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import F, Q
from django.contrib.admin.views.decorators import staff_member_required, user_passes_test
from django.urls import reverse
from .forms import OrderForm
import datetime

# Create your views here.

def loginPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')
    
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('smc:menu')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('smc:login')
    elif request.method == 'GET':
        return render(request, 'smc/login.html')
    

def logoutUser(request):
    logout(request)
    return redirect('smc:login')
    

def add_funds(request):
    if request.method == 'POST':
        student = Student.objects.get(user=request.user)
        amount = request.POST['amount']
        transaction = Transaction(student=student, transaction_type='Deposit', amount=amount)
        transaction.save()
        student.account_balance += float(amount)
        student.save()
        return redirect('history')
    else:
        return render(request, 'add_funds.html')


@staff_member_required(login_url='smc:login')
def menu(request):
    if request.method == 'POST':
        student_id = request.POST['roll']
        selected_items = request.POST.getlist('selected_items[]')

        # Perform checks such as student's balance and available items

        # Deduct the total cost from the student's account balance
        student = Student.objects.get(roll=student_id)
        # Calculate the total cost of the selected items
        total_cost = sum([MenuItem.objects.get(item_id=item_id).price for item_id in selected_items])

        if total_cost <= student.account_balance:
            student.account_balance -= total_cost
            student.save()

            # Record the transaction
            transaction = Transaction.objects.create(student=student, transaction_type='Debit', amount=total_cost)
            # Add the selected items to the transaction
            transaction.items.add(*selected_items)
            transaction.save()
            # update the quantity of the selected items
            MenuItem.objects.filter(item_id__in=selected_items).update(qty=F('qty') - 1)

            return redirect('smc:menu')
        else:
            error_message = 'Insufficient balance. Please add funds to your account.'
            students = Student.objects.all()
            menu_items = MenuItem.objects.all()
            context = {'students': students, 'menu_items': menu_items, 'error_message': error_message}
            return render(request, 'smc/menu.html', context)
        


    students = Student.objects.all()
    # menu_items = MenuItem.objects.all()
    # get menu items for the current day
    today = datetime.datetime.today().strftime('%a')
    # today = 'Mon'
    menu_items = MenuItem.objects.filter(Q(day='Everyday')|Q(day=today))
    context = {'students': students, 'menu_items': menu_items}
    return render(request, 'smc/menu.html', context)


def mainMenu(request):
    menu_items = MenuItem.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            roll_id = form.cleaned_data['roll_id']

            # Process the selected items and calculate the total cost
            total_cost = 0
            for item in menu_items:
                field_name = f"item_{item.item_id}"
                if form.cleaned_data[field_name]:
                    total_cost += item.price

            # Assuming you have a UserProfile model with a balance field for each student
            user_profile = Student.objects.get(roll=roll_id)
            if user_profile.account_balance >= total_cost:
                user_profile.account_balance -= total_cost
                user_profile.save()
                # Perform additional actions like updating the order history, etc.
                return redirect('smc:mainMenu')
            else:
                error_message = "Insufficient balance."
                return render(request, 'smc/mainMenu.html', {'menu_items': menu_items, 'form': form, 'error_message': error_message})
    else:
        form = OrderForm()
        error_message = None

    return render(request, 'smc/mainMenu.html', {'menu_items': menu_items, 'form': form, 'error_message': error_message})


def testMenu(request):
    return render(request, 'smc/testMenu.html')