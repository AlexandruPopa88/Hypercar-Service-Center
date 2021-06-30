from django.views import View
from django.shortcuts import render, HttpResponse,redirect
from .models import Ticket

class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')

class MenuView(View):
    def get(self, request):
        return render(request, "tickets/Menu.html", context={})

class TicketView(View):
    def get(self, request, service):
        my_ticket = Ticket(service = service)
        my_ticket.wait_min = Ticket.ETA(service)
        my_ticket.save()
        Ticket.queue[service].append(my_ticket)
        return render(request, "tickets/Ticket.html", {"ticket": my_ticket})

class ProcessingView(View):
    def get(self, request):
        return render(request, "tickets/Processing.html", {"tickets": Ticket.queue})

    def post(self, request):
        for service in Ticket.queue:
            if Ticket.queue[service]:
                Ticket.next_ticket = Ticket.queue[service].popleft()
                Ticket.next_ticket.delete()
                return redirect("/next")
        return HttpResponse("<div>Waiting for the next client</div>")

class NextTicketView(View):
    def get(self, request):
        return render(request, "tickets/NextTicket.html", {"next_ticket": Ticket.next_ticket})
