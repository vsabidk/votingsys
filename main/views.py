from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.http import Http404
from .models import User,Position,Candidate, Visited_Check
from .forms import AuthForm
import random

def PasswordGen():
    characters = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSUVWXYZ0123456789@#$')
    password = ''
    while len(password) < 8:
        password+=characters[random.randint(0,len(characters)-1)]
    return password

def Authentication(request):
    logout(request)
    form = AuthForm(request.POST)
    if request.method  == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username,password=password)
            if user is not None:
                login(request,user)
            
                if request.user.is_superuser:
                    return redirect('Admin_page')
                else:
                    return redirect('Voting_page/0')
            else:
                form = AuthForm()
        else:
            form = AuthForm()
    else:
        form = AuthForm()
    return render(request, 'Login_page.html', context = {'form':form})
 





def voting_procedures(request,ind):
    if request.user.is_authenticated:
        Positions = list(Position.objects.all().filter(Grades_voting__contains = '%s'%(request.user.grade)))
        Pos_copy = Positions[:]
        if request.user.grade <= 12:
            for i in Positions:
                if i.House == 'X':
                    pass
                else:
                    if request.user.house.upper() != i.House.upper():
                        Pos_copy.remove(i)
                        print(i.Position_name)

        
        Positions = Pos_copy[:]

        if int(ind) >= len(list(Positions)):
            logout(request)
            return redirect('/Thanks')
        else:
            return redirect('/Vote/%s'%(ind,))
    else:
        return redirect('')
            
            
def Vote(request,index):
    if request.user.is_authenticated and not Visited_Check.objects.all().filter(user=request.user, url=request.path).exists():
        Positions = list(Position.objects.all().filter(Grades_voting__contains = '%s'%(request.user.grade)))
        Pos_copy = Positions[:]
        if request.user.grade <= 12:
            for i in Positions:
                if i.House == 'X':
                    pass
                else:
                    if request.user.house.upper() != i.House.upper():
                        print(i.Position_name)
                        Pos_copy.remove(i)
                        

        
        Positions = Pos_copy[:]
        data = Candidate.objects.all().filter(position=Positions[int(index)])
        pos = Positions[int(index)].Position_name
        index = str(int(index)+1)
        obj = Visited_Check(user=request.user,url=request.path)
        obj.save()
        return render(request,'voting_page.html',context={'data':data,'index':index,'pos':pos})
    else:
        return redirect('/Voting_page/%s'%(int(index)+1,))
    
def counter(request,id,index):
    obj = Candidate.objects.get(id=id)
    obj.votes_Recieved +=1
    obj.save()
    return redirect('/Voting_page/%s'%(index,))


def thanks(request):
    return render(request, 'Thanks.html')





import csv
from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect
from .forms import UserForm
import csv

def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            unhashed_password = form.cleaned_data['password']
            user.set_password(unhashed_password)

            try:
                user.save()
                # Log the unhashed password for debugging (temporarily)
                print(f"Unhashed Password: {unhashed_password}")

                # Write to CSV for debugging (not recommended for production)
                with open('users.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([user.username, user.grade, user.house, unhashed_password])

                return redirect('/add_user')  # Adjust the redirect URL as needed
            except IntegrityError:
                form.add_error('username', 'This username is already taken. Please choose another.')

    else:
        form = UserForm()

    return render(request, 'add_user.html', {'form': form})




import csv
import random
import string
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .models import User
from django.contrib import messages

def generate_password():
    """Generates a random password."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

def process_csv_file(csv_file):
    """Process the CSV file to create users."""
    decoded_file = csv_file.read().decode("utf-8").splitlines()
    reader = csv.DictReader(decoded_file)
    users = []

    for row in reader:
        username = row['username']
        if User.objects.filter(username=username).exists():
            continue  # Skip if user already exists

        grade = int(row['grade']) if row['grade'] else None
        house = row['house'][:1].upper() if row['house'] else None
        password = generate_password()
        
        user = User(username=username, grade=grade, house=house)
        user.set_password(password)
        users.append(user)

        # Update the CSV file with username and password
        with open('users.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([username, password])

    # Save users to the database
    User.objects.bulk_create(users)

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            process_csv_file(request.FILES['file'])
            messages.success(request, 'Users added')
            form = UploadFileForm()
    else:
        form = UploadFileForm()

    return render(request, 'upload_file.html', {'form': form})



from django.shortcuts import render, redirect
from .forms import PositionForm
from .models import Position

def add_position(request):
    if request.method == 'POST':
        form = PositionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/ap')  # Redirect to the position list view
    else:
        form = PositionForm()

    positions = Position.objects.all()  # Fetch all positions to display in the form
    return render(request, 'add_position.html', {'form': form, 'positions': positions})



from django.shortcuts import render, redirect
from .forms import CandidateForm
from .models import Candidate

def add_candidate(request):
    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/ac')  # Redirect to a list of candidates or another view
    else:
        form = CandidateForm()

    candidates = Candidate.objects.all()
    return render(request, 'add_candidate.html', {'form': form, 'candidates': candidates})


import csv
from django.http import HttpResponse
from .models import Candidate
from django.shortcuts import render
from io import BytesIO
from django.http import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def export_csv(request):
    candidates = Candidate.objects.all().order_by('position', '-votes_Recieved')
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="election_results.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Position', 'Candidate Name', 'Votes Received'])
    
    for candidate in candidates:
        writer.writerow([candidate.position.Position_name, candidate.Candidate_name, candidate.votes_Recieved])
    
    return response

def export_pdf(request):
    candidates = Candidate.objects.all().order_by('position', '-votes_Recieved')
    
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    y_position = height - 40
    p.setFont("Helvetica-Bold", 16)
    p.drawString(40, y_position, "Election Results")
    
    y_position -= 40
    p.setFont("Helvetica-Bold", 12)
    p.drawString(40, y_position, "Position")
    p.drawString(200, y_position, "Candidate Name")
    p.drawString(400, y_position, "Votes Received")

    y_position -= 20
    p.setFont("Helvetica", 12)

    for candidate in candidates:
        p.drawString(40, y_position, candidate.position.Position_name)
        p.drawString(200, y_position, candidate.Candidate_name)
        p.drawString(400, y_position, str(candidate.votes_Recieved))
        y_position -= 20
        if y_position < 40:
            p.showPage()
            y_position = height - 40
            p.setFont("Helvetica-Bold", 12)
            p.drawString(40, y_position, "Position")
            p.drawString(200, y_position, "Candidate Name")
            p.drawString(400, y_position, "Votes Received")
            y_position -= 20
            p.setFont("Helvetica", 12)
    
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='election_results.pdf')

def view_results(request):
    positions = Candidate.objects.values('position__Position_name').distinct()
    grouped_candidates = {}
    
    for position in positions:
        position_name = position['position__Position_name']
        candidates = Candidate.objects.filter(position__Position_name=position_name).order_by('-votes_Recieved')
        grouped_candidates[position_name] = candidates

    return render(request, 'view_results.html', {'grouped_candidates': grouped_candidates})
