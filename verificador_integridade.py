import os
import sys
import hashlib

# Nome do arquivo que será salvo os hashes
arquivo_hashes = "hashes.txt"

def calcular_hash_arquivo(caminho_arquivo):
    """Calcula o hash SHA-256 do arquivo, o lendo em blocos de tamanho de 64 KB (65536 bytes)."""
    # O tamanho definido para cada bloco, sendo este 65536 bytes
    tamanho_bloco=65536
    # Cria o objeto responsável pelos calculos dos hashes
    sha256 = hashlib.sha256()
    # Tenta abrir o arquivo, se não for possivel, emite uma mensagem de erro com o caminho do arquivo
    try:
        # Abre o arquivo no formato binario, em modo leitura e guarda como a variavel arquivo
        with open(caminho_arquivo, "rb") as arquivo:
            # Loop que vai ler de bloco (65536 bytes) em bloco do arquivo
            for bloco in iter(lambda: arquivo.read(tamanho_bloco), b""):
                # Guarda cada bloco no objeto sha256
                sha256.update(bloco)
        # Executa o calculo do hash do arquivo dentro do objeto sha256 e retorna o resultado
        return sha256.hexdigest()
    # Mensagem de erro se não for possivel abrir o arquivo e retorna nada
    except Exception as e:
        print(f"Erro ao ler {caminho_arquivo}: {e}")
        return None

def gerar_hashes(diretorio):
    """Percorre o diretório, calcula os hashes e salva no arquivo com o nome definido por arquivo_hashes."""
    print(f"Iniciando varredura no diretório: {diretorio}")
    # Se não existir arquivo arquivo_hashes: Cria ele. abre em modo escrita e guarda como a variavel arquivo_saida
    # Se existir arquivo arquivo_hashes: Abre ele em modo escrita, apaga o conteudo anterior e guarda como a variavel arquivo_saida
    with open(arquivo_hashes, "w", encoding="utf-8") as arquivo_saida:
        # Define os dados contidos no diretório
        for root, dirs, files in os.walk(diretorio):
            # Verifica todos os arquivos dentro do diretório, um por um
            for file in files:
                # Define o caminho do arquivo sendo verificado
                caminho_completo = os.path.join(root, file)
                # Calcula o hash do arquivo sendo verificado
                hash_calculado = calcular_hash_arquivo(caminho_completo)
                # Se hash for calculado salva ele no arquivo arquivo_hashes
                if hash_calculado:
                    arquivo_saida.write(f"{caminho_completo}:{hash_calculado}\n")
    print("Arquivo hashes.txt gerado com sucesso!")

def verificar_integridade(diretorio):
    """Compara o estado atual do diretório com o arquivo com o nome definido por arquivo_hashes."""
    print("Modo de verificação ativado. Analisando arquivos...")
    # Dicionario para salvar os dados do arquivo arquivo_hashes
    estado_salvo = {}
    # Tenta abrir o arquivo arquivo_hashes, se não for possivel, emite uma mensagem de erro
    try:
        # Abre o arquivo em modo leitura e guarda como a variavel arquivo_entrada
        with open(arquivo_hashes, "r", encoding="utf-8") as hashes_entrada:
            # Loop que vai ler de linha em linha do arquivo_hashes
            for hashes_linha in hashes_entrada:
                hashes_linha = hashes_linha.strip()
                # Se houver conteúdo na linha
                # Separa os dados e salva em um dicionario, antes de : é o caminho do arquivo que irá ser a key e depois de : é o hash que será o value da key
                if hashes_linha:
                    caminho, hash_salvo = hashes_linha.rsplit(':', 1)
                    estado_salvo[caminho] = hash_salvo
    # Mensagem de erro e retorna
    except FileNotFoundError:
        print("Erro: Arquivo hashes.txt não encontrado. Execute sem a flag --verificar para gerar os hashes primeiro.")
        return
    # Dicionario para salvar os hashes e caminhos dos arquivos do diretorio sendo analisado
    estado_novo = {}
    # Define os dados contidos no diretório
    for root, dirs, files in os.walk(diretorio):
        # Verifica todos os arquivos dentro do diretório, um por um
        for file in files:
            # Define o caminho do arquivo sendo verificado
            caminho_completo = os.path.join(root, file)
            # Calcula o hash do arquivo sendo verificado
            hash_calculado = calcular_hash_arquivo(caminho_completo)
            # Se hash for calculado salva ele no dicionario, key é o caminho do arquivo e o value da key é o hash
            if hash_calculado:
                estado_novo[caminho_completo] = hash_calculado
    # Listas para guarda os arquivos categorizados depois de comparar as hashes e caminhos entre o diretorio sendo analisado e o arquivo arquivo_hashes
    arquivos_novos = []
    arquivos_removidos = []
    arquivos_modificados = []
    arquivos_inalterados = []
    # Analisa e define cada hashes e caminhos entre o diretório sendo analisado e o arquivo arquivo_hashes
    for caminho, hash_salvo in estado_salvo.items():
        # Verifica se um caminho vindo do arquivo arquivo_hashes não existe no diretório sendo analisado
        if caminho not in estado_novo:
            arquivos_removidos.append(caminho)
        # Verifica se a hash de uma determinada posição do diretório sendo analisado é igual a guardada na mesma posição no arquivo arquivo_hashes
        elif estado_novo[caminho] == hash_salvo:
            arquivos_inalterados.append(caminho)
        # Define o arquivo como modificado
        else:
            arquivos_modificados.append(caminho)
    # Verifica se algum caminho do diretório sendo analisado não existe no arquivo arquivo_hashes
    for caminho in estado_novo:
        if caminho not in estado_salvo:
            arquivos_novos.append(caminho)
    # Resultados na analise entre o diretório sendo analisado e o arquivo arquivo_hashes
    print("\n--- Relatório de Status ---")
    print(f"Arquivos inalterados: {len(arquivos_inalterados)}")
    for arquivo in arquivos_inalterados:
        print(f' - {arquivo}')
    print(f"Arquivos novos: {len(arquivos_novos)}")
    for arquivo in arquivos_novos:
        print(f' - {arquivo}')
    print(f"Arquivos modificados: {len(arquivos_modificados)}")
    for arquivo in arquivos_modificados:
        print(f' - {arquivo}')
    print(f"Arquivos removidos: {len(arquivos_removidos)}")
    for arquivo in arquivos_removidos:
        print(f' - {arquivo}')

if __name__ == "__main__":
    # Verifica uso correto da chamada do arquivo em comando
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Uso incorreto!")
        print("Para gerar: python verificador_integridade.py <diretorio>")
        print("Para verificar: python verificador_integridade.py <diretorio> --verificar")
        # Encerra o programa
        sys.exit(1)
    # Define o caminho do diretório a ser analisado
    diretorio_alvo = sys.argv[1]
    # Verifica o tipo de chamada em comando / Se True, executa a verificação do diretório
    if len(sys.argv) == 3 and sys.argv[2] == "--verificar":
        verificar_integridade(diretorio_alvo)
    # Se False, executa o calculo e mapeamento dos hashes do diretório
    else:
        gerar_hashes(diretorio_alvo)