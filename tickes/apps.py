from django.apps import AppConfig

class TickesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tickes'

    def ready(self):
        from django.contrib.auth.models import Group, Permission
        from django.contrib.contenttypes.models import ContentType
        from .models import Ticket, SolutionMessage

        # Créer les groupes
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        helpdesk_group, _ = Group.objects.get_or_create(name='Help-desk')
        normal_group, _ = Group.objects.get_or_create(name='Normal User')

        # Permissions pour Ticket
        ticket_ct = ContentType.objects.get_for_model(Ticket)
        perm_view_ticket = Permission.objects.get(codename='view_ticket', content_type=ticket_ct)
        perm_change_ticket = Permission.objects.get(codename='change_ticket', content_type=ticket_ct)
        perm_add_ticket = Permission.objects.get(codename='add_ticket', content_type=ticket_ct)
        perm_delete_ticket = Permission.objects.get(codename='delete_ticket', content_type=ticket_ct)

        # Permissions pour SolutionMessage
        solution_ct = ContentType.objects.get_for_model(SolutionMessage)
        perm_view_solution = Permission.objects.get(codename='view_solutionmessage', content_type=solution_ct)
        perm_change_solution = Permission.objects.get(codename='change_solutionmessage', content_type=solution_ct)
        perm_add_solution = Permission.objects.get(codename='add_solutionmessage', content_type=solution_ct)
        perm_delete_solution = Permission.objects.get(codename='delete_solutionmessage', content_type=solution_ct)

        # Assign permissions
        admin_group.permissions.set([
            perm_view_ticket, perm_change_ticket, perm_add_ticket, perm_delete_ticket,
            perm_view_solution, perm_change_solution, perm_add_solution, perm_delete_solution
        ])

        helpdesk_group.permissions.set([perm_view_ticket, perm_view_solution, perm_add_solution, perm_change_solution, perm_delete_solution])

        normal_group.permissions.set([
            perm_add_ticket, perm_view_ticket, perm_add_solution, perm_view_solution
        ])
