from django.db import transaction
from .models import CarMake, CarModel


@transaction.atomic
def initiate():
    car_make_data = [
        ("NISSAN", "Great cars. Japanese technology", 1,
         [("Pathfinder", "SUV"), ("Qashqai", "SUV"), ("XTRAIL", "SUV")]),
        ("Mercedes", "Great cars. German technology", 2,
         [("A-Class", "SUV"), ("C-Class", "SUV"), ("E-Class", "SUV")]),
        ("Audi", "Great cars. German technology", 3,
         [("A4", "SUV"), ("A5", "SUV"), ("A6", "SUV")]),
        ("Kia", "Great cars. Korean technology", 4,
         [("Sorrento", "SUV"), ("Carnival", "SUV"), ("Cerato", "Sedan")]),
        ("Toyota", "Great cars. Japanese technology", 5,
         [("Corolla", "Sedan"), ("Camry", "Sedan"), ("Kluger", "SUV")]),
    ]

    for name, description, dealer_id, car_models in car_make_data:
        car_make, _ = CarMake.objects.get_or_create(
            name=name, defaults={"description": description}
        )
        for model_name, car_type in car_models:
            CarModel.objects.get_or_create(
                name=model_name,
                car_make=car_make,
                year=2023,
                defaults={"type": car_type, "dealer_id": dealer_id},
            )
