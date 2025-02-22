from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30, default='BMW')
    description = models.CharField(max_length=300)
    
    # Create a toString method for object string representation
    def __str__(self):
        return "Name: " + self.name + "," + \
            "Description: " + self.description


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    car_make = models.ManyToManyField(CarMake)
    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'WAGON'
    HATCHBACK = 'Hatchback'
    CROSSOVER = 'Crossover'
    TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'WAGON'),
        (HATCHBACK, 'Hatchback'),
        (CROSSOVER, 'Crossover')
    ]

    name = models.CharField(null=False, max_length=30, default='BMW')
    dealer_id = models.CharField(null=False, max_length=100)
    type = models.CharField(null=False, max_length=20, choices=TYPE_CHOICES, default=SEDAN)
    year = models.DateField(null=True)
    
    # Create a toString method for object string representation
    def __str__(self):
        return "Name: " + self.name + "," + \
            "Dealer id: " + self.dealer_id + "," + \
            "Type: " + self.type + "," + \
            "Year: " + self.year + "," + \
            "Car Make: " + self.car_make 



# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer(models.Model):
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip
    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview(models.Model):
    dealership = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    purchase = models.CharField(max_length=30)
    review = models.CharField(null=False ,max_length=30)
    purchase_date = models.DateField(null=True)
    car_make = models.CharField(max_length=30)
    car_model = models.CharField(max_length=30)
    car_year = models.DateField(null=True)
    sentiment = models.CharField(max_length=30)
    id = models.CharField(primary_key=True,max_length=30)
    def __str__(self):
        return "DealerReview: " + self.review