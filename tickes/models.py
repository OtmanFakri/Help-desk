from django.db import models
from django.contrib.auth.models import User

# Choices for priority, impact, and status
PRIORITY_CHOICES = [
    ('très haut', 'Très Haut'),
    ('haut', 'Haut'),
    ('moyen', 'Moyen'),
    ('bas', 'Bas'),
    ('très bas', 'Très Bas'),
]

IMPACT_CHOICES = [
    ('élevé', 'Élevé'),
    ('moyen', 'Moyen'),
    ('faible', 'Faible'),
]

STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('in_progress', 'In Progress'),
    ('solved', 'Solved'),
    ('closed', 'Closed'),
]

SOLUTION_STATUS_CHOICES = [
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
    ('pending', 'Pending'),
]

TYPE_CHOICES = [
    ('incident', 'Incident'),
    ('demande', 'Demande'),
]
class Ticket(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    category = models.CharField(max_length=100, blank=True, null=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    impact = models.CharField(max_length=20, choices=IMPACT_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='tickets_created')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets_assigned')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.status})"


class SolutionMessage(models.Model):
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE, related_name='solutionMessage')
    message = models.TextField()
    status = models.CharField(max_length=20, choices=SOLUTION_STATUS_CHOICES, default='pending')
    details = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Solution for Ticket {self.ticket.id}: {self.status}"
