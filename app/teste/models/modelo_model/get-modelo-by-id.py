from ....models.modelo_model import ModeloModel

ModeloModel().create_modelo("Sedan Compacto", "Toyota", "Econômico")

if ModeloModel().get_modelo_by_id(1):
  print("Modelo exists")
else:
  print("Modelo doesn't exist")
