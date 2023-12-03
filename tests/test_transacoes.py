from unittest import TestCase
from app.models.filial_model import FilialModel
from app.models.fornecedor_model import FornecedorModel
from app.models.produto_model import ProdutoModel
from app.views.produto_view import ProdutoView
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, engine, Base
from parameterized import parameterized

client = TestClient(app)


class TestTransacao(TestCase):
    def setUp(self):
        Base.metadata.create_all(bind=engine)
        self.db = SessionLocal()

        fornecedor = FornecedorModel(nome="Nome do Fornecedor")
        filialA = FilialModel(nome="Filial", endereco="Rua A",
                              telefone="(11)1111-1111")
        filialB = FilialModel(nome="FilialB", endereco="Rua B",
                              telefone="(22)2222-2222")
        produtoA = ProdutoModel(descricao="Produto Teste", codigo_barras="QWERTY",
                                custo=1.0, preco_venda=5.0, quantidade_disponivel=10, filial_id=1)
        produtoB = ProdutoModel(descricao="Produto Teste", codigo_barras="QWERTY",
                                custo=1.0, preco_venda=5.0, quantidade_disponivel=10, filial_id=2)

        self.db.add(fornecedor)
        self.db.add(filialA)
        self.db.add(filialB)
        self.db.add(produtoA)
        self.db.add(produtoB)

        self.db.commit()

    @parameterized.expand([
        (5, "QWERTY", 1, 1),
        (10, "QWERTY", 1, 1),
        (15, "QWERTY", 1, 2),
    ])
    def test_recebimento(self, quantidade, codigo_barras, fornecedor_id, filial_id):
        transacao_view = ProdutoView()

        transacao_data = {
            "quantidade": quantidade,
            "codigo_barras": codigo_barras,
            "fornecedor_id": fornecedor_id,
            "filial_id": filial_id
        }

        produto = self.db.query(ProdutoModel).filter(
            ProdutoModel.codigo_barras == codigo_barras and ProdutoModel.filial_id == filial_id).first()
        produto.quantidade_disponivel += quantidade

        response = client.post("/transacao/recebimento", json=transacao_data)

        assert response.status_code == 200
        assert response.json() == transacao_view.format_response(produto)

        self.db.close()

    @parameterized.expand([
        (5, "QWERTY", 1),
        (10, "QWERTY", 1),
        (15, "QWERTY", 2),
    ])
    def test_ajuste(self, quantidade, codigo_barras, filial_id):
        transacao_view = ProdutoView()

        transacao_data = {
            "quantidade": quantidade,
            "codigo_barras": codigo_barras,
            "tipo": "ajustes",
            "filial_id": filial_id
        }

        produto = self.db.query(ProdutoModel).filter(
            ProdutoModel.codigo_barras == codigo_barras and ProdutoModel.filial_id == filial_id).first()
        produto.quantidade_disponivel = quantidade

        response = client.post("/transacao", json=transacao_data)

        assert response.status_code == 200
        assert response.json() == transacao_view.format_response(produto)

        self.db.close()

    @parameterized.expand([
        (5, "QWERTY", 1),
        (10, "QWERTY", 1),
        (15, "QWERTY", 2),
    ])
    def test_devolucao(self, quantidade, codigo_barras, filial_id):
        transacao_view = ProdutoView()

        transacao_data = {
            "quantidade": quantidade,
            "codigo_barras": codigo_barras,
            "tipo": "devolucao",
            "filial_id": filial_id
        }

        produto = self.db.query(ProdutoModel).filter(
            ProdutoModel.codigo_barras == codigo_barras and ProdutoModel.filial_id == filial_id).first()
        produto.quantidade_disponivel += quantidade

        response = client.post("/transacao", json=transacao_data)

        assert response.status_code == 200
        assert response.json() == transacao_view.format_response(produto)

        self.db.close()

    @parameterized.expand([
        (5, "QWERTY", 1),
        (10, "QWERTY", 1),
        (15, "QWERTY", 2),
    ])
    def test_venda(self, quantidade, codigo_barras, filial_id):
        transacao_view = ProdutoView()

        transacao_data = {
            "quantidade": quantidade,
            "codigo_barras": codigo_barras,
            "tipo": "venda",
            "filial_id": filial_id
        }

        produto = self.db.query(ProdutoModel).filter(
            ProdutoModel.codigo_barras == codigo_barras and ProdutoModel.filial_id == filial_id).first()
        produto.quantidade_disponivel -= quantidade

        response = client.post("/transacao", json=transacao_data)

        assert response.status_code == 200
        assert response.json() == transacao_view.format_response(produto)

        self.db.close()

    @parameterized.expand([
        (5, "QWERTY", 1, 2),
        (10, "QWERTY", 1, 2),
        (15, "QWERTY", 2, 1),
    ])
    def test_transferencia(self, quantidade, codigo_barras, filial_origem, filial_destino):
        transacao_view = ProdutoView()

        transacao_data = {
            "quantidade": quantidade,
            "codigo_barras": codigo_barras,
            "filial_origem": filial_origem,
            "filial_destino": filial_destino
        }

        produto_origem = self.db.query(ProdutoModel).filter(
            ProdutoModel.codigo_barras == codigo_barras and ProdutoModel.filial_id == filial_origem).first()
        produto_destino = self.db.query(ProdutoModel).filter(
            ProdutoModel.codigo_barras == codigo_barras and ProdutoModel.filial_id == filial_destino).first()

        produto_origem.quantidade_disponivel -= quantidade
        produto_destino.quantidade_disponivel += quantidade

        response = client.post("/transacao/transferencia", json=transacao_data)

        produtos = []
        produtos.append(produto_origem)
        produtos.append(produto_destino)

        assert response.status_code == 200
        assert response.json() == [transacao_view.format_response(
            produto_model) for produto_model in produtos]

        self.db.close()

    def test_recebimento_negativo(self):

        transacao_data = {
            "quantidade": -5,
            "codigo_barras": "QWERTY",
            "fornecedor_id": 1,
            "filial_id": 1
        }

        response = client.post("/transacao/recebimento", json=transacao_data)

        assert response.status_code == 400
        assert response.json() == {
            "detail": "Quantidade da transação não deve ser menor que zero."}

        self.db.close()

    def test_transferencia_negativa(self):

        transacao_data = {
            "quantidade": -5,
            "codigo_barras": "QWERTY",
            "filial_origem": 1,
            "filial_destino": 2
        }

        response = client.post("/transacao/transferencia", json=transacao_data)

        assert response.status_code == 400
        assert response.json() == {
            "detail": "Quantidade da transação não deve ser menor que zero."}

        self.db.close()

    def test_devolucao_negativa(self):

        transacao_data = {
            "quantidade": -5,
            "codigo_barras": "QWERTY",
            "tipo": "devolucao",
            "filial_id": 1
        }

        response = client.post("/transacao", json=transacao_data)

        assert response.status_code == 400
        assert response.json() == {
            "detail": "Quantidade da transação não deve ser menor que zero."}

        self.db.close()

    def test_venda_negativa(self):

        transacao_data = {
            "quantidade": -5,
            "codigo_barras": "QWERTY",
            "tipo": "venda",
            "filial_id": 1
        }

        response = client.post("/transacao", json=transacao_data)

        assert response.status_code == 400
        assert response.json() == {
            "detail": "Quantidade da transação não deve ser menor que zero."}

        self.db.close()
