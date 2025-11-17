from fastapi import FastAPI
import uvicorn
from routes import router

app = FastAPI(title="API de Gestão de Produtos")
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="192.168.0.8", port=8000, reload=True)
