# Importa as bibliotecas necessárias
from abc import ABC, abstractmethod  # Para criar classes abstratas
import re  # Para trabalhar com expressões regulares
from datetime import datetime, timedelta  # Para manipulação de data e hora

# Exceção personalizada para hora inválida
class HoraInvalidaError(Exception):
    def __init__(self, mensagem):
        self.mensagem = mensagem  # A mensagem de erro que será exibida
        super().__init__(self.mensagem)  # Chama o construtor da classe pai

# Classe abstrata Usuario, que serve de base para outros tipos de usuário
class Usuario(ABC):
    def __init__(self, nome: str, hora: str, id: int):
        self.nome = nome  # Nome do usuário
        self.hora = hora  # Hora relacionada ao chamado
        self.id = id  # ID do usuário (por exemplo, ID do cliente)

    @abstractmethod
    def mostrar_info(self):
        """Método abstrato que deve ser implementado pelas subclasses"""
        pass  # Esse método deve ser implementado nas subclasses

# Classe concreta Cliente, que herda de Usuario e representa um cliente específico
class Cliente(Usuario):
    def __init__(self, nome: str, hora: str, id: int, descricao: str, prioridade: str, tempo_estimado: str, ticket_id: int):
        super().__init__(nome, hora, id)  # Chama o construtor da classe base
        self.descricao = descricao  # Descrição do problema relatado
        self.prioridade = prioridade  # Prioridade do chamado
        self.tempo_estimado = tempo_estimado  # Tempo estimado para solução
        self.ticket_id = ticket_id  # ID único do ticket de chamado

    # Implementação do método abstrato para exibir as informações do cliente
    def mostrar_info(self):
        print(f"\nCliente: {self.nome}, Hora: {self.hora}, ID: {self.id}, Ticket ID: {self.ticket_id}")
        print(f"Descrição do Chamado: {self.descricao}")
        print(f"Prioridade: {self.prioridade}, Prazo limite para atendimento: {self.tempo_estimado}")

# Função para validar o formato da hora (HH:MM)
def validar_hora(hora):
    # Usa uma expressão regular para verificar se a hora está no formato correto
    if not re.match(r"^[0-2][0-9]:[0-5][0-9]$", hora):
        raise HoraInvalidaError("Hora inválida! O formato correto é HH:MM.")  # Levanta exceção se o formato for inválido
    return hora  # Retorna a hora se estiver válida

# Função para calcular o status do chamado com base no tempo estimado e hora do chamado
def calcular_status(tempo_estimado, hora_chamado):
    formato_hora = "%H:%M"  # Define o formato da hora
    
    # Converte as strings de hora para objetos datetime para facilitar a comparação
    hora_chamado_obj = datetime.strptime(hora_chamado, formato_hora)
    tempo_estimado_obj = datetime.strptime(tempo_estimado, formato_hora)
    
    # Compara as horas e determina se o prazo foi cumprido
    if hora_chamado_obj <= tempo_estimado_obj:
        return "Chamado dentro do prazo de atendimento"  # Se a hora do chamado for menor ou igual ao prazo, está no prazo
    else:
        return "Chamado com prazo limite excedido"  # Caso contrário, o prazo foi excedido

# Função para exibir o menu principal do sistema
def exibir_menu_principal():
    print("\nEscolha uma opção:")
    print("1 - Abrir Chamado")  # Opção para abrir um novo chamado
    print("2 - Consultar Chamado por Número do Ticket")  # Opção para consultar um chamado existente
    print("3 - Sair")  # Opção para sair do sistema

# Função para abrir um novo chamado
def abrir_chamado(ticket_counter, chamados):
    # Solicitar dados do cliente para abrir o chamado
    nome = solicitar_nome()
    if nome is None:
        return ticket_counter, chamados  # Se o nome for 's', volta ao menu
    
    hora = solicitar_hora()
    if hora is None:
        return ticket_counter, chamados  # Se a hora for inválida, volta ao menu
    
    id_usuario = solicitar_id()
    if id_usuario is None:
        return ticket_counter, chamados  # Se o ID for inválido, volta ao menu
    
    # Cria o objeto cliente1 com os dados fornecidos
    cliente1 = Cliente(nome, hora, id_usuario, "", "", "", ticket_counter)
    
    # Menu para definir a prioridade e tempo de atendimento
    prioridade, tempo_atendimento = definir_prioridade()
    if prioridade is None:
        return ticket_counter, chamados  # Se a prioridade não for selecionada, volta ao menu
    
    # Atualiza o cliente com a prioridade e tempo estimado
    cliente1.prioridade = prioridade
    cliente1.tempo_estimado = tempo_atendimento
    
    # Solicita uma descrição do chamado
    descricao = input("\nDescreva o problema do chamado (ou 's' para voltar ao menu principal): ")
    if descricao.lower() == 's':
        return ticket_counter, chamados  # Se a descrição for 's', volta ao menu principal
    cliente1.descricao = descricao  # Atribui a descrição ao cliente
    
    # Salva o chamado em um arquivo
    salvar_chamado(cliente1)
    
    # Adiciona o chamado no dicionário 'chamados', com o ticket_id como chave
    chamados[cliente1.ticket_id] = cliente1
    
    # Exibe as informações do chamado
    print(f"Chamado aberto com sucesso! Ticket ID: {cliente1.ticket_id}")
    cliente1.mostrar_info()
    
    return ticket_counter + 1, chamados  # Retorna o contador de tickets incrementado

# Função para solicitar o nome do usuário
def solicitar_nome():
    while True:
        nome = input("Digite o nome do usuário (ou 's' para voltar ao menu principal): ")
        if nome.lower() == 's':
            return None  # Retorna None se o usuário digitar 's'
        if nome:
            return nome  # Retorna o nome se for válido

# Função para solicitar o ID do usuário
def solicitar_id():
    while True:
        try:
            id_usuario = input("Digite o ID do usuário (ou 's' para voltar ao menu principal): ")
            if id_usuario.lower() == 's':
                return None  # Retorna None se o usuário digitar 's'
            return int(id_usuario)  # Converte o ID para inteiro e retorna
        except ValueError:
            print("ID inválido! Digite um número.")  # Se o ID não for um número, exibe erro

# Função para solicitar e validar a hora do chamado
def solicitar_hora():
    while True:
        try:
            hora = input("Digite a hora (HH:MM) (ou 's' para voltar ao menu principal): ")
            if hora.lower() == 's':
                return None  # Retorna None se o usuário digitar 's'
            validar_hora(hora)  # Valida o formato da hora
            return hora  # Retorna a hora se for válida
        except HoraInvalidaError as e:
            print(e)  # Exibe a mensagem de erro se a hora for inválida

# Função para definir a prioridade e o tempo estimado do chamado
def definir_prioridade():
    prioridades = {
        1: ('N1', '01:00'),  # Urgente
        2: ('N2', '04:00'),  # Médio
        3: ('N3', '08:00')   # Baixa
    }
    
    # Exibe as opções de prioridade
    print("\nDefina a prioridade do seu chamado:")
    print("1 - Urgente (Prazo limite para atendimento: 01:00)")
    print("2 - Médio (Prazo limite para atendimento: 04:00)")
    print("3 - Baixa (Prazo limite para atendimento: 08:00)")
    print("4 - Sair")  # Opção para sair do sistema

    while True:
        try:
            opcao_prioridade = input("Digite o número da prioridade (1, 2 ou 3) (ou 's' para voltar ao menu principal): ")
            if opcao_prioridade.lower() == 's':
                return None, None  # Se o usuário digitar 's', volta ao menu principal
            opcao_prioridade = int(opcao_prioridade)  # Converte para inteiro
            if opcao_prioridade == 4:
                print("Saindo do sistema. Até logo!")
                exit()  # Sai do sistema se a opção for 4
            if opcao_prioridade not in prioridades:
                raise ValueError("Opção inválida! Escolha entre 1, 2 ou 3.")  # Verifica se a opção é válida
            return prioridades[opcao_prioridade]  # Retorna a prioridade e o tempo estimado
        except ValueError as e:
            print(e)  # Exibe mensagem de erro caso a opção seja inválida

# Função para salvar o chamado em um arquivo
def salvar_chamado(cliente):
    with open("chamados.txt", "a") as file:
        # Salva as informações do chamado no arquivo
        file.write(f"Ticket ID: {cliente.ticket_id}, Cliente: {cliente.nome}, Hora: {cliente.hora}, ID: {cliente.id}, Prioridade: {cliente.prioridade}, Prazo limite para atendimento: {cliente.tempo_estimado}\n")
        file.write(f"Descrição do Chamado: {cliente.descricao}\n")
        file.write("-" * 50 + "\n")  # Separa os chamados por uma linha de hífens

# Função para consultar o status do chamado
def consultar_chamado(tickets):
    while True:
        ticket_id = input("Digite o número do Ticket ID (ou 's' para voltar ao menu principal): ")
        if ticket_id.lower() == 's':
            return  # Se o usuário digitar 's', volta ao menu principal
        try:
            ticket_id = int(ticket_id)  # Converte o Ticket ID para inteiro
            if ticket_id in tickets:
                cliente1 = tickets[ticket_id]  # Busca o chamado correspondente ao Ticket ID
                # Exibe as informações do chamado
                print("\nInformações do Chamado:")
                cliente1.mostrar_info()

                # Calcula e exibe o status do chamado
                status = calcular_status(cliente1.tempo_estimado, cliente1.hora)
                print(f"Status do chamado: {status}")
            else:
                print("Chamado não encontrado com esse Ticket ID.")  # Caso o Ticket ID não exista
            break
        except ValueError:
            print("Digite um número válido ou 's' para voltar ao menu principal.")  # Caso o Ticket ID seja inválido

# Função principal que organiza o fluxo do sistema
def main():
    ticket_counter = 1  # Contador de Ticket IDs, começa em 1
    chamados = {}  # Dicionário para armazenar os chamados com o Ticket ID como chave
    
    print("Bem-vindo ao sistema de abertura de chamados!\n")

    while True:
        exibir_menu_principal()  # Exibe o menu principal
        
        opcao = input("Digite o número da opção: ")

        if opcao == '1':
            ticket_counter, chamados = abrir_chamado(ticket_counter, chamados)  # Abre um novo chamado
        elif opcao == '2':
            consultar_chamado(chamados)  # Consulta um chamado existente
        elif opcao == '3':
            print("Saindo do sistema. Até logo!")
            break  # Sai do sistema
        else:
            print("Opção inválida! Tente novamente.")  # Caso a opção seja inválida

# Chama a função principal quando o script é executado
if __name__ == "__main__":
    main()
