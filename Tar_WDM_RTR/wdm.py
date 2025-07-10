
W = 1 # Canais

while(W <= 2):
    W = int(input("Quantos sinais? "))
    print(f"Número de sinais: {W}")
    if(W <= 2):
        print("No mínimo há 3 sinais...")

sinais = []

for i in range(W):
    sinais.append(float(input(f"Frequência {i+1}: ")))


S = W*(W-1)^2 # Sinais


