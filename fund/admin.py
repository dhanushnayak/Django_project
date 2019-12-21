from django.contrib import admin
from .models import food,stay,medicine,region,donate,citizen,spent_on,required
from django.contrib.auth.decorators import login_required
from admin_numeric_filter.admin import NumericFilterModelAdmin, SingleNumericFilter, RangeNumericFilter,SliderNumericFilter

from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter

# Register your models here.


    

admin.site.register(food, list_display = ('name','cost'),search_fields = ('name',"cost"),filter_horizontal=(),list_filter = ( ), fieldsets = ())
admin.site.register(stay, list_display = ('name','cost'),search_fields = ('name',"cost"),filter_horizontal=(),list_filter = ( ), fieldsets = ())
admin.site.register(medicine, list_display = ('name','cost'),search_fields = ('name',"cost"),filter_horizontal=(),list_filter = ( ), fieldsets = ())
admin.site.register(region, list_display = ('place','caused','migrated'),filter_horizontal=(),list_filter = ( ), fieldsets = ())
admin.site.login 
#admin.site.register(spent_on,list_display = ('name','date','quality','Total'),search_fields=('date','name'),readonly_fields=('Total','quality'),filter_horizontal=(),list_filter = (), fieldsets = ())
@admin.register(donate)
class donateAdmin(admin.ModelAdmin):
    list_display = ("date","name","email","amount","organization")
    search_fields=('name',"email","organization")
    readonly_fields=("date","name","email","amount","organization")
    list_filter = (
        ('date', DateRangeFilter),
    )
    filter_horizontal=()
    fieldsets = ()
    list_per_page= 15
    def has_add_permission(self, request,obj=None):
            return False
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    try:
        pass
    except:
        pass
    
@admin.register(citizen)
class citizenAdmin(admin.ModelAdmin):
    list_display = ('name',"adhar","gender","place_id","migrated")
    search_fields=('name',"adhar")
    readonly_fields=("name","adhar","gender","place_id","migrated")
    list_filter = ()
    filter_horizontal=()
    fieldsets = ()
    list_per_page= 15
    def has_add_permission(self, request,obj=None):
            return False
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    try:
        pass
    except:
        pass
    
@admin.register(spent_on)
class spent_onAdmin(admin.ModelAdmin):
    list_display = ('name','date','quality','Total')
    search_fields=('date','name')
    readonly_fields=('Total','quality','date','name')
    list_filter = (
    )
    filter_horizontal=()
    fieldsets = ()
    list_per_page = 15
    def has_add_permission(self, request,obj=None):
            return False
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    try:
        pass
    except:
        pass
    
@admin.register(required)
class requiredAdmin(admin.ModelAdmin):
    list_display = ('date','place','required','required1','quality','feedback')
    search_fields=('date','place','required','required1','feedback')
    readonly_fields = ('date','place','required','required1','quality','feedback')
    list_filter = (
        ('date', DateRangeFilter),
    )
    filter_horizontal=()
    fieldsets = ()
    list_per_page = 15
    def has_add_permission(self, request,obj=None):
            return False
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    try:
        pass
    except:
        pass
    