import struct
import os
from collections import defaultdict

ARQUIVO_COMPRAS = r"C:\Users\olive\Downloads\Trabalho algortimos\compras.dat"
ARQUIVO_INDICE = "indice_compras.idx"
FORMATO_REGISTRO = "15s15s15sid20s"
TAMANHO_REGISTRO = struct.calcsize(FORMATO_REGISTRO)
contador_operacoes = 0
RECONSTRUIR_APOS = 3

def analise_produtos_lideres():
    if not os.path.exists(ARQUIVO_COMPRAS):
        print("Arquivo de compras nao encontrado!")
        return []
    vendas_por_produto = defaultdict(int)
    total_vendido = 0
    with open(ARQUIVO_COMPRAS, "rb") as f:
        while True:
            registro = f.read(TAMANHO_REGISTRO)
            if not registro:
                break
            try:
                order_id_bytes, product_id_bytes, user_id_bytes, quantity, price, date_bytes = struct.unpack(FORMATO_REGISTRO, registro)
                product_id = product_id_bytes.decode('utf-8', errors='ignore').strip()
                vendas_por_produto[product_id] += quantity
                total_vendido += quantity
            except (ValueError, struct.error):
                pass
    if total_vendido == 0:
        print("Nenhuma compra registrada para analise!")
        return []
    print(f"\nANALISE: Produtos Lideres de Vendas")
    print(f"Total de produtos vendidos: {total_vendido}")
    print(f"Produtos distintos: {len(vendas_por_produto)}")
    print("-" * 50)
    produtos_ordenados = sorted(vendas_por_produto.items(), key=lambda x: x[1], reverse=True)
    lideres = []
    for i, (produto, qtd) in enumerate(produtos_ordenados[:5], 1):
        percentual = (qtd / total_vendido) * 100
        print(f"Top {i}: Produto {produto:<10} - {qtd:>3} unidades ({percentual:5.1f}%)")
        if percentual > 20:
            lideres.append((produto, qtd, percentual))
    if lideres:
        print(f"RESPOSTA: SIM - {len(lideres)} produto(s) lider(es) encontrado(s)")
        for produto, qtd, perc in lideres:
            print(f"   Produto {produto}: {qtd} unidades ({perc:.1f}% do total)")
        return lideres
    else:
        print(f"RESPOSTA: NAO - Nenhum produto domina as vendas (mais de 20%)")
        return []

def analise_sazonalidade_vendas():
    if not os.path.exists(ARQUIVO_COMPRAS):
        print("Arquivo de compras nao encontrado!")
        return False
    vendas_por_mes = defaultdict(int)
    total_vendido = 0
    with open(ARQUIVO_COMPRAS, "rb") as f:
        while True:
            registro = f.read(TAMANHO_REGISTRO)
            if not registro:
                break
            try:
                order_id_bytes, product_id_bytes, user_id_bytes, quantity, price, date_bytes = struct.unpack(FORMATO_REGISTRO, registro)
                data_str = date_bytes.decode('utf-8', errors='ignore').strip()
                try:
                    if '-' in data_str:
                        mes = int(data_str.split('-')[1])
                        vendas_por_mes[mes] += quantity
                        total_vendido += quantity
                except (IndexError, ValueError):
                    pass
            except (ValueError, struct.error):
                pass
    if total_vendido == 0:
        print("Nenhuma compra registrada para analise!")
        return False
    print(f"\nANALISE: Sazonalidade das Vendas")
    print(f"Total de produtos vendidos: {total_vendido}")
    print(f"Periodo analisado: {len(vendas_por_mes)} meses distintos")
    print("-" * 50)
    meses_ordenados = sorted(vendas_por_mes.items())
    for mes, qtd in meses_ordenados:
        percentual = (qtd / total_vendido) * 100
        nome_mes = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
                   'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'][mes-1] if 1 <= mes <= 12 else f'Mes {mes}'
        print(f"{nome_mes:<4}: {qtd:>3} unidades ({percentual:5.1f}%)")
    if vendas_por_mes:
        mes_pico, qtd_pico = max(vendas_por_mes.items(), key=lambda x: x[1])
        percentual_pico = (qtd_pico / total_vendido) * 100
        nome_mes_pico = ['Janeiro', 'Fevereiro', 'Marco', 'Abril', 'Maio', 'Junho',
                        'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'][mes_pico-1] if 1 <= mes_pico <= 12 else f'Mes {mes_pico}'
        print(f"Mes de pico: {nome_mes_pico} com {percentual_pico:.1f}% das vendas")
        if percentual_pico > 30:
            print(f"RESPOSTA: SIM - Ha sazonalidade marcante em {nome_mes_pico}")
            return True
        else:
            print(f"RESPOSTA: NAO - As vendas estao distribuidas ao longo do ano")
            return False
    return False

def analise_usuarios_fieis():
    if not os.path.exists(ARQUIVO_COMPRAS):
        print("Arquivo de compras nao encontrado!")
        return []
    compras_por_usuario = defaultdict(list)
    with open(ARQUIVO_COMPRAS, "rb") as f:
        while True:
            registro = f.read(TAMANHO_REGISTRO)
            if not registro:
                break
            try:
                order_id_bytes, product_id_bytes, user_id_bytes, quantity, price, date_bytes = struct.unpack(FORMATO_REGISTRO, registro)
                usuario = user_id_bytes.decode('utf-8', errors='ignore').strip()
                valor_compra = price * quantity
                compras_por_usuario[usuario].append(valor_compra)
            except (ValueError, struct.error):
                pass
    if not compras_por_usuario:
        print("Nenhuma compra registrada para analise!")
        return []
    print(f"\nANALISE: Usuarios com Alto Valor por Compra")
    print(f"Total de usuarios distintos: {len(compras_por_usuario)}")
    print("-" * 50)
    usuarios_valor_medio = []
    for usuario, compras in compras_por_usuario.items():
        valor_total = sum(compras)
        valor_medio = valor_total / len(compras)
        usuarios_valor_medio.append((usuario, valor_medio, len(compras), valor_total))
    usuarios_valor_medio.sort(key=lambda x: x[1], reverse=True)
    usuarios_destaque = []
    limite_alto_valor = 200.0
    print(f"Top 5 usuarios com maior valor medio por compra:")
    for i, (usuario, valor_medio, num_compras, valor_total) in enumerate(usuarios_valor_medio[:5], 1):
        status = "ALTO VALOR" if valor_medio > limite_alto_valor else ""
        print(f"Top {i}: Usuario {usuario:<8} - ${valor_medio:>7.2f} medios ({num_compras} compras) {status}")
        if valor_medio > limite_alto_valor:
            usuarios_destaque.append((usuario, valor_medio, num_compras, valor_total))
    if usuarios_destaque:
        print(f"RESPOSTA: SIM - {len(usuarios_destaque)} usuario(s) com alto valor medio (>${limite_alto_valor})")
        for usuario, valor_medio, num_compras, valor_total in usuarios_destaque:
            print(f"   Usuario {usuario}: ${valor_medio:.2f} medios por compra")
        return usuarios_destaque
    else:
        print(f"RESPOSTA: NAO - Nenhum usuario com valor medio muito alto")
        return []

def inserir_compra(id_pedido, id_produto, id_usuario, quantidade, preco, data):
    global contador_operacoes
    if compra_existe(id_pedido):
        print(f"Erro: Pedido com ID {id_pedido} ja existe!")
        return False
    order_id = str(id_pedido).ljust(15)[:15]
    product_id = str(id_produto).ljust(15)[:15]
    user_id = str(id_usuario).ljust(15)[:15]
    try:
        qtd = int(quantidade)
        preco_val = float(preco)
    except ValueError:
        print("Erro: Quantidade deve ser inteiro e preco deve ser float!")
        return False
    data_str = str(data).ljust(20)[:20]
    novo_registro = struct.pack(FORMATO_REGISTRO,
                                order_id.encode('utf-8'),
                                product_id.encode('utf-8'),
                                user_id.encode('utf-8'),
                                qtd,
                                preco_val,
                                data_str.encode('utf-8'))
    registros = []
    with open(ARQUIVO_COMPRAS, "rb") as f:
        while True:
            registro = f.read(TAMANHO_REGISTRO)
            if not registro:
                break
            registros.append(registro)
    pos_inserir = 0
    for i, reg in enumerate(registros):
        order_id_atual = struct.unpack(FORMATO_REGISTRO, reg)[0].decode('utf-8').strip()
        if order_id_atual < order_id:
            pos_inserir = i + 1
        else:
            break
    registros.insert(pos_inserir, novo_registro)
    with open(ARQUIVO_COMPRAS, "wb") as f:
        for reg in registros:
            f.write(reg)
    contador_operacoes += 1
    print(f"Compra {id_pedido} inserida com sucesso na posicao {pos_inserir}!")
    reconstruir_indice_se_necessario()
    return True

def remover_compra(id_pedido):
    global contador_operacoes
    if not os.path.exists(ARQUIVO_COMPRAS):
        print("Arquivo de compras nao existe!")
        return False
    registros = []
    encontrou = False
    id_pedido_str = str(id_pedido)
    with open(ARQUIVO_COMPRAS, "rb") as f:
        while True:
            registro = f.read(TAMANHO_REGISTRO)
            if not registro:
                break
            try:
                order_id_bytes, product_id, user_id, quantity, price, date = struct.unpack(FORMATO_REGISTRO, registro)
                current_id = order_id_bytes.decode('utf-8', errors='ignore').strip()
                if current_id != id_pedido_str:
                    registros.append(registro)
                else:
                    encontrou = True
                    print(f"Pedido {id_pedido} removido!")
            except struct.error:
                registros.append(registro)
    if not encontrou:
        print(f"Pedido {id_pedido} nao encontrado!")
        return False
    with open(ARQUIVO_COMPRAS, "wb") as f:
        for reg in registros:
            f.write(reg)
    contador_operacoes += 1
    reconstruir_indice_se_necessario()
    return True

def compra_existe(id_pedido):
    if not os.path.exists(ARQUIVO_COMPRAS):
        return False
    id_pedido_str = str(id_pedido)
    with open(ARQUIVO_COMPRAS, "rb") as f:
        while True:
            registro = f.read(TAMANHO_REGISTRO)
            if not registro:
                break
            try:
                order_id_bytes, _, _, _, _, _ = struct.unpack(FORMATO_REGISTRO, registro)
                current_id = order_id_bytes.decode('utf-8', errors='ignore').strip()
                if current_id == id_pedido_str:
                    return True
            except struct.error:
                pass
    return False

def reconstruir_indice_se_necessario():
    global contador_operacoes
    if contador_operacoes >= RECONSTRUIR_APOS:
        print("Reconstruindo indice...")
        criar_indice_compras()
        contador_operacoes = 0

def forcar_reconstrucao_indice():
    global contador_operacoes
    criar_indice_compras()
    contador_operacoes = 0
    print("Indice reconstruido!")

def listar_compras():
    if not os.path.exists(ARQUIVO_COMPRAS):
        print("Arquivo de compras vazio.")
        return
    print(f"\n{'ID':<15} | {'Produto':<15} | {'Usuario':<15} | {'Qtd':<10} | {'Preco':<15} | {'Data':<20}")
    print("-" * 100)
    with open(ARQUIVO_COMPRAS, "rb") as f:
        while True:
            registro = f.read(TAMANHO_REGISTRO)
            if not registro:
                break
            try:
                order_id_bytes, product_id_bytes, user_id_bytes, quantity, price, date_bytes = struct.unpack(FORMATO_REGISTRO, registro)
                order_str = order_id_bytes.decode('utf-8', errors='ignore').strip()
                product_str = product_id_bytes.decode('utf-8', errors='ignore').strip()
                user_str = user_id_bytes.decode('utf-8', errors='ignore').strip()
                date_str = date_bytes.decode('utf-8', errors='ignore').strip()
                print(f"{order_str:<15} | {product_str:<15} | {user_str:<15} | {quantity:<10} | ${price:<14.2f} | {date_str:<20}")
            except struct.error:
                pass

def criar_indice_compras():
    if not os.path.exists(ARQUIVO_COMPRAS):
        print("Arquivo de compras nao existe!")
        return
    indices = []
    pos = 0
    with open(ARQUIVO_COMPRAS, "rb") as f:
        while True:
            registro = f.read(TAMANHO_REGISTRO)
            if not registro:
                break
            try:
                order_id_bytes, _, _, _, _, _ = struct.unpack(FORMATO_REGISTRO, registro)
                order_id = order_id_bytes.decode('utf-8', errors='ignore').strip()
                indices.append((order_id, pos))
            except struct.error:
                pass
            pos += TAMANHO_REGISTRO
    if not indices:
        print("Nenhum registro valido!")
        return
    indices.sort(key=lambda x: x[0])
    with open(ARQUIVO_INDICE, "wb") as f:
        passo = max(1, len(indices) // 10)
        for i in range(0, len(indices), passo):
            order_id, pos = indices[i]
            order_bytes = order_id.ljust(15).encode('utf-8')[:15]
            f.write(struct.pack("15si", order_bytes, pos))
    print(f"Indice criado com {len(range(0, len(indices), passo))} entradas")

def buscar_compra(id_pedido):
    if not os.path.exists(ARQUIVO_INDICE):
        print("Indice nao encontrado. Gere o indice primeiro!")
        return
    id_pedido_str = str(id_pedido)
    indices = []
    with open(ARQUIVO_INDICE, "rb") as idx:
        while True:
            idx_bytes = idx.read(19)
            if not idx_bytes:
                break
            try:
                order_bytes, pos = struct.unpack("15si", idx_bytes)
                order_id = order_bytes.decode('utf-8', errors='ignore').strip()
                indices.append((order_id, pos))
            except struct.error:
                pass
    if not indices:
        print("Indice vazio.")
        return
    inicio, fim = 0, len(indices) - 1
    while inicio <= fim:
        meio = (inicio + fim) // 2
        order_idx, pos = indices[meio]
        if order_idx == id_pedido_str:
            with open(ARQUIVO_COMPRAS, "rb") as f:
                f.seek(pos)
                registro = f.read(TAMANHO_REGISTRO)
                if registro:
                    try:
                        order_id_bytes, product_id_bytes, user_id_bytes, quantity, price, date_bytes = struct.unpack(FORMATO_REGISTRO, registro)
                        print(f"PEDIDO ENCONTRADO:")
                        print(f"   ID Pedido: {order_id_bytes.decode().strip()}")
                        print(f"   Produto: {product_id_bytes.decode().strip()}")
                        print(f"   Usuario: {user_id_bytes.decode().strip()}")
                        print(f"   Quantidade: {quantity}")
                        print(f"   Preco: ${price:.2f}")
                        print(f"   Data: {date_bytes.decode().strip()}")
                        return
                    except struct.error:
                        print("Registro corrompido.")
                        return
        elif order_idx < id_pedido_str:
            inicio = meio + 1
        else:
            fim = meio - 1
    print("Pedido nao encontrado no indice. Fazendo busca sequencial...")
    with open(ARQUIVO_COMPRAS, "rb") as f:
        while True:
            registro = f.read(TAMANHO_REGISTRO)
            if not registro:
                break
            try:
                order_id_bytes, product_id_bytes, user_id_bytes, quantity, price, date_bytes = struct.unpack(FORMATO_REGISTRO, registro)
                current_id = order_id_bytes.decode('utf-8', errors='ignore').strip()
                if current_id == id_pedido_str:
                    print(f"PEDIDO ENCONTRADO:")
                    print(f"   ID Pedido: {current_id}")
                    print(f"   Produto: {product_id_bytes.decode().strip()}")
                    print(f"   Usuario: {user_id_bytes.decode().strip()}")
                    print(f"   Quantidade: {quantity}")
                    print(f"   Preco: ${price:.2f}")
                    print(f"   Data: {date_bytes.decode().strip()}")
                    return
            except struct.error:
                pass
    print("Pedido nao encontrado.")

def estatisticas_compras():
    if not os.path.exists(ARQUIVO_COMPRAS):
        print("Nenhuma compra registrada.")
        return
    total_compras = 0
    total_valor = 0.0
    quantidade_total = 0
    with open(ARQUIVO_COMPRAS, "rb") as f:
        while True:
            registro = f.read(TAMANHO_REGISTRO)
            if not registro:
                break
            try:
                order_id_bytes, product_id_bytes, user_id_bytes, quantity, price, date_bytes = struct.unpack(FORMATO_REGISTRO, registro)
                total_compras += 1
                total_valor += price * quantity
                quantidade_total += quantity
            except (ValueError, struct.error):
                pass
    print(f"ESTATISTICAS DAS COMPRAS:")
    print(f"   Total de pedidos: {total_compras}")
    print(f"   Quantidade total de produtos: {quantidade_total}")
    print(f"   Valor total: ${total_valor:.2f}")
    if total_compras > 0:
        print(f"   Valor medio por pedido: ${total_valor/total_compras:.2f}")

def pesquisa_binaria_direta(id_pedido):
    if not os.path.exists(ARQUIVO_COMPRAS):
        print("Arquivo de compras nao encontrado!")
        return
    id_pedido_str = str(id_pedido)
    with open(ARQUIVO_COMPRAS, "rb") as f:
        f.seek(0, 2)
        total_bytes = f.tell()
        total_registros = total_bytes // TAMANHO_REGISTRO
        inicio, fim = 0, total_registros - 1
        while inicio <= fim:
            meio = (inicio + fim) // 2
            pos = meio * TAMANHO_REGISTRO
            f.seek(pos)
            registro_bytes = f.read(TAMANHO_REGISTRO)
            if not registro_bytes:
                break
            order_id_bytes, product_id_bytes, user_id_bytes, quantity, price, date_bytes = struct.unpack(FORMATO_REGISTRO, registro_bytes)
            order_id_atual = order_id_bytes.decode('utf-8').strip()
            if order_id_atual == id_pedido_str:
                print(f"PEDIDO ENCONTRADO (Busca Binaria Direta):")
                print(f"   ID Pedido: {order_id_atual}")
                print(f"   Produto: {product_id_bytes.decode('utf-8').strip()}")
                print(f"   Usuario: {user_id_bytes.decode('utf-8').strip()}")
                print(f"   Quantidade: {quantity}")
                print(f"   Preco: ${price:.2f}")
                print(f"   Data: {date_bytes.decode('utf-8').strip()}")
                return
            elif order_id_atual < id_pedido_str:
                inicio = meio + 1
            else:
                fim = meio - 1
    print("Pedido nao encontrado na busca binaria direta.")

def menu_compras():
    while True:
        print("\n" + "="*60)
        print("        SISTEMA DE GERENCIAMENTO DE COMPRAS")
        print("="*60)
        print("1. Inserir compra")
        print("2. Remover compra")
        print("3. Consultar compra (usando indice)")
        print("4. Listar todas as compras")
        print("5. Estatisticas das compras")
        print("6. Criar/Reconstruir indice")
        print("7. Analise: Produtos lideres de venda")
        print("8. Analise: Sazonalidade nas vendas")
        print("9. Analise: Usuarios com alto valor por compra")
        print("10. Mostrar contador de operacoes")
        print("11. Pesquisa binaria direta (sem indice)")
        print("0. Sair")
        opcao = input("\nEscolha uma opcao: ")
        if opcao == "1":
            try:
                id_pedido = input("ID do pedido: ")
                id_produto = input("ID do produto: ")
                id_usuario = input("ID do usuario: ")
                quantidade = int(input("Quantidade: "))
                preco = float(input("Preco unitario: "))
                data = input("Data (YYYY-MM-DD HH:MM): ")
                inserir_compra(id_pedido, id_produto, id_usuario, quantidade, preco, data)
            except ValueError:
                print("Erro: Verifique os tipos de dados!")
        elif opcao == "2":
            try:
                id_pedido = input("ID do pedido a remover: ")
                remover_compra(id_pedido)
            except Exception as e:
                print(f"Erro: {e}")
        elif opcao == "3":
            try:
                id_pedido = input("ID do pedido a consultar: ")
                buscar_compra(id_pedido)
            except Exception as e:
                print(f"Erro: {e}")
        elif opcao == "4":
            listar_compras()
        elif opcao == "5":
            estatisticas_compras()
        elif opcao == "6":
            forcar_reconstrucao_indice()
        elif opcao == "7":
            analise_produtos_lideres()
        elif opcao == "8":
            analise_sazonalidade_vendas()
        elif opcao == "9":
            analise_usuarios_fieis()
        elif opcao == "10":
            print(f"Operacoes desde ultima reconstrucao: {contador_operacoes}/{RECONSTRUIR_APOS}")
        elif opcao == "11":
            try:
                id_pedido = input("ID do pedido para busca binaria direta: ")
                pesquisa_binaria_direta(id_pedido)
            except Exception as e:
                print(f"Erro: {e}")
        elif opcao == "0":
            print("Saindo do sistema...")
            break
        else:
            print("Opcao invalida!")
menu_compras()