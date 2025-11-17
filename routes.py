from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from database import SessionLocal
from models import User, Product, EditedItem, QuickToken, PasswordReset
from utils import hash_password, verify_password, create_access_token, generate_quick_token, read_dados_json, SECRET_KEY, ALGORITHM

from sqlalchemy.orm import Session

router = APIRouter()

class RegisterSchema(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    funcao: str
    cpf: str
    idade: int | None = None

class LoginSchema(BaseModel):
    email: EmailStr
    senha: str

class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post('/auth/register')
def register(payload: RegisterSchema, db: Session = Depends(get_db)):

    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail='Email já cadastrado')
    if db.query(User).filter(User.cpf == payload.cpf).first():
        raise HTTPException(status_code=400, detail='CPF já cadastrado')

    user = User(
        nome=payload.nome,
        idade=payload.idade,
        funcao=payload.funcao,
        email=payload.email,
        senha_hash=hash_password(payload.senha),
        cpf=payload.cpf
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": user.email, "id": user.id})

    return {
        "nome": user.nome,
        "hora": datetime.utcnow().isoformat(),
        "confirmado": "sim",
        "token": token
    }

@router.post('/auth/login')
def login(payload: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.senha, user.senha_hash):
        raise HTTPException(status_code=401, detail='Credenciais inválidas')

    token = create_access_token({"sub": user.email, "id": user.id})
    return {"access_token": token, "token_type": "bearer"}


@router.post('/token_acesso_rapido')
def gerar_token_rapido(email: EmailStr = Body(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail='Usuário não encontrado')

    codigo = generate_quick_token(7)
    agora = datetime.utcnow()
    expira = agora + timedelta(hours=6)

    qt = QuickToken(
        nome=user.nome,
        email=user.email,
        senha_hash=user.senha_hash,
        codigo=codigo,
        criado_em=agora,
        expira_em=expira
    )
    db.add(qt)
    db.commit()
    db.refresh(qt)

    return {"token_rapido": codigo, "expira_em": expira.isoformat()}


@router.get('/auth/troca_senha')
def troca_senha(email: EmailStr, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail='Usuário não encontrado')

    token = generate_quick_token(20)
    pr = PasswordReset(nome=user.nome, email=user.email, token_troca=token)
    db.add(pr)
    db.commit()
    db.refresh(pr)


    dados = read_dados_json()
    return {"email": user.email, "token": token, "senha_anterior": ""}

def validar_token_rapido(db: Session, codigo: str) -> QuickToken | None:
    qt = db.query(QuickToken).filter(QuickToken.codigo == codigo).first()
    if not qt:
        return None
    if qt.expira_em < datetime.utcnow():
        return None
    return qt


@router.delete('/APISocket/{token}/deletar_produto/{product_id}')
def deletar_proto(token: str, product_id: int, db: Session = Depends(get_db)):
    qt = validar_token_rapido(db, token)
    if not qt:
        raise HTTPException(status_code=401, detail='Token rápido inválido ou expirado')

    produto = db.query(Product).filter(Product.id == product_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail='Produto não encontrado')

    db.delete(produto)
    db.commit()

    edit = EditedItem(id_informacoes=str(product_id), token_item=produto.token_produto, informacoes_editadas='DELETADO')
    db.add(edit)
    db.commit()
    return {"detalhe": "Produto removido"}

@router.get('/APISocket/{token}/listar_produtos')
def listar_produtos(token: str, db: Session = Depends(get_db)):
    qt = validar_token_rapido(db, token)
    if not qt:
        raise HTTPException(status_code=401, detail='Token rápido inválido ou expirado')
    produtos = db.query(Product).all()
    res = []
    for p in produtos:
        res.append({
            "id": p.id,
            "nome": p.nome,
            "data_criacao": p.data_criacao.isoformat(),
            "preco": p.preco,
            "volume": p.volume,
            "validade": p.validade
        })
    return res

@router.get('/APISocket/{token}/listar_produtos')
def listar_produtos(token: str, db: Session = Depends(get_db)):
    qt = validar_token_rapido(db, token)
    if not qt:
        raise HTTPException(status_code=401, detail='Token rápido inválido ou expirado')
    produtos = db.query(Product).all()
    res = []
    for p in produtos:
        res.append({
            "id": p.id,
            "nome": p.nome,
            "data_criacao": p.data_criacao.isoformat(),
            "preco": p.preco,
            "volume": p.volume,
            "validade": p.validade
        })
    return res