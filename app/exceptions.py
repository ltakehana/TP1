

class DescricaoEmBrancoException(Exception):
    def __init__(self, message="Descrição, código de barras, custo, preço de venda e quantidade disponível são obrigatórios."):
        self.message = message
        super().__init__(self.message)

class ValorInvalidoException(Exception):
    def __init__(self, message="Custo, preço de venda e quantidade disponível devem ser maiores que zero."):
        self.message = message
        super().__init__(self.message)

class ValorIdNaoEncontrado(Exception):
    def __init__(self, message="Não foi encontrado nenhum seletor com tal id."):
        self.message = message
        super().__init__(self.message)


class FaltaLoteException(Exception):
    def __init__(self, message="É necessário especificar um lote"):
        self.message = message
        super().__init__(self.message)

class CampoObrigatorioException(Exception):
    def __init__(self, message="Campo obrigatório não fornecido."):
        self.message = message
        super().__init__(self.message)

class EstoqueNegativoException(Exception):
    def __init__(self, message="O valor do estoque não pode ser menor que zero."):
        self.message = message
        super().__init__(self.message)
