import requests

def ListProductApi():
    url = "https://dummyjson.com/products"
    response = requests.get(url)
    response.raise_for_status() 
    return response.json()["products"]

def SelectionObject(produtos, campos):
    return [
        {campo: produto.get(campo) for campo in campos}
        for produto in produtos
    ]

def resultResulme():
        campos_necessarios = ["id", "title", "price", "brand", "thumbnail"]
        return SelectionObject(ListProductApi(), campos_necessarios)


import requests

def buscar_produtos():
    url = "https://dummyjson.com/products"
    response = requests.get(url)
    data = response.json()["products"]

    campos = ["title", "thumbnail", "stock"]

    produtos_filtrados = []
    for p in data:
        produtos_filtrados.append({
            "nome": p["title"],
            "imagem": p["thumbnail"],
            "quantidade": p["stock"],
        })

    return produtos_filtrados
