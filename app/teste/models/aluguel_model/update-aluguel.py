from ....models.aluguel_model import AluguelModel

# Para funcionar, deve existir um cliente com ID 1, um carro com placa "ABC1234" e um funcionário com matrícula 1 no banco de dados
AluguelModel().create_aluguel("2024-01-20 10:00:00", "2024-01-25 18:00:00", 500.00, None, 1, "ABC1234", 1)
AluguelModel().update_aluguel(1, "Valor_Total", 600.00)
