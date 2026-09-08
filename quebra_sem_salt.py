import hashlib
import sys
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

def gerar_hash(senha):
    """Gera o hash SHA-256 de uma string."""
    # Retorna o hash da senha
    return hashlib.sha256(senha.encode('utf-8')).hexdigest()

def quebrar_senhas(arquivo_hashes, arquivo_dicionario):
    """Calcula os hashes de arquivo_dicionario e compara com arquivo_hashes"""
    # Cria duas listas, uma contendo as linhas de arquivo_hashes e a outra de arquivo_dicionario
    hashes_salvos = carregar_linhas(arquivo_hashes)
    senhas_comuns = carregar_linhas(arquivo_dicionario)
    # Dicionario para guarda as senhas comuns e seus hashes
    dicionario_hashes = {}
    # Calcula as hashes de cada senha em senhas_comuns e guarda no dicionario, key é o hash e o value é a senha
    for senha in senhas_comuns:
        hash_calculado = gerar_hash(senha)
        dicionario_hashes[hash_calculado] = senha
    print("\nResultados:")
    # Compara cada hash em hashes_salvos com dicionario_hashes
    for hash_salvo in hashes_salvos:
        # Verifica se a hash de hashes_salvos é igual a alguma hash de dicionario_hashes
        if hash_salvo in dicionario_hashes:
            print(f"{hash_salvo}:{dicionario_hashes[hash_salvo]}")
        # Define que a hash de hashes_salvos não está presente em nenhuma hash de dicionario_hashes
        else:
            print(f"{hash_salvo}:NAO_ENCONTRADA")
    # Registra o tempo de fim
    fim = time.perf_counter()
    # Calcula e exibe a diferença entre fim e inicio
    tempo_execucao = fim - inicio
    print(f"Tempo de execução: {tempo_execucao:.6f} segundos")

if __name__ == "__main__":
    # Verifica uso correto da chamada do arquivo em comando
    if len(sys.argv) != 3:
        print("Uso incorreto!")
        print("Uso de forma correta: python quebra_sem_salt.py <arquivo_hashes> <arquivo_dicionario>")
        # Encerra o programa
        sys.exit(1)
    # Registra o tempo de inicio
    inicio = time.perf_counter()
    quebrar_senhas(sys.argv[1], sys.argv[2])