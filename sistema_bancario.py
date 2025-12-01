import re

menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[nu] Novo usuário
[nc] Nova conta
[q] Sair

=> """

AGENCIA_PADRAO = "0001"


def depositar(saldo, valor, extrato, /):
    """Deposita um valor na conta. Argumentos por posição.

    Retorna: (saldo, extrato)
    """
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    """Realiza saque. Argumentos somente por nome.

    Retorna: (saldo, extrato, numero_saques)
    """
    if valor <= 0:
        print("Operação falhou! O valor informado é inválido.")
        return saldo, extrato, numero_saques

    if valor > saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
        return saldo, extrato, numero_saques

    if valor > limite:
        print("Operação falhou! O valor do saque excede o limite.")
        return saldo, extrato, numero_saques

    if numero_saques >= limite_saques:
        print("Operação falhou! Número máximo de saques excedido.")
        return saldo, extrato, numero_saques

    saldo -= valor
    extrato += f"Saque: R$ {valor:.2f}\n"
    numero_saques += 1

    return saldo, extrato, numero_saques


def mostrar_extrato(saldo, /, *, extrato):
    """Exibe o extrato. `saldo` como positional-only, `extrato` como nomeado."""
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")


def criar_usuario(usuarios, nome, data_nascimento, cpf, endereco):
    """Cria um usuário e adiciona na lista `usuarios`.

    - `cpf` será armazenado apenas com dígitos.
    - Não permite CPFs duplicados (verifica na lista).
    Retorna True se criado, False se CPF já existir.
    """
    cpf_digits = re.sub(r"\D", "", cpf)

    for u in usuarios:
        if u["cpf"] == cpf_digits:
            print("Já existe usuário com esse CPF.")
            return False

    usuario = {
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf_digits,
        "endereco": endereco,
    }
    usuarios.append(usuario)
    return True


def criar_conta(contas, usuarios, cpf):
    """Cria uma conta para o usuário identificado por `cpf`.

    - Agência fixa: `AGENCIA_PADRAO`
    - Número da conta: sequencial (inicia em 1)
    - Retorna a conta criada (dict) ou None se usuário não encontrado.
    """
    cpf_digits = re.sub(r"\D", "", cpf)
    usuario = None
    for u in usuarios:
        if u["cpf"] == cpf_digits:
            usuario = u
            break

    if usuario is None:
        print("Usuário não encontrado, por favor cadastre o usuário antes de criar a conta.")
        return None

    numero_conta = len(contas) + 1
    conta = {"agencia": AGENCIA_PADRAO, "numero": numero_conta, "usuario": usuario}
    contas.append(conta)
    return conta


if __name__ == "__main__":
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3

    usuarios = []
    contas = []

    while True:
        opcao = input(menu).strip().lower()

        if opcao == "d":
            try:
                valor = float(input("Informe o valor do depósito: "))
            except ValueError:
                print("Valor inválido.")
                continue

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            try:
                valor = float(input("Informe o valor do saque: "))
            except ValueError:
                print("Valor inválido.")
                continue

            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            mostrar_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            nome = input("Nome do usuário: ")
            data_nascimento = input("Data de nascimento (DD/MM/AAAA): ")
            cpf = input("CPF (somente números ou formatado): ")
            endereco = input("Endereço (logradouro, número - bairro - cidade/UF): ")
            criado = criar_usuario(usuarios, nome, data_nascimento, cpf, endereco)
            if criado:
                print("Usuário criado com sucesso.")

        elif opcao == "nc":
            cpf = input("Informe o CPF do usuário para vincular a conta: ")
            conta = criar_conta(contas, usuarios, cpf)
            if conta:
                print(f"Conta criada com sucesso. Agência: {conta['agencia']} - Conta: {conta['numero']}")

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")
 

