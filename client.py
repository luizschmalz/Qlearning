import connection as cn
import random as r

socket = cn.connect(2037)
aprendizado = 0.5
gamma = 0.9
possiveis_acoes = ['left', 'jump', 'right']
epsilon = 0.1

#00 = norte, 01 = leste, 10 = sul, 11 = oeste

for i in range(100):
    acao = 'jump'
    estado, recompensa = cn.get_state_reward(socket, acao)
    print(estado)
    print(recompensa)
    while recompensa != -1: #nao estando nos blocos finais
        posicao = int(estado[2:7],2)*4 + int(estado[7:],2)
        #calculando aonde vai mexer na q table

        file = open('resultado.txt', 'r')

        resultados = file.readlines()

        #escolhendo a linha certa e recebdno os valores
        valorestado = resultados[posicao]
        valorestado_split = valorestado.split(" ")
        qtable = []

        for i in valorestado_split:
            qtable.append(float(i))
        
        print(f'valores desse estado: {qtable}')

        #escolhendo proxima acao
        #como o nao determinismo ja esta implementado, so vamos escolher o melhor caminho
        if r.uniform(0, 1) < epsilon:
            acao = r.choice(possiveis_acoes)
        else:    
            valor = qtable.index(max(qtable[0], qtable[1], qtable[2]))
            acao = possiveis_acoes[valor]

        novo_estado, recompensa = cn.get_state_reward(socket, acao)

        #precisamos atualizar a Q table agora
        #equacao de atualizacao = aprendizado * (recompensa + gamma * qtable.inqtableex(max(qtable[0], qtable[1], qtable[2])) - qtable[state, possivelacao])
        #precisamos atualizar o valor de acordo com a acao escolhida

        if acao == "left":
            novo_valor = aprendizado * ((recompensa + gamma * max(float(valorestado_split[0]), float(valorestado_split[1]), float(valorestado_split[2])) - float(valorestado_split[0])))
            atual = str(float(novo_valor) + float(valorestado_split[0])) + " " + valorestado_split[1] + " " + valorestado_split[2]
        elif acao == "jump":
            novo_valor = aprendizado * ((recompensa + gamma * max(float(valorestado_split[0]), float(valorestado_split[1]), float(valorestado_split[2])) - float(valorestado_split[1])))
            atual = valorestado_split[0] + " " + str(float(novo_valor) + float(valorestado_split[1])) + " " + valorestado_split[2]
        elif acao == "right":
            novo_valor = aprendizado * ((recompensa + gamma * max(float(valorestado_split[0]), float(valorestado_split[1]), float(valorestado_split[2])) - float(valorestado_split[2])))
            atual = valorestado_split[0]+ " " + valorestado_split[1] + " " + str(float(novo_valor) + float(valorestado_split[2])) + "\n"
            atual = atual.replace(r"\n", "\n")

        #escrevendo o novo valor
        resultados[posicao] = atual

        # guardando novos valores na q table
        file = open('resultado.txt', 'w')
        file.writelines(resultados)

        estado = novo_estado

file.close()
#acabando as rodadas de aprendizado





