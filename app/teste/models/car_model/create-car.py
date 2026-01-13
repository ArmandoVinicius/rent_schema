from ....models.car_model import CarModel

# Para funcionar, deve existir um modelo com ID 1 no banco de dados 
CarModel().create_car("ABC1234", "ADSA6S5SADA7TD", "Azul", 2005, 123456, "Disponível", 2005, 1)