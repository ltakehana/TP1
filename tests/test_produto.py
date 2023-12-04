from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, engine, Base
from app.views.produto_view import ProdutoView
from app.schemas.produto_schema import ProdutoSchema,ProdutoCreationSchema
from app.models.produto_model import ProdutoModel
from app.schemas.fornecedor_schema import FornecedorSchema
from app.models.fornecedor_model import FornecedorModel

client = TestClient(app)

def setup_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    fornecedor_data = FornecedorSchema(
    nome= "Fornecedor A",
    endereco= "Rua A",
    telefone= "61 9 9999-9999"
    )

    fornecedor = FornecedorModel(**fornecedor_data.dict())
    db.add(fornecedor)
    db.commit()
    db.refresh(fornecedor)

    return db, fornecedor


def test_cadastrar_produto():
    db, fornecedor = setup_db()

    produto_data = {
        "descricao": "Produto Teste 1",
        "codigo_barras": "123456789",
        "custo": 10.0,
        "preco_venda": 20.0,
        "quantidade_disponivel": 50,
        "lote": 1232132,
        "validade":"05/2023",
        "quantidade_minima": 1,
        "fornecedor_id": fornecedor.id
    }

    response = client.post("/produto/", json=produto_data)


    produto_data = {
        "descricao": "Produto Teste 1",
        "codigo_barras": "123456789",
        "custo": 10.0,
        "preco_venda": 20.0,
        "quantidade_disponivel": 50,
        "fornecedor_id": fornecedor.id,
        "quantidade_minima": 1
    }

    assert response.status_code == 200
    assert response.json() == produto_data

    db.close()


def test_cadastrar_produto_com_descricao_em_branco():
    db, fornecedor = setup_db()

    produto_data = {
        "descricao": "",  # Descrição em branco
        "codigo_barras": "123456789",
        "custo": 10.0,
        "preco_venda": 20.0,
        "quantidade_disponivel": 50,
        "lote": 1232132,
        "validade":"05/2023",
        "fornecedor_id": fornecedor.id
    }

    response = client.post("/produto/", json=produto_data)

    assert response.status_code == 400
    assert response.json() == {"detail":"Descrição, código de barras, custo, preço de venda e quantidade disponível são obrigatórios."}
    db.close()

def test_cadastrar_produto_com_valores_invalidos():
    db, fornecedor = setup_db()

    produto_data = {
        "descricao": "Produto Teste 2",
        "codigo_barras": "123456789",
        "custo": -5.0,  # Valor inválido
        "preco_venda": 0.0,  # Valor inválido
        "lote": 1232132,
        "validade":"05/2023",
        "quantidade_disponivel": -10,  # Valor inválido
        "fornecedor_id": fornecedor.id
    }

    response = client.post("/produto/", json=produto_data)

    assert response.status_code == 400
    assert response.json() == {"detail":"Custo, preço de venda e quantidade disponível devem ser maiores que zero."}


    db.close()


def test_consultar_produto():
    db, fornecedor = setup_db()

    produto = ProdutoSchema(
        codigo_barras= "111 000 010 11",
        custo= 50.00,
        descricao="Produto Teste 3",
        preco_venda= 80.00,
        quantidade_disponivel= 10,
        fornecedor_id= fornecedor.id
    )

    produto_db = ProdutoModel(**produto.dict())
    db.add(produto_db)
    db.commit()
    db.refresh(produto_db)

    response = client.get('produto/' + produto_db.codigo_barras + '/')

    produto_view = ProdutoView()

    assert response.status_code == 200
    assert response.json() == produto_view.format_response(produto)

    db.close()


def test_consultar_produto():
    db, fornecedor = setup_db()

    produto = ProdutoSchema(
        codigo_barras= "111 000 010 11",
        custo= 50.00,
        descricao="Produto Teste 4",
        preco_venda= 80.00,
        quantidade_disponivel= 10,
        fornecedor_id= fornecedor.id
    )

    produto_db = ProdutoModel(**produto.dict())
    db.add(produto_db)
    db.commit()
    db.refresh(produto_db)

    response = client.get('produto/' + produto_db.codigo_barras + '/')

    produto_view = ProdutoView()

    assert response.status_code == 200
    assert response.json() == produto_view.format_response(produto)

    db.close()


def test_consultar_produto_codigo_barras1():
    db, fornecedor = setup_db()

    produto = ProdutoSchema(
        codigo_barras= "111 000 010 11 1",
        custo= 50.00,
        descricao="Produto Teste 5",
        preco_venda= 80.00,
        quantidade_disponivel= 10,
        fornecedor_id= fornecedor.id
    )

    produto_db = ProdutoModel(**produto.dict())
    db.add(produto_db)
    db.commit()
    db.refresh(produto_db)

    response = client.get('produto/' + produto_db.codigo_barras + '/')

    produto_view = ProdutoView()

    assert response.status_code == 200
    assert response.json() == produto_view.format_response(produto)

    db.close()

def test_consultar_produto_codigo_barras2():
    db, fornecedor = setup_db()

    produto = ProdutoSchema(
        codigo_barras= "111 000 01002",
        custo= 50.00,
        descricao="Produto Teste 6",
        preco_venda= 80.00,
        quantidade_disponivel= 10,
        fornecedor_id= fornecedor.id
    )

    produto_db = ProdutoModel(**produto.dict())
    db.add(produto_db)
    db.commit()
    db.refresh(produto_db)

    response = client.get('produto/' + produto_db.codigo_barras + '/')

    produto_view = ProdutoView()

    assert response.status_code == 200
    assert response.json() == produto_view.format_response(produto)

    db.close()

def test_consultar_produto_descricao():
    db, fornecedor = setup_db()

    produto = ProdutoSchema(
        codigo_barras= "111 000 010 11",
        custo= 50.00,
        descricao="Produto Teste 7",
        preco_venda= 80.00,
        quantidade_disponivel= 10,
        fornecedor_id= fornecedor.id
    )

    produto_db = ProdutoModel(**produto.dict())
    db.add(produto_db)
    db.commit()
    db.refresh(produto_db)

    response = client.get('produto/' + produto_db.descricao + '/')

    produto_view = ProdutoView()

    assert response.status_code == 200
    assert response.json() == produto_view.format_response(produto)

    db.close()


def test_consultar_produto_sem_descricao():
    db, fornecedor = setup_db()

    produto = ProdutoSchema(
        codigo_barras= "111 000 000 000",
        custo= 100.00,
        descricao="",
        preco_venda= 120.00,
        quantidade_disponivel= 10,
        fornecedor_id= fornecedor.id
    )

    produto_db = ProdutoModel(**produto.dict())
    db.add(produto_db)
    db.commit()
    db.refresh(produto_db)

    response = client.get('estoque/' + produto_db.codigo_barras + '/')
    produto_view = ProdutoView()

    assert response.status_code == 400
    assert response.json() == {"detail":"Descrição, código de barras, custo, preço de venda e quantidade disponível são obrigatórios."}

    db.close()


def test_consultar_produto_Codigo_Incorreto():
    db, fornecedor = setup_db()

    produto = ProdutoSchema(
        codigo_barras= "99 000 9 11",
        custo= 50.00,
        descricao="Produto Teste 9",
        preco_venda= 80.00,
        quantidade_disponivel= 10,
        fornecedor_id= fornecedor.id
    )

    produto_db = ProdutoModel(**produto.dict())
    db.add(produto_db)
    db.commit()
    db.refresh(produto_db)

    response = client.get('produto/234023423424/')

    produto_view = ProdutoView()

    assert response.status_code == 400
    assert response.json() == {"detail":"Não foi encontrado nenhum seletor com tal id."}

    db.close()
