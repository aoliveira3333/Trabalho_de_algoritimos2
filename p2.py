import pandas as pd
import struct
import os

caminho_csv = r"C:\Users\olive\Downloads\Trabalho algortimos\jewelry.csv"
pasta = os.path.dirname(caminho_csv)
caminho_saida = os.path.join(pasta, "compras.dat")

df = pd.read_csv(caminho_csv, header=None)
df.columns = [
    "data", "id_pedido", "id_produto", "quantidade", "id_categoria", 
    "categoria", "genero", "preco", "id_usuario", 
    "col9", "material", "col11", "pedra"
]

dados_compras = df[["id_pedido", "id_produto", "id_usuario", "quantidade", "preco", "data"]]
dados_compras = dados_compras.fillna(0)

dados_compras["id_pedido"] = dados_compras["id_pedido"].astype(str)
dados_compras["id_produto"] = dados_compras["id_produto"].astype(str)
dados_compras["id_usuario"] = dados_compras["id_usuario"].astype(str)
dados_compras["quantidade"] = dados_compras["quantidade"].astype(int)
dados_compras["preco"] = dados_compras["preco"].astype(float)
dados_compras["data"] = dados_compras["data"].astype(str)

dados_compras = dados_compras.drop_duplicates(subset=["id_pedido"])
dados_compras = dados_compras.sort_values('id_pedido')

with open(caminho_saida, "wb") as arquivo:
    for _, linha in dados_compras.iterrows():
        id_pedido = str(linha["id_pedido"]).ljust(15)[:15]
        id_produto = str(linha["id_produto"]).ljust(15)[:15]
        id_usuario = str(linha["id_usuario"]).ljust(15)[:15]
        quantidade = int(linha["quantidade"])
        preco = float(linha["preco"])
        data = str(linha["data"]).ljust(20)[:20]
        
        registro = struct.pack(
            "15s15s15sid20s",
            id_pedido.encode('utf-8'),
            id_produto.encode('utf-8'),
            id_usuario.encode('utf-8'),
            quantidade,
            preco,
            data.encode('utf-8')
        )
        arquivo.write(registro)

print("Arquivo 'compras.dat' criado!")
print(f"Registros: {len(dados_compras)}")
print(f"Local: {caminho_saida}")
print(f"Tamanho do arquivo: {os.path.getsize(caminho_saida)} bytes")