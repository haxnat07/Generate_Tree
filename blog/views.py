from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Post,People,Entries,Payment
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
import stripe
from django.contrib.auth.decorators import login_required
import random
from django.db.models import Q


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

def about(request):
    return render(request, 'blog/about.html', {'title': "About Page"})

def stories(request):
    return render(request, 'blog/stories.html')

def free_plan(request):
    return render(request, 'blog/free_plan.html')

def premium_plan(request):
    return render(request, 'blog/premium_plan.html')

@login_required
def add_people(request):
    if request.method == 'POST':
        name = request.POST.get('name') 
        if name:
            my_people = People(name=name, user=request.user)
            my_people.save()
            return redirect('people_list')
    return render(request, 'blog/add_people.html')

@login_required
def people_list(request):
    if request.method == 'GET':
        people = People.objects.filter(user=request.user)
    return render(request, 'blog/list.html',{'people':people})

@login_required
def add_entry(request, pk):
    if request.method == 'POST':
        # Extract data from the request
        year = request.POST.get('year')
        title = request.POST.get('title')
        description = request.POST.get('description')
        photo = request.FILES.get('photo', None)

        # Get the User instance
        user = People.objects.get(id = pk)

        # Save data to the database
        if photo:
            entry = Entries.objects.create(user=user, year=year, title=title, description=description, photo=photo)
        else:
            entry = Entries.objects.create(user=user, year=year, title=title, description=description)
        entry.save()
        return redirect("entry_list",user.id)
    return render(request, 'blog/add_entry.html')

@login_required
def entry_list(request,pk):
    user = People.objects.get(id = pk)
    entries = Entries.objects.filter(user=user)
    # print(entries)
    return render(request, 'blog/entry_list.html',{'entries':entries,'user_added':user})

#@login_required
def generate_tree(request,pk):
    colors_list = ['#ffc56f','#444444','#007bff','#6c757d','#8e8b51']
    random_color = random.choice(colors_list)
    user = People.objects.get(id = pk)
    entries = Entries.objects.filter(user=user)
    return render(request, 'blog/tree.html',{'entries':entries,'user_added':user,'color':random_color})
    
def premium_plan(request):
    
    return render(request, 'blog/premium_plan.html')

def tree_page(request):
    return render(request, 'blog/tree.html')

def premium(request):
    if request.method == 'POST':
        card = request.POST.get('card_number')   
        if card.isdigit() and len(card) == 16:
            payment = Payment(user=request.user,card=card)
            payment.save()
            return redirect('people_list')
    return render(request, 'blog/premium.html')


# def premium(request):
#     if request.method == 'POST':
#         stripe.api_key = 'sk_test_51OFD35HCn0Q8R1RZjsABieAYj2Rvg1wszP7oIZdodqdxb0p4eE1BZkkNi9kf9br3fSgNedT1ZuMjRfTqfD3Prl6d005FBoLJ1Y'
#         token = request.POST['stripeToken']
#         amount = 1000  # Amount in cents

#         try:
#             charge = stripe.Charge.create(
#                 amount=amount,
#                 currency='usd',
#                 description='Premium Membership',
#                 source=token,
#             )
#             # If the charge is successful, you can redirect the user to a thank you page or perform other actions
#             return redirect('blog/thank_you')
#         except stripe.error.CardError as e:
#             # Display error message to the user
#             error_message = e.error.message
#             return render(request, 'blog/premium.html', {'error_message': error_message})

#     # Handle GET requests or other cases
#     return render(request, 'blog/premium.html')

class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/stories.html'
    context_object_name = 'posts'
    ordering = ["-date_posted"]

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    

class StorySearchView(ListView):
    template_name = 'blog/stories.html'
    context_object_name = 'results'
    #login_url = '/login/'
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        post_results = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).order_by('-date_posted')
        
        people_results = People.objects.filter(
            name__icontains=query
        ).order_by('name')
        return list(post_results) + list(people_results)
        
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def contact_submit(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')

        # Prepare email content
        subject = f"New Contact Form Submission from {name}"
        email_content = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

        # Send email
        email = EmailMessage(
            subject=subject,
            body=email_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.CONTACT_EMAIL],
        )
        email.send()

        # Redirect
        return HttpResponseRedirect('/')
    else:
        return render(request, 'blog/contact_submit.html')
