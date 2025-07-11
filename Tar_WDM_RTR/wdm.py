
W = 1 # Canais

# Pergunta a quantidade de canais usados
while True:
    try:
        W = int(input("Quantos canais? "))
        if W <= 2:
            print("No mínimo há 3 canais...")
        else:
            print(f"Número de canais: {W}")
            break
    except ValueError:
        print("Opção inválida!")

# Vetor usado para carregar as freqs dadas pelo usuario
ondas = []

# Pergunta e armazena as frequências dos canais
for i in range(W):
    while True:
        try:
            freq = float(input(f"Frequência {i+1}(THz): "))
            ondas.append(freq)
            break
        except ValueError:
            print("Frequência inválida!")

# Contagem meramente para mostras quantos sinais foram gerados
count = 0

# calcula cada frequencia gerada, baseada na fórmulada dada pelo prof
for k in range(len(ondas)):
    for j in range(len(ondas)):
        if(j != k):
            for i in range(len(ondas)):
                if (i != k):
                    count += 1
                    sinal = round(ondas[i] + ondas[j] - ondas[k], 1)
                    resultado = f"{count}: f{i+1} + f{j+1} - f{k+1} = {sinal} THz"
                    if sinal in ondas:
                        print(f"{resultado} => Sobreposição!")
                    else:
                        print(f"{resultado}")
                    

# S = W*(W-1)^2 => Sinais


