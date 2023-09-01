import os
from rest_framework.response import Response
from rest_framework.decorators import api_view
from smc.models import Student, MenuItem
from .serializers import StudentSerializer, MenuItemSerializer, TransactionSerializer
from django.contrib.admin.views.decorators import staff_member_required
from smc.models import Student, MenuItem, Transaction
from decimal import Decimal
from .pdf import make_pdf
from .tasks import send_email

# Create your views here.

@api_view(['GET'])
# @staff_member_required(login_url='smc:login')
def getBalance(request, roll):
    # check if logged in user has roll number `roll`
    try:
        if request.user.student.roll == roll or request.user.is_staff:
            student = request.user.student
            return Response({'balance': student.account_balance})
        else:
            return Response({'error': 'Not authorized'})
    except:
        return Response({'error': 'Not authorized'})


@api_view(['GET'])
def getItems(request):
    menu_items = MenuItem.objects.all()
    menu_items = MenuItemSerializer(menu_items, many=True)
    return Response(menu_items.data)


@api_view(['GET'])
def getAccounts(request):
    students = Student.objects.all()
    students = StudentSerializer(students, many=True)
    return Response(students.data)


@api_view(['POST'])
def checkout(request):
    roll = request.data['roll']
    items = request.data['items']
    student = Student.objects.get(roll=roll)
    total_cost = 0
    for item in items.values():
        menu_item = MenuItem.objects.get(name=item['name'])
        total_cost += menu_item.price * Decimal(item['qty'])
    student.account_balance -= total_cost
    student.save()
    item_objects = [MenuItem.objects.get(item_id=item_key) for item_key in items.keys()]
    transaction = Transaction(student=student, transaction_type='Purchase', amount=total_cost, balance=student.account_balance)
    transaction.save()
    transaction.items.add(*item_objects)
    return Response({'message': 'success'})


@api_view(['POST'])
@staff_member_required(login_url='smc:login')
def addFunds(request):
    roll = request.data['roll']
    amount = request.data['amount']
    student = Student.objects.get(roll=roll)
    student.account_balance += Decimal(amount)
    # create a transaction
    transaction = Transaction(student=student, transaction_type='Deposite', amount=amount)
    transaction.save()
    student.save()
    return Response({'message': 'success'})


@api_view(['GET'])
def getHistory(request, roll):
    try:
        if request.user.student.roll == roll or request.user.is_staff:
            student = Student.objects.get(roll=roll)
            transactions = student.transaction_set.all()
            transactions = TransactionSerializer(transactions, many=True)
            return Response(transactions.data)
        else:
            return Response({'error': 'Not authorized'})
    except AttributeError:
        return Response({'error': 'Not authorized'})


@api_view(['GET'])
def emailStatement(request, roll):
    try:
        if request.user.student.roll == roll or request.user.is_staff:
            student = Student.objects.get(roll=roll)
            # get recent 10 transactions
            transactions = student.transaction_set.all()[:10]
            # make a pdf of the transactions and email it to the user requesting endpoint
            pdf = make_pdf(transactions)
            # email the pdf to the user
            # email = EmailMessage(
            #     subject=f'Statement for {student.roll}',
            #     body='Please find the attached statement',
            #     attachments=[(pdf, open(pdf, 'rb').read(), 'application/pdf')],
            #     to=[request.user.email]
            # )
            # email.send()
            send_email.delay(f'Statement for {student.roll}', 'Please find the attached statement', [request.user.email], [pdf])

            return Response({'message': 'success'})
        else:
            return Response({'error': 'Not authorized'})
    except AttributeError as e:
        return Response({'error': f'some error occured\n{e}'})



@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
            'Endpoint': '/balance/<str:roll>',
            'method': 'GET',
            'body': None,
            'description': 'Returns the account balance of the student with roll number `roll`'
        },
        {
            'Endpoint': '/items/',
            'method': 'GET',
            'body': None,
            'description': 'Returns the list of items available in the menu'
        },
        {
            'Endpoint': '/accounts/',
            'method': 'GET',
            'body': None,
            'description': 'Returns the list of all students'
        },
        {
            'Endpoint': '/checkout/',
            'method': 'POST',
            'body': {
                'roll': '<roll number of the student>',
                'items': {
                    '<item_id>': '<quantity>',
                    '<item_id>': '<quantity>',
                    '<item_id>': '<quantity>',
                    "...": "..."
                }
            },
            'description': 'Deducts the total cost of the items from the student\'s account balance'
        },
        {
            'Endpoint': '/add_funds/',
            'method': 'POST',
            'body': {
                'roll': '<roll number of the student>',
                'amount': '<amount to be added>'
            },
            'description': 'Adds the specified amount to the student\'s account balance'
        },
        {
            'Endpoint': '/history/<str:roll>',
            'method': 'GET',
            'body': None,
            'description': 'Returns the transaction history of the student with roll number `roll`'
        },
        {
            'Endpoint': '/email_statement/<str:roll>',
            'method': 'GET',
            'body': None,
            'description': 'Emails the transaction history of the student with roll number `roll` to the user requesting the endpoint (either the student or admin)'
        }
    ]
    return Response(routes)
