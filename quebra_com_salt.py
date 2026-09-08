import sys
import hashlib
import time

def carregar_linhas(caminho_arquivo):
    """Lê o arquivo e retorna uma lista das linhas."""
    # Tenta abrir o arquivo, se não for possivel, emite uma mensagem de erro
    try:
        # Abre o arquivo em modo leitura e guarda como a variavel arquivo
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            # Retorna uma lista aonde cada índice contém uma linha do arquivo
            return [linha.strip() for linha in arquivo if linha.strip()]
    # Mensagem de erro e retorna uma lista vazia
    except FileNotFoundError:
        print(f"Erro: Arquivo {caminho_arquivo} não encontrado.")
        return []

def ataque_com_salt(arquivo_hashes, arquivo_dicionario):
    """Calcula os hashes de arquivo_dicionario e compara com arquivo_hashes"""
    # Cria duas listas, uma contendo as linhas de arquivo_hashes e a outra de arquivo_dicionario
    linhas_hashes = carregar_linhas(arquivo_hashes)
    senhas_comuns = carregar_linhas(arquivo_dicionario)
    # Dicionario para armazenar os salts e hashes
    dicionario_hashes = {}
    # Loop linha por linha de linha_hashes
    for linha in linhas_hashes:
        # Separa linha em 2 variaveis, salt_hex que contem o salt e hash_hex que contem o hash
        salt_hex, hash_hex = linha.split(':')
        # Verifica se o salt_hex não existe no dicionario
        if salt_hex not in dicionario_hashes:
            # Adiciona o salt_hex como key e cria um conjunto vazio associado a ele
            dicionario_hashes[salt_hex] = set()
        # Adiciona o hash_hex em um conjunto definido pelo seu salt_hex no dicionario
        dicionario_hashes[salt_hex].add(hash_hex)
    # Dicionario para guardar as hashes que tiveram a senha descoberta
    resultados_quebrados = {}
    # Converte senhas para binario
    senhas_bytes = [senha.encode('utf-8') for senha in senhas_comuns]
    # Analisa conjunto por conjunto dentro de dicionario_hashes, e separa o salt_hex do conjunto de hashes
    for salt_hex, hashes in dicionario_hashes.items():
        # Converte o salt_hex em binario
        salt_bytes = bytes.fromhex(salt_hex)
        # Loop de senha em senha de senhas_comuns
        for senha in senhas_bytes:
            # Calcula o hash da concatenação de salt em binario com a senha em binario
            hash_calculada = hashlib.sha256(salt_bytes + senha).hexdigest()
            # Verifica se hash_calculado é igual a alguma hash de hashes
            if hash_calculada in hashes:
                # Guarda a senha no dicionario associada a uma hash_calculada
                resultados_quebrados[hash_calculada] = senha.decode('utf-8')
                break
    # Loop de linha em linha de linhas_hashes
    for linha in linhas_hashes:
        # Separa linha em 2 variaveis, salt_hex que contem o salt e hash_hex que contem o hash
        salt_hex, hash_hex = linha.split(':')
        # Verifica se a hash_hex existe em resultados_quebrados
        if hash_hex in resultados_quebrados:
            print(f"{salt_hex}:{hash_hex} -> {resultados_quebrados[hash_hex]}")
        # Define que hash_hez não está no dicionario
        else:
            print(f"{salt_hex}:{hash_hex} -> NAO_ENCONTRADA")
    # Registra o tempo de fim
    fim = time.perf_counter()
    # Calcula e exibe a diferença entre fim e inicio
    tempo_execucao = fim - inicio
    print(f"Tempo de execução: {tempo_execucao:.6f} segundos")

if __name__ == "__main__":
    # Verifica uso correto da chamada do arquivo em comando
    if len(sys.argv) != 3:
        print("Uso incorreto!")
        print("Uso de forma correta: python quebra_com_salt.py <arquivo_hashes_com_salt> <arquivo_senhas_comuns>")
        # Encerra o programa
        sys.exit(1)
    # Registra o tempo de inicio
    inicio = time.perf_counter()
    ataque_com_salt(sys.argv[1], sys.argv[2])