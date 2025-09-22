from django.shortcuts import render
from .models import Notice , Event 
from datetime import date
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactEnquiry
from django.core.mail import send_mail
from django.conf import settings



SCHOOL_NAME = "RK Sahu Junior High School"
Mobile_number="9140468493 or 9984031885"
address='Ramdashpur Nevada, Shitla Chaukiya, Jaunpur - 222001'
map_embed_code ='''<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d14372.51037246835!2d82.7126644!3d25.7663488!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x399039010272e529%3A0x98b4e3a8e9f358d6!2sRK%20sahu%20junior%20high%20school!5e0!3m2!1sen!2sin!4v1758396916394!5m2!1sen!2sin" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>'''

def home(request):
    notices = Notice.objects.order_by('-created_at')[:5]  # latest 5 notices
    events = Event.objects.filter(date__gte=date.today()).order_by('date')[:5]
    return render(request, 'index.html', {
    'notices': notices,
    'events': events,
    'school_name': SCHOOL_NAME ,
    'Mobile_number':Mobile_number,'address':address
})


def about(request):
    return render(request, 'about.html',{'school_name': SCHOOL_NAME,'Mobile_number':Mobile_number,'address':address,'map_embed_code': map_embed_code,})

def event(request):
    return render(request, 'event.html',{'school_name': SCHOOL_NAME,'Mobile_number':Mobile_number,'address':address,'map_embed_code': map_embed_code,})

# def gallery(request):
#     return render(request, 'gallery.html')

def faculty(request):
    return render(request, 'faculty.html',{'school_name': SCHOOL_NAME,'Mobile_number':Mobile_number,'address':address,'map_embed_code': map_embed_code,})


 
def contact(request):
    if request.method == "POST":
        parent_name = request.POST.get('parent_name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        student_name = request.POST.get('student_name')
        class_applying = request.POST.get('class_applying')
        message = request.POST.get('message')

        # Save to DB
        ContactEnquiry.objects.create(
            parent_name=parent_name,
            email=email,
            mobile=mobile,
            student_name=student_name,
            class_applying=class_applying,
            message=message
        )

        # Send email to school
        send_mail(
            "New Admission Enquiry Received",
            f"Parent/Guardian Name: {parent_name}\n"
            f"Email: {email}\n"
            f"Mobile: {mobile}\n"
            f"Student Name: {student_name}\n"
            f"Class Applying For: {class_applying}\n"
            f"Message: {message}",
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )

        messages.success(request, "Your enquiry has been submitted successfully!")
        return redirect('contact')

    return render(request, 'contact.html',{'school_name': SCHOOL_NAME,'Mobile_number':Mobile_number,'address':address
    ,'map_embed_code': map_embed_code,'map_embed_code': map_embed_code,})
