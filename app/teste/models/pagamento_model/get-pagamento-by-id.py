from ....models.pagamento_model import PagamentoModel

# Para funcionar, deve existir um aluguel com ID 1 no banco de dados
PagamentoModel().create_pagamento(500.00, "2024-01-20", "Cartão de Crédito", 1)

if PagamentoModel().get_pagamento_by_id(1):
  print("Pagamento exists")
else:
  print("Pagamento doesn't exist")
