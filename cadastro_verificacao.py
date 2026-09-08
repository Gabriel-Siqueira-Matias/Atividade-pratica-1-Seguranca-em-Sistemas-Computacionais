import os
import sys
import hashlib

# Nome do arquivo que será salvo/lido os usuarios
arquivo_usuarios = "usuarios.txt"

def calcular_hash_com_salt(salt_bytes, senha_string):
    """Transforma a senha em bytes, concatena a senha (em bytes) com o salt e gera o hash."""
    # Transforma a senha em bytes
    senha_bytes = senha_string.encode('utf-8')
    # Concatena salt com a senha em bytes
    dados_combinados = salt_bytes + senha_bytes
    # Retona o hash dos dados_combinados
    return hashlib.sha256(dados_combinados).hexdigest()

def cadastrar(usuario, senha):
    # Verifica se existe um arquivo_usuarios
    if os.path.exists(arquivo_usuarios):
        # Abre o arquivo_usuarios em modo leitura e guarda como a variavel arquivo
        with open(arquivo_usuarios, 'r', encoding='utf-8') as usuarios:
            # Loop que vai ler de linha em linha do arquivo_usuarios
            for usuarios_linha in usuarios:
                usuarios_linha = usuarios_linha.strip()
                # Verifica se não tem conteudo em usuarios_linha
                if not usuarios_linha:
                    continue
                # Extrai a parte inicial de usuarios_linha, antes do primeiro ':', como o nome do usuário
                usuario_salvo = usuarios_linha.split(':')[0]
                # Verifica se usuário sendo verificado é igual a algum usuário salvo
                if usuario_salvo == usuario:
                    print("Usuário já existente, insira outro")
                    # Encerra o programa
                    sys.exit(1)
    # Gera um salt aleatório de 16 bytes
    salt_bytes = os.urandom(16)
    # Concatena a senha com o salt e calcula o hash
    hash_hex = calcular_hash_com_salt(salt_bytes, senha)
    # Converte o salt para hexadecimal
    salt_hex = salt_bytes.hex()
    # Abre o arquivo_usuarios e guarda como a variavel arquivo
    with open(arquivo_usuarios, 'a', encoding='utf-8') as arquivo:
        # Salva no arquivo_usuarios no formato usuario:salt_hex:hash_hex
        arquivo.write(f"{usuario}:{salt_hex}:{hash_hex}\n")
    print(f"Usuário '{usuario}' cadastrado com sucesso!")

def verificar(usuario, senha):
    # Tenta abrir o arquivo_usuarios, se não for possivel, emite uma mensagem de erro
    try:
        # Abre o arquivo_usuarios em modo leitura e guarda como a variavel arquivo
        with open(arquivo_usuarios, 'r', encoding='utf-8') as usuarios:
            # Loop que vai ler de linha em linha do arquivo_usuarios
            for usuarios_linha in usuarios:
                usuarios_linha = usuarios_linha.strip()
                # Verifica se não tem conteudo em usuarios_linha
                if not usuarios_linha:
                    continue
                # Separa os dados de usuarios_linha em 3 variaveis
                # Usuario_salvo = usuário da linha, salt_salvo = salt do usuário e hash_salvo = hash do usuário
                usuario_salvo, salt_salvo, hash_salvo = usuarios_linha.split(':')
                # Verifica se usuário sendo verificado é igual a algum usuário salvo
                if usuario_salvo == usuario:
                    # Extrai o salt daquele usuário salvo e converte para binario
                    salt_bytes = bytes.fromhex(salt_salvo)
                    # Concatena a senha inserida com o salt extraido e calcula o hash
                    hash_calculado = calcular_hash_com_salt(salt_bytes, senha)
                    # Verifica se o hash calculado com a senha inserida no modo verificar é igual a salva para aquele usuário
                    if hash_calculado == hash_salvo:
                        print("Acesso permitido")
                    # Define que não é a mesma hash
                    else:
                        print("Acesso negado")
                    return
        print("Acesso negado (Usuário não encontrado)")
    # Mensagem de erro
    except FileNotFoundError:
        print("Erro: Arquivo de usuários não existe. Cadastre alguém primeiro.")

if __name__ == "__main__":
    # Verifica uso correto da chamada do arquivo em comando
    if len(sys.argv) != 4:
        print("Uso incorreto!")
        print("Para cadastrar: python cadastro_verificacao.py --cadastrar <usuario> <senha>")
        print("Para verificar: python cadastro_verificacao.py --verificar <usuario> <senha>")
        # Encerra o programa
        sys.exit(1)
    # Define o modo que o comando será executado
    modo = sys.argv[1]
    # Define o usuario
    usuario = sys.argv[2]
    # Define a senha
    senha = sys.argv[3]
    # Verifica se o usuário é aceitavel
    if ":" in usuario:
        print("Usuário não pode conter o caracter ':'")
        # Encerra o programa
        sys.exit(1)
    # Verifica o modo e executa de acordo
    if modo == "--cadastrar":
        cadastrar(usuario, senha)
    elif modo == "--verificar":
        verificar(usuario, senha)
    else:
        print("Modo inválido. Use --cadastrar ou --verificar.")