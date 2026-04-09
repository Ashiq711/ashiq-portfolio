from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib import messages
from .models import Experience,Idea,Article,ProjectStats,Project,Journey,Contact,Purchase
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import razorpay






# Create your views here.
def index(request):
   experiences = Experience.objects.all()[:6]
   projects=Project.objects.all()[:6]
   ideas=Idea.objects.all()[:6]

   return render(request, 'index.html', {
       'experiences': experiences,
       'projects':projects,
       'ideas': ideas
       })


def about(request):
    journeys=Journey.objects.all()
    return render(request, 'about.html', {'journeys':journeys})


def ideas(request):
   ideas = Idea.objects.all().order_by('-created_at')
   return render(request, 'ideas.html', {'ideas': ideas})



def articles(request):
   articles = Article.objects.all().order_by('-created_at')
   return render(request, 'articles.html', {'articles': articles})


def projects(request):
    stats = ProjectStats.objects.first()
    projects = Project.objects.all()

    return render(request, 'projects.html', {
        'stats': stats,
        'projects': projects
    })

def expertise(request):
    experiences = Experience.objects.all()
    return render(request, 'expertise.html', {'experiences': experiences})

def article_detail(request, id):
    article = Article.objects.get(id=id)
    return render(request, 'article_detail.html', {'article': article})


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Save to DB
        Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        # Send Email
        send_mail(
            subject=f"New Contact: {subject}",
            message=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=['abbasashique7@gmail.com'],  # 🔴 change this
            fail_silently=False,
        )

        # Success message
        messages.success(request, "Thank you for your valuable time in contacting me , i will get back to you as early as possible..!")
        

    return render(request, 'contact.html')


def payment_page(request, idea_id):
    idea = Idea.objects.get(id=idea_id)

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    payment = client.order.create({
        "amount": int(idea.price * 100),
        "currency": "INR",
        "payment_capture": 1
    })

    # Save to DB (IMPORTANT)
    purchase = Purchase.objects.create(
        idea=idea,
        name="Guest",  # later we’ll take input
        email="test@email.com",
        phone="0000000000",
        razorpay_order_id=payment['id'],
        amount=idea.price,
        status="created"
    )

    return render(request, "payment.html", {
        "idea": idea,
        "payment": payment,
        "razorpay_key": settings.RAZORPAY_KEY_ID
    })


@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        data = request.POST

        order_id = data.get('razorpay_order_id')
        payment_id = data.get('razorpay_payment_id')
        signature = data.get('razorpay_signature')

        purchase = Purchase.objects.get(razorpay_order_id=order_id)

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            })

            # SUCCESS
            purchase.razorpay_payment_id = payment_id
            purchase.razorpay_signature = signature
            purchase.status = "paid"
            purchase.save()

            return render(request, "download.html", {"idea": purchase.idea})

        except:
            purchase.status = "failed"
            purchase.save()

            return HttpResponse("Payment Failed")
        

def idea_detail(request, id):
    idea = Idea.objects.get(id=id)
    return render(request, 'idea_detail.html', {'idea': idea})

