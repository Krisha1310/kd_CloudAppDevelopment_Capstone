from django.contrib import admin
from .models import CarMake, CarModel, CarDealer, DealerReview


# Register your models here.

# CarModelInline class
class CarModelInline(admin.ModelAdmin):
    name : 'BMW'
    dealer_id : 1
    type : 'Sedan'

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    fields: ['car_make' ,'name', 'dealer_id', 'type', 'year']

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    fields: ['name', 'description']
    inlines: [CarModelInline]

# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
