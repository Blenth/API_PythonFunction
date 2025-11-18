from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    senha = Column(String, nullable=False)  # ← senha simples
    idade = Column(Integer, nullable=True)
    funcao = Column(String, nullable=True)
    cpf = Column(String, unique=True, nullable=True)
    data_cadastro = Column(DateTime, default=datetime.utcnow)


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    data_criacao = Column(DateTime, default=datetime.utcnow)
    id_informacoes = Column(String, nullable=True)
    token_produto = Column(String, unique=True, nullable=True)
    preco = Column(Float, nullable=True)
    volume = Column(String, nullable=True)
    validade = Column(String, nullable=True)

class EditedItem(Base):
    __tablename__ = 'edited_items'
    id = Column(Integer, primary_key=True, index=True)
    data_edicao = Column(DateTime, default=datetime.utcnow)
    id_informacoes = Column(String, nullable=True)
    token_item = Column(String, nullable=False)
    informacoes_editadas = Column(Text, nullable=True)

class QuickToken(Base):
    __tablename__ = 'quick_tokens'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False)
    codigo = Column(String, nullable=False)
    criado_em = Column(DateTime, default=datetime.utcnow)
    expira_em = Column(DateTime, nullable=False)
