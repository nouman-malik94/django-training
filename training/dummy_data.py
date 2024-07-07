import random
from faker import Faker
from .models import CatCity, CatTrainingType, Training, Resource

fake = Faker()

# Create dummy data for CatCity model
def create_cat_city():
    name = fake.city()
    abbreviation = fake.word()[:10]
    CatCity.objects.create(name=name, abbreviation=abbreviation)

# Create dummy data for CatTrainingType model
def create_cat_training_type():
    name = fake.job()
    abbreviation = fake.word()[:10]
    CatTrainingType.objects.create(name=name, abbreviation=abbreviation)

# Create dummy data for Training model
def create_training():
    name = fake.word()
    type = random.choice(CatTrainingType.objects.all())
    date_start = fake.date_this_century(before_today=True, after_today=False)
    date_end = fake.date_between(start_date=date_start, end_date='+2y')
    city = random.choice(CatCity.objects.all())
    street_address = fake.street_address()
    training = Training.objects.create(name=name, type=type, date_start=date_start,
        date_end=date_end, city=city, street_address=street_address)
    # Add resources to the training
    for _ in range(random.randint(1, 5)):
        resource = create_resource()
        training.resources.add(resource)

# Create dummy data for Resource model
def create_resource():
    name = fake.name()
    dob = fake.date_of_birth()
    pin = fake.random_int(min=100000, max=999999)
    father_name = fake.name()
    cnic = fake.random_int(min=1000000000000, max=9999999999999)
    return Resource.objects.create(name=name, dob=dob, pin=pin, father_name=father_name, CNIC=cnic)

# Generate 10 dummy data for each model
for _ in range(10):
    create_cat_city()
    create_cat_training_type()
    create_training()
