from unfold.admin import ModelAdmin
from django.contrib import admin

from .models import Ticket, SolutionMessage
from unfold.contrib.forms.widgets import WysiwygWidget
from django import forms

# Form for Ticket
class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = '__all__'
        widgets = {
            'description': WysiwygWidget(),
        }

# Form for SolutionMessage
class SolutionMessageForm(forms.ModelForm):
    class Meta:
        model = SolutionMessage
        fields = '__all__'
        widgets = {
            'message': WysiwygWidget(), 
        }

# Inline for SolutionMessage
class SolutionMessageInline(admin.StackedInline):
    model = SolutionMessage
    form = SolutionMessageForm
    can_delete = True
    extra = 1
    verbose_name_plural = "Solution Messages"
    fk_name = 'ticket'
    
    def has_add_permission(self, request, obj=None):
        if request.user.groups.filter(name='Admin').exists() or request.user.is_superuser:
            return True
        elif request.user.groups.filter(name='Help-desk').exists():
            return True
        return False
    
    def has_change_permission(self, request, obj=None):
        if request.user.groups.filter(name='Admin').exists() or request.user.is_superuser:
            return True
        elif request.user.groups.filter(name='Help-desk').exists():
            return True
        return False
    
    def has_delete_permission(self, request, obj=None):
        if request.user.groups.filter(name='Admin').exists() or request.user.is_superuser:
            return True
        elif request.user.groups.filter(name='Help-desk').exists():
            return True
        return False

# TicketAdmin with Inline
@admin.register(Ticket)
class TicketAdmin(ModelAdmin):
    form = TicketForm
    list_display = ('id', 'title', 'status', 'priority', 'impact', 'created_by', 'assigned_to', 'created_at')
    list_filter = ('status', 'priority', 'impact', 'category')
    search_fields = ('title', 'description', 'subcategory')
    ordering = ('-created_at',)
    raw_id_fields = ('created_by', 'assigned_to')
    inlines = (SolutionMessageInline,)
    
    def get_readonly_fields(self, request, obj=None):
        if request.user.groups.filter(name='Help-desk').exists() and not request.user.is_superuser:
            return [f.name for f in self.model._meta.fields]
        return super().get_readonly_fields(request, obj)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name='Admin').exists() or request.user.is_superuser:
            return qs
        elif request.user.groups.filter(name='Help-desk').exists():
            return qs
        else:
            return qs.filter(created_by=request.user)

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        if request.user.groups.filter(name='Admin').exists() or request.user.is_superuser:
            return True
        elif request.user.groups.filter(name='Help-desk').exists():
            return True  
        else:
            return obj.created_by == request.user

    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return False
        if request.user.groups.filter(name='Admin').exists() or request.user.is_superuser:
            return True
        else:
            return obj.created_by == request.user

    def has_view_permission(self, request, obj=None):
        if obj is None:
            return True
        if request.user.groups.filter(name='Admin').exists() or request.user.groups.filter(name='Help-desk').exists() or request.user.is_superuser:
            return True
        else:
            return obj.created_by == request.user


@admin.register(SolutionMessage)
class SolutionMessageAdmin(ModelAdmin):
    form = SolutionMessageForm
    list_display = ('id', 'ticket', 'updated_at')
    list_filter = ('updated_at',)
    
    def has_module_permission(self, request):
        return False