import struct
import os

ARQUIVO_JOIAS = r"C:\Users\olive\Downloads\Trabalho algortimos\joias.dat"
ARQUIVO_INDICE = "indice_joias.idx"
FORMATO_REGISTRO = "20s20s10s10s"
TAMANHO_REGISTRO = 60
contador_operacoes = 0
RECONSTRUIR_APOS = 3

def reparar_arquivo_joias():
    print("Reparando arquivo joias.dat...")
    if os.path.exists(ARQUIVO_JOIAS):
        os.rename(ARQUIVO_JOIAS, "joias_corrompido_backup.dat")
        print("Backup do arquivo corrompido criado: joias_corrompido_backup.dat")
    with open(ARQUIVO_JOIAS, "wb") as f:
        pass
    if os.path.exists(ARQUIVO_INDICE):
        os.remove(ARQUIVO_INDICE)
    print("Arquivo joias.dat reparado! Agora insira novas joias.")
    return True

def analise_categorias_dominantes():
    if not os.path.exists(ARQUIVO_JOIAS):
        print("Arquivo de joias nao encontrado!")
        return False
    categorias = {}
    total_joias = 0
    try:
        with open(ARQUIVO_JOIAS, "rb") as f:
            while True:
                chunk = f.read(TAMANHO_REGISTRO)
                if not chunk:
                    break
                if len(chunk) == TAMANHO_REGISTRO:
                    try:
                        product_id, category, material, stone = struct.unpack(FORMATO_REGISTRO, chunk)
                        cat = category.decode('utf-8', errors='ignore').strip()
                        if cat:
                            categorias[cat] = categorias.get(cat, 0) + 1
                            total_joias += 1
                    except struct.error:
                        pass
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
        return False
    if total_joias == 0:
        print("Nenhuma joia valida cadastrada para analise!")
        return False
    print(f"\nANALISE: Dominancia de Categorias no Catalogo")
    print(f"Total de joias analisadas: {total_joias}")
    print("-" * 50)
    categoria_dominante = None
    for categoria, quantidade in categorias.items():
        percentual = (quantidade / total_joias) * 100
        print(f"{categoria:<20}: {quantidade:>3} joias ({percentual:5.1f}%)")
        if percentual > 50:
            categoria_dominante = (categoria, percentual)
    if categoria_dominante:
        print(f"RESPOSTA: SIM - {categoria_dominante[0]} domina com {categoria_dominante[1]:.1f}% do catalogo!")
        return True
    else:
        print(f"RESPOSTA: NAO - Nenhuma categoria domina o catalogo (mais de 50%)")
        return False

def analise_concentracao_materiais():
    if not os.path.exists(ARQUIVO_JOIAS):
        print("Arquivo de joias nao encontrado!")
        return False
    materiais = {}
    total_joias = 0
    try:
        with open(ARQUIVO_JOIAS, "rb") as f:
            while True:
                chunk = f.read(TAMANHO_REGISTRO)
                if not chunk:
                    break
                if len(chunk) == TAMANHO_REGISTRO:
                    try:
                        product_id, category, material, stone = struct.unpack(FORMATO_REGISTRO, chunk)
                        mat = material.decode('utf-8', errors='ignore').strip()
                        if mat:
                            materiais[mat] = materiais.get(mat, 0) + 1
                            total_joias += 1
                    except struct.error:
                        pass
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
        return False
    if total_joias == 0:
        print("Nenhuma joia valida cadastrada para analise!")
        return False
    materiais_ordenados = sorted(materiais.items(), key=lambda x: x[1], reverse=True)
    print(f"\nANALISE: Concentracao por Material")
    print(f"Total de joias analisadas: {total_joias}")
    print(f"Total de materiais distintos: {len(materiais)}")
    print("-" * 50)
    for i, (material, quantidade) in enumerate(materiais_ordenados[:3], 1):
        percentual = (quantidade / total_joias) * 100
        print(f"Top {i}: {material:<15} - {quantidade:>3} joias ({percentual:5.1f}%)")
    percentual_top_3 = sum(qtd for _, qtd in materiais_ordenados[:3]) / total_joias * 100
    print(f"\nOs 3 principais materiais concentram {percentual_top_3:.1f}% das joias")
    if percentual_top_3 > 60:
        print(f"RESPOSTA: SIM - Ha concentracao (mais de 60% em apenas 3 materiais)")
        return True
    else:
        print(f"RESPOSTA: NAO - As joias estao bem distribuidas entre materiais")
        return False

def correlacao_categoria_material():
    if not os.path.exists(ARQUIVO_JOIAS):
        print("Arquivo de joias nao encontrado!")
        return []
    correlacao = {}
    total_joias = 0
    try:
        with open(ARQUIVO_JOIAS, "rb") as f:
            while True:
                chunk = f.read(TAMANHO_REGISTRO)
                if not chunk:
                    break
                if len(chunk) == TAMANHO_REGISTRO:
                    try:
                        product_id, category, material, stone = struct.unpack(FORMATO_REGISTRO, chunk)
                        cat = category.decode('utf-8', errors='ignore').strip()
                        mat = material.decode('utf-8', errors='ignore').strip()
                        if cat and mat:
                            if cat not in correlacao:
                                correlacao[cat] = {}
                            correlacao[cat][mat] = correlacao[cat].get(mat, 0) + 1
                            total_joias += 1
                    except struct.error:
                        pass
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
        return []
    if total_joias == 0:
        print("Nenhuma joia valida cadastrada para analise!")
        return []
    print(f"\nANALISE: Correlacao Categoria-Material")
    print(f"Total de joias analisadas: {total_joias}")
    print(f"Total de categorias distintas: {len(correlacao)}")
    print("-" * 50)
    categorias_especializadas = []
    for categoria, materiais in correlacao.items():
        total_categoria = sum(materiais.values())
        material_principal, qtd_principal = max(materiais.items(), key=lambda x: x[1])
        percentual_especializacao = (qtd_principal / total_categoria) * 100
        print(f"\n{categoria:<20}: {total_categoria:>2} joias no total")
        for mat, qtd in materiais.items():
            percentual = (qtd / total_categoria) * 100
            print(f"  {mat:<15}: {qtd:>2} joias ({percentual:5.1f}%)")
        if percentual_especializacao > 70:
            categorias_especializadas.append((categoria, material_principal, percentual_especializacao))
            print(f"  ESPECIALIZADA em {material_principal}")
    if categorias_especializadas:
        print(f"RESPOSTA: SIM - {len(categorias_especializadas)} categoria(s) especializada(s) encontrada(s)")
        for cat, mat, perc in categorias_especializadas:
            print(f"   {cat} -> {mat} ({perc:.1f}%)")
        return categorias_especializadas
    else:
        print(f"RESPOSTA: NAO - Nenhuma categoria mostra especializacao clara (>70% em um material)")
        return []

def inserir_joia(product_id, category, material, stone):
    global contador_operacoes
    if joia_existe(product_id):
        print(f"Erro: Joia com ID {product_id} ja existe!")
        return False
    product_id_fixed = product_id.ljust(20)[:20]
    category_fixed = category.ljust(20)[:20]
    material_fixed = material.ljust(10)[:10]
    stone_fixed = stone.ljust(10)[:10]
    novo_registro = struct.pack(FORMATO_REGISTRO, 
                               product_id_fixed.encode('utf-8'), 
                               category_fixed.encode('utf-8'), 
                               material_fixed.encode('utf-8'), 
                               stone_fixed.encode('utf-8'))
    registros = []
    if os.path.exists(ARQUIVO_JOIAS):
        with open(ARQUIVO_JOIAS, "rb") as f:
            while True:
                chunk = f.read(TAMANHO_REGISTRO)
                if not chunk:
                    break
                if len(chunk) == TAMANHO_REGISTRO:
                    registros.append(chunk)
    registros.append(novo_registro)
    registros_com_chave = []
    for reg in registros:
        product_id_atual = struct.unpack(FORMATO_REGISTRO, reg)[0].decode('utf-8').strip()
        registros_com_chave.append((product_id_atual, reg))
    registros_com_chave.sort(key=lambda x: x[0])
    registros_ordenados = [reg[1] for reg in registros_com_chave]
    with open(ARQUIVO_JOIAS, "wb") as f:
        for reg in registros_ordenados:
            f.write(reg)
    contador_operacoes += 1
    print(f"Joia {product_id.strip()} inserida!")
    reconstruir_indice_se_necessario()
    return True

def pesquisa_binaria_direta_joias(product_id):
    if not os.path.exists(ARQUIVO_JOIAS):
        return None
    with open(ARQUIVO_JOIAS, "rb") as f:
        f.seek(0, 2)
        total_bytes = f.tell()
        total_registros = total_bytes // TAMANHO_REGISTRO
        inicio = 0
        fim = total_registros - 1
        while inicio <= fim:
            meio = (inicio + fim) // 2
            pos = meio * TAMANHO_REGISTRO
            f.seek(pos)
            registro_bytes = f.read(TAMANHO_REGISTRO)
            if not registro_bytes:
                break
            product_id_bytes, category_bytes, material_bytes, stone_bytes = struct.unpack(FORMATO_REGISTRO, registro_bytes)
            product_id_atual = product_id_bytes.decode('utf-8').strip()
            if product_id_atual == product_id:
                return (product_id_bytes, category_bytes, material_bytes, stone_bytes)
            elif product_id_atual < product_id:
                inicio = meio + 1
            else:
                fim = meio - 1
    return None

def consultar_pesquisa_binaria_joias(product_id):
    resultado = pesquisa_binaria_direta_joias(product_id)
    if resultado:
        product_id_bytes, category_bytes, material_bytes, stone_bytes = resultado
        print(f"JOIA ENCONTRADA (via pesquisa binaria):")
        print(f"   ID: {product_id_bytes.decode().strip()}")
        print(f"   Categoria: {category_bytes.decode().strip()}")
        print(f"   Material: {material_bytes.decode().strip()}")
        print(f"   Pedra: {stone_bytes.decode().strip()}")
    else:
        print("Joia nao encontrada via pesquisa binaria.")

def remover_joia(product_id):
    global contador_operacoes
    if not os.path.exists(ARQUIVO_JOIAS):
        print("Arquivo de joias nao existe!")
        return False
    registros = []
    encontrou = False
    with open(ARQUIVO_JOIAS, "rb") as f:
        while True:
            chunk = f.read(TAMANHO_REGISTRO)
            if not chunk:
                break
            if len(chunk) == TAMANHO_REGISTRO:
                try:
                    pid, category, material, stone = struct.unpack(FORMATO_REGISTRO, chunk)
                    current_id = pid.decode('utf-8', errors='ignore').strip()
                    if current_id != product_id.strip():
                        registros.append(chunk)
                    else:
                        encontrou = True
                        print(f"Joia {product_id} removida!")
                except struct.error:
                    pass
    if not encontrou:
        print(f"Joia {product_id} nao encontrada para remocao!")
        return False
    with open(ARQUIVO_JOIAS, "wb") as f:
        for reg in registros:
            f.write(reg)
    contador_operacoes += 1
    reconstruir_indice_se_necessario()
    return True

def joia_existe(product_id):
    if not os.path.exists(ARQUIVO_JOIAS):
        return False
    with open(ARQUIVO_JOIAS, "rb") as f:
        while True:
            chunk = f.read(TAMANHO_REGISTRO)
            if not chunk:
                break
            if len(chunk) == TAMANHO_REGISTRO:
                try:
                    pid, category, material, stone = struct.unpack(FORMATO_REGISTRO, chunk)
                    current_id = pid.decode('utf-8', errors='ignore').strip()
                    if current_id == product_id.strip():
                        return True
                except struct.error:
                    pass
    return False

def reconstruir_indice_se_necessario():
    global contador_operacoes
    if contador_operacoes >= RECONSTRUIR_APOS:
        print("Reconstruindo indice devido a multiplas operacoes...")
        criar_indice_joias()
        contador_operacoes = 0

def forcar_reconstrucao_indice():
    global contador_operacoes
    criar_indice_joias()
    contador_operacoes = 0
    print("Indice reconstruido forçadamente!")

def mostrar_joias():
    if not os.path.exists(ARQUIVO_JOIAS):
        print("Nenhum dado encontrado. Use a opcao 1 para inserir joias.")
        return
    print(f"\n{'ID':<20} | {'Categoria':<20} | {'Material':<10} | {'Pedra':<10}")
    print("-" * 70)
    registros_validos = 0
    with open(ARQUIVO_JOIAS, "rb") as f:
        while True:
            chunk = f.read(TAMANHO_REGISTRO)
            if not chunk:
                break
            if len(chunk) == TAMANHO_REGISTRO:
                try:
                    product_id, category, material, stone = struct.unpack(FORMATO_REGISTRO, chunk)
                    pid = product_id.decode('utf-8', errors='ignore').strip()
                    cat = category.decode('utf-8', errors='ignore').strip()
                    mat = material.decode('utf-8', errors='ignore').strip()
                    stn = stone.decode('utf-8', errors='ignore').strip()
                    print(f"{pid:<20} | {cat:<20} | {mat:<10} | {stn:<10}")
                    registros_validos += 1
                except struct.error:
                    pass
    if registros_validos == 0:
        print("Nenhum registro valido encontrado.")
    else:
        print(f"\nTotal de registros: {registros_validos}")

def criar_indice_joias():
    if not os.path.exists(ARQUIVO_JOIAS):
        print("Arquivo de joias nao existe para criar indice!")
        return
    with open(ARQUIVO_JOIAS, "rb") as f:
        indices = []
        pos = 0
        while True:
            registro = f.read(TAMANHO_REGISTRO)
            if not registro:
                break
            if len(registro) == TAMANHO_REGISTRO:
                try:
                    product_id, category, material, stone = struct.unpack(FORMATO_REGISTRO, registro)
                    pid = product_id.decode('utf-8', errors='ignore').strip()
                    indices.append((pid, pos))
                except struct.error:
                    pass
            pos += TAMANHO_REGISTRO
    if not indices:
        print("Nenhum registro valido para criar indice!")
        return
    with open(ARQUIVO_INDICE, "wb") as f:
        passo = max(1, len(indices) // 10)
        for i in range(0, len(indices), passo):
            pid, pos = indices[i]
            pid_bytes = pid.ljust(20).encode('utf-8')[:20]
            f.write(struct.pack("20si", pid_bytes, pos))
    print(f"Indice parcial criado com {len(range(0, len(indices), passo))} entradas")

def consultar_joia(product_id):
    if not os.path.exists(ARQUIVO_INDICE):
        print("Indice nao encontrado. Gere o indice primeiro!")
        return
    indices = []
    with open(ARQUIVO_INDICE, "rb") as idx:
        while True:
            idx_bytes = idx.read(24)
            if not idx_bytes:
                break
            try:
                pid_bytes, pos = struct.unpack("20si", idx_bytes)
                pid = pid_bytes.decode('utf-8', errors='ignore').strip()
                indices.append((pid, pos))
            except struct.error:
                pass
    if not indices:
        print("Indice vazio.")
        return
    product_id = product_id.strip()
    for pid_idx, pos in indices:
        if pid_idx == product_id:
            with open(ARQUIVO_JOIAS, "rb") as f:
                f.seek(pos)
                registro = f.read(TAMANHO_REGISTRO)
                if registro and len(registro) == TAMANHO_REGISTRO:
                    try:
                        pid, category, material, stone = struct.unpack(FORMATO_REGISTRO, registro)
                        print(f"Resultado da busca:")
                        print(f"ID: {pid.decode().strip()}")
                        print(f"Categoria: {category.decode().strip()}")
                        print(f"Material: {material.decode().strip()}")
                        print(f"Pedra: {stone.decode().strip()}")
                        return
                    except struct.error:
                        print("Registro corrompido no arquivo.")
                        return
    print("Joia nao encontrada no indice. Fazendo busca sequencial...")
    with open(ARQUIVO_JOIAS, "rb") as f:
        pos = 0
        while True:
            registro = f.read(TAMANHO_REGISTRO)
            if not registro:
                break
            if len(registro) == TAMANHO_REGISTRO:
                try:
                    pid, category, material, stone = struct.unpack(FORMATO_REGISTRO, registro)
                    current_id = pid.decode('utf-8', errors='ignore').strip()
                    if current_id == product_id:
                        print(f"Resultado da busca (busca sequencial):")
                        print(f"ID: {current_id}")
                        print(f"Categoria: {category.decode().strip()}")
                        print(f"Material: {material.decode().strip()}")
                        print(f"Pedra: {stone.decode().strip()}")
                        return
                except struct.error:
                    pass
            pos += TAMANHO_REGISTRO
    print("Joia nao encontrada no sistema.")

def menu_joias():
    while True:
        print("\n" + "="*60)
        print("           SISTEMA DE GERENCIAMENTO DE JOIAS")
        print("="*60)
        print("1. Inserir joia")
        print("2. Remover joia")
        print("3. Consultar joia")
        print("4. Listar todas as joias")
        print("5. Criar/Reconstruir indice")
        print("6. Analise: Categorias dominantes")
        print("7. Analise: Concentracao por material") 
        print("8. Analise: Correlacao categoria-material")
        print("9. Mostrar contador de operacoes")
        print("10. REPARAR ARQUIVO (use se der erro)")
        print("11. Consultar por pesquisa binaria (sem indice)")
        print("0. Sair")
        opcao = input("\nEscolha uma opcao: ")
        if opcao == "1":
            try:
                id_joia = input("ID da joia: ")
                categoria = input("Categoria: ")
                material = input("Material: ")
                pedra = input("Pedra: ")
                inserir_joia(id_joia, categoria, material, pedra)
            except Exception as e:
                print(f"Erro: {e}")
        elif opcao == "2":
            try:
                id_joia = input("ID da joia a remover: ")
                remover_joia(id_joia)
            except Exception as e:
                print(f"Erro: {e}")
        elif opcao == "3":
            try:
                id_joia = input("ID da joia a consultar: ")
                consultar_joia(id_joia)
            except Exception as e:
                print(f"Erro: {e}")
        elif opcao == "4":
            mostrar_joias()
        elif opcao == "5":
            forcar_reconstrucao_indice()
        elif opcao == "6":
            analise_categorias_dominantes()
        elif opcao == "7":
            analise_concentracao_materiais()
        elif opcao == "8":
            correlacao_categoria_material()
        elif opcao == "9":
            print(f"Operacoes desde ultima reconstrucao: {contador_operacoes}/{RECONSTRUIR_APOS}")
        elif opcao == "10":
            reparar_arquivo_joias()
        elif opcao == "11":
            try:
                id_joia = input("ID da joia a consultar (pesquisa binaria): ")
                consultar_pesquisa_binaria_joias(id_joia)
            except Exception as e:
                print(f"Erro: {e}")
        elif opcao == "0":
            print("Saindo do sistema...")
            break
        else:
            print("Opcao invalida!")

if __name__ == "__main__":
    if os.path.exists(ARQUIVO_JOIAS):
        file_size = os.path.getsize(ARQUIVO_JOIAS)
        if file_size > 0:
            print(f"Arquivo joias.dat encontrado ({file_size} bytes)")
            print("Use a opcao 4 para listar todas as joias")
        else:
            print("Arquivo joias.dat existe mas esta vazio")
    else:
        print("Arquivo joias.dat nao encontrado")
        print("Use a opcao 1 para inserir joias ou 10 para reparar")
    menu_joias()