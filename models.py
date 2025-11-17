from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    idade = Column(Integer, nullable=True)
    data_cadastro = Column(DateTime, default=datetime.utcnow)
    funcao = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    senha_hash = Column(String, nullable=False)
    cpf = Column(String, unique=True, nullable=False)

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    data_criacao = Column(DateTime, default=datetime.utcnow)
    id_informacoes = Column(String, nullable=True)
    token_produto = Column(String, unique=True, nullable=False)
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
    senha_hash = Column(String, nullable=False)
    codigo = Column(String, nullable=False) 
    criado_em = Column(DateTime, default=datetime.utcnow)
    expira_em = Column(DateTime, nullable=False)

class PasswordReset(Base):
    __tablename__ = 'password_resets'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False)
    token_troca = Column(String, nullable=False)
    criado_em = Column(DateTime, default=datetime.utcnow)
    usado_em = Column(DateTime, nullable=True)
