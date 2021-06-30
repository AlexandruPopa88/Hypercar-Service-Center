from collections import deque
from django.db import models
# Create your models here.

class Ticket(models.Model):
    queue = {
        "change_oil": deque(),
        "inflate_tires": deque(),
        "diagnostic": deque()
    }
    next_ticket = None

    service = models.CharField(max_length=15)
    wait_min = models.IntegerField(null=True)

    @classmethod
    def ETA(cls, service):
        total_time = 0
        if service == "change_oil":
            total_time += 2  * len(cls.queue["change_oil"])
        elif service == "inflate_tires":
            total_time += 2 * len(cls.queue["change_oil"]) + 5  * len(cls.queue["inflate_tires"])
        else:
            total_time += 2 * len(cls.queue["change_oil"]) + 5  * len(cls.queue["inflate_tires"]) + 30 * len(cls.queue["diagnostic"])
        return total_time