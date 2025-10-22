import pandas as pd
import os

caminho_csv = r"C:\Users\olive\Downloads\Trabalho algortimos\jewelry.csv"
pasta = os.path.dirname(caminho_csv)
caminho_saida = os.path.join(pasta, "joias.dat")

df = pd.read_csv(caminho_csv, header=None)
df.columns = [
    "data", "id_pedido", "id_produto", "quantidade", "id_categoria", 
    "categoria", "genero", "preco", "id_usuario", 
    "col9", "material", "col11", "pedra"
]

dados_joias = df[["id_produto", "categoria", "material", "pedra"]]
dados_joias = dados_joias.fillna("")

dados_joias["id_produto"] = dados_joias["id_produto"].astype(str)
dados_joias["categoria"] = dados_joias["categoria"].astype(str)
dados_joias["material"] = dados_joias["material"].astype(str)
dados_joias["pedra"] = dados_joias["pedra"].astype(str)

dados_joias = dados_joias.sort_values('id_produto')

with open(caminho_saida, "wb") as arquivo:
    for _, linha in dados_joias.iterrows():
        registro = (
            str(linha["id_produto"]).ljust(20)[:20] +
            str(linha["categoria"]).ljust(20)[:20] +
            str(linha["material"]).ljust(10)[:10] +
            str(linha["pedra"]).ljust(10)[:10]
        )
        arquivo.write(registro.encode("utf-8"))

print("Arquivo criado")
print(f"Registros: {len(dados_joias)}")
print(f"Local: {caminho_saida}")