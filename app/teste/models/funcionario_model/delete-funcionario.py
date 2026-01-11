from ....models.funcionario_model import FuncionarioModel

FuncionarioModel().create_funcionario("João Silva", "2024-01-15", "Gerente")

FuncionarioModel().delete_funcionario(1)

if FuncionarioModel().get_funcionario_by_matricula(1):
  print("Funcionario exists")
else:
  print("Funcionario doesn't exist")
