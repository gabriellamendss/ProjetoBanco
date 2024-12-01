import random

def processar_valor(valor):
    try:
        return float(valor.replace(",", "."))
    except ValueError:
        raise ValueError("Erro ao processar o valor. Insira um número válido.")

class ContaCorrente:
    def __init__(self, nome, senha):
        self.nome = nome
        self.numero_conta = random.randint(100, 999)
        self.__senha = senha
        self.__saldo_corrente = 0.0
        self.tentativas_senha = 0
        self.bloqueada = False
    
    @property
    def saldo_corrente(self):
        return self.__saldo_corrente

    def depositar_corrente(self, valor):
        if valor >= 10.0:
            self.__saldo_corrente += valor
            print(f"Depósito de R$ {valor:.2f} na conta corrente efetuado com sucesso!")
            print(f"Saldo atual da conta corrente: R$ {self.__saldo_corrente:.2f}")
        else:
            print("O valor do depósito deve ser de no mínimo R$ 10,00.")
    
    def sacar(self, valor_saque):
        if valor_saque <= 0:
            print("O valor de saque deve ser maior que zero.")
            return
        if self.__saldo_corrente >= valor_saque:
            self.__saldo_corrente -= valor_saque
            print(f"Saque de R$ {valor_saque:.2f} efetuado com sucesso!")
            print(f"Saldo atual da conta corrente: R$ {self.__saldo_corrente:.2f}")
        else:
            print(f"Saldo insuficiente para realizar o saque. Saldo atual: R$ {self.__saldo_corrente:.2f}")
    
    def aplicar(self, valor, conta_poupanca):
        if self.__saldo_corrente >= valor:
            self.__saldo_corrente -= valor
            conta_poupanca.depositar(valor)
            print(f"Aplicação de R$ {valor:.2f} na poupança efetuada com sucesso!")
        else:
            print("Saldo insuficiente para realizar a aplicação.")
    
    def verificar_senha(self, senha):
        if self.bloqueada:
            print("Conta bloqueada. Dirija-se à agência para desbloqueio.")
            return False
        if senha == self.__senha:
            self.tentativas_senha = 0
            return True
        else:
            self.tentativas_senha += 1
            print(f"Senha incorreta. Tentativa {self.tentativas_senha}/3.")
            if self.tentativas_senha >= 3:
                self.bloqueada = True
                print("Conta bloqueada. Dirija-se à agência com documento com foto.")
            return False


class ContaPoupanca(ContaCorrente):
    def __init__(self, nome, senha):
        super().__init__(nome, senha)
        self.__saldo_poupanca = 0.0
    
    @property
    def saldo_poupanca(self):
        return self.__saldo_poupanca

    def depositar(self, valor):
        self.__saldo_poupanca += valor
        print(f"Depósito de R$ {valor:.2f} na poupança efetuado com sucesso!")
        print(f"Saldo atual da poupança: R$ {self.__saldo_poupanca:.2f}")

    def resgatar(self, valor, conta_corrente):
        if self.__saldo_poupanca >= valor:
            self.__saldo_poupanca -= valor
            #TEM Q SEPARAR ESSA MERDA ASSIM MSM SE NAO DA PROBLEMA
            conta_corrente.depositar_corrente(valor)
            print(f"Resgate de R$ {valor:.2f} efetuado com sucesso!")
        else:
            print("Saldo insuficiente na poupança para realizar o resgate.")
    
    def extrato(self):
        print("+------------------------------------------------+")
        print(f"| Titular: {self.nome}")
        print(f"| Número da conta: {self.numero_conta}")
        print(f"| Saldo da Conta Corrente: R$ {self.saldo_corrente:.2f}")
        print(f"| Saldo da Conta Poupança: R$ {self.saldo_poupanca:.2f}")
        print("+------------------------------------------------+")

def main():
    print("+------------------------------------------------+")
    print("Olá, bem vindo ao Banco LaLa")
    print("Você esta na sessão para se cadastrar!")
    print("+------------------------------------------------+")
    
    nome = input("Insira o nome do titular da conta: ")
    while True:
        senha = input("Crie sua senha numérica de 4 dígitos: ")
        if len(senha) == 4 and senha.isdigit():
            senha = int(senha)
            break
        else:
            print("A senha deve conter exatamente 4 dígitos numéricos.")
    
    conta_poupanca = ContaPoupanca(nome, senha)
    
    while True:
        try:
            deposito_inicial = processar_valor(input("Realize seu primeiro depósito de no mínimo R$ 10,00: "))
            if deposito_inicial >= 10:
                conta_poupanca.depositar(deposito_inicial)
                print("Sua conta foi criada com sucesso! Bem vindo(a)")
                print(f"Número da conta: {conta_poupanca.numero_conta}")
                break
            else:
                print("O valor do depósito deve ser de no mínimo R$ 10,00.")
        except ValueError:
            print("Digite um valor válido.")
    
    while True:
        print("+----------------Banco LaLa---------------------+")
        print("\nEscolha uma opção: ")
        print("1 - Extrato")
        print("2 - Depositar na Conta Corrente")
        print("3 - Depositar na Poupança")
        print("4 - Sacar da Conta Corrente")
        print("5 - Aplicar na Poupança")
        print("6 - Resgatar da Poupança")
        print("7 - Sair")
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            senha = int(input("Digite sua senha para acessar o extrato: "))
            if conta_poupanca.verificar_senha(senha):
                conta_poupanca.extrato()
        
        elif opcao == "2":
            try:
                valor = processar_valor(input("Digite o valor a ser depositado na conta corrente: "))
                conta_poupanca.depositar_corrente(valor)
            except ValueError:
                print("Valor inválido. Por favor, insira um número.")
        
        elif opcao == "3":
            try:
                valor = processar_valor(input("Digite o valor a ser depositado na poupança: "))
                conta_poupanca.depositar(valor)
            except ValueError:
                print("Valor inválido. Por favor, insira um número.")
        
        elif opcao == "4":
            senha = int(input("Digite sua senha para realizar o saque: "))
            if conta_poupanca.verificar_senha(senha):
                try:
                    valor_saque = processar_valor(input("Digite o valor a ser sacado: "))
                    conta_poupanca.sacar(valor_saque)
                except ValueError:
                    print("Valor inválido. Por favor, insira um número.")
        
        elif opcao == "5":
            senha = int(input("Digite sua senha para aplicar: "))
            if conta_poupanca.verificar_senha(senha):
                try:
                    valor_aplicar = processar_valor(input("Digite o valor a ser aplicado na poupança: "))
                    conta_poupanca.aplicar(valor_aplicar, conta_poupanca)
                except ValueError:
                    print("Valor inválido. Por favor, insira um número.")
        
        elif opcao == "6":
            senha = int(input("Digite sua senha para resgatar: "))
            if conta_poupanca.verificar_senha(senha):
                try:
                    valor_resgate = processar_valor(input("Digite o valor a ser resgatado da poupança: "))
                    conta_poupanca.resgatar(valor_resgate, conta_poupanca)
                except ValueError:
                    print("Valor inválido. Por favor, insira um número.")
        
        elif opcao == "7":
            print("Obrigado por usar o banco. Atendimento finalizado.")
            break
        
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
