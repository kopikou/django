from django.contrib import admin

# Register your models here.
from artists.models import Show,Artist,Type,Income,Expenses
@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    #list_display = ['name','show']
    list_display = ['id','name','show']  

@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ['id','name','type','price']    

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ['id','show_type']      

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ['id','date','place','show'] 

@admin.register(Expenses)
class ExpensesAdmin(admin.ModelAdmin):
    list_display = ['id','salary','artist','income__id']     