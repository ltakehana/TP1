

class DescricaoEmBrancoException(Exception):
    def __init__(self, message="Descrição, código de barras, custo, preço de venda e quantidade disponível são obrigatórios."):
        self.message = message
        super().__init__(self.message)