import os
import time
from datetime import datetime
from termcolor import colored
import threading

class ListaTarefas:
    def __init__(self):
        self.lista = []
        self.id = 0
        self.stop_request = threading.Event()
        
    def cadastrar_tarefa(self):
        tarefa = input('Digite a tarefa: ')
        tarefa_data = input("Digite o dia da tarefa, (Exp: '2021-12-31'): ")
        tarefa_hora = input("Digite a hora da tarefa, (Exp: '23:59'): ")
        tarefa_data_hora = datetime.strptime(tarefa_data + ' ' + tarefa_hora, '%Y-%m-%d %H:%M')
        self.id += 1
        tarefa = (self.id, tarefa, tarefa_data_hora)
        self.lista.append(tarefa)
        
    def listar_tarefas(self):
        for tarefa in self.lista:
            print(
                f'{colored("ID:", "red")} {colored(tarefa[0], "green")} - {colored("Tarefa:", "red")} {colored(tarefa[1], "green")} - {colored("Data e hora:", "red")} {colored(tarefa[2].strftime("%d/%m/%Y %H:%M"), "blue")}'
            )
            
    def apagar_tarefa(self, id):
        for tarefa in self.lista:
            if tarefa[0] == id:
                self.lista.remove(tarefa)
                print('Tarefa removida com sucesso!')
                return
        print('Tarefa não encontrada!')
            
    def sair(self):
        self.stop_request.set()
        print('Saindo...')
        
    def run(self):
        intervalo = 60  # Total de segundos a esperar
        intervalo_verificacao = 1  # Verifica a cada 1 segundo
        
        while not self.stop_request.is_set():
            for tarefa in self.lista:
                if tarefa[2] <= datetime.now():
                    print(f'{colored("ALERTA:", "red")} {colored(tarefa[1], "green")} - {colored("Data e hora:", "red")} {colored(tarefa[2].strftime("%d/%m/%Y %H:%M"), "blue")}')

            # Espera em intervalos menores para resposta rápida à solicitação de parada
            for _ in range(intervalo):
                if self.stop_request.is_set():
                    break
                time.sleep(intervalo_verificacao)

            
    def join(self, timeout=None):
        self.stop_request.set()
        super().join(timeout)

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Você está entrando no projeto de cadastramento de tarefas.')
    print('O que deseja fazer?')
    print('1 - Cadastrar tarefa')
    print('2 - Listar tarefas')
    print('3 - Apagar tarefa')
    print('4 - Sair')
    try:
        opcao = int(input('Digite a opção desejada: '))
    except ValueError:
        print('Opção inválida! Saindo do programa...')
        return
    lista_tarefas = ListaTarefas()
    tarefa_thread = threading.Thread(target=lista_tarefas.run)
    tarefa_thread.start()

    while opcao != 4:
        if opcao == 1:
            lista_tarefas.cadastrar_tarefa()
        elif opcao == 2:
            os.system('cls' if os.name == 'nt' else 'clear')
            lista_tarefas.listar_tarefas()
            print('\n')
        elif opcao == 3:
            os.system('cls' if os.name == 'nt' else 'clear')
            lista_tarefas.listar_tarefas()
            id = int(input('Digite o ID da tarefa que deseja apagar: '))
            lista_tarefas.apagar_tarefa(id)
        else:
            print('Opção inválida!')
        
        # Limpa o terminal
        if opcao != 2:
            os.system('cls' if os.name == 'nt' else 'clear')
        print('Gostaria de fazer mais alguma coisa?')
        print('1 - Cadastrar tarefa')
        print('2 - Listar tarefas')
        print('3 - Apagar tarefa')
        print('4 - Sair')
        opcao = int(input('Digite a opção desejada: '))
        
    lista_tarefas.sair()  # Seta a flag de parada
    tarefa_thread.join()  # Espera a thread terminar

    
if __name__ == '__main__':
    main()
    