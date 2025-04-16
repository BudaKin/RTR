def quebrar_linha(texto, tamanho):
    return '\n'.join([texto[i:i+tamanho] for i in range(0, len(texto), tamanho)])

def leitura(texto: str):
    indice = 0
    PAQ = "10011011"
    while 1:
        indice = texto.find(PAQ, indice)
        # Verificando se a sequência foi encontrada
        if indice != -1 and indice + 257 < len(texto):
            if texto[indice+257] == "1":
                res = texto[indice:]
                print(f"foi encontrado a primeira flag: {indice}")
                return res
            print(f"flag errada em: {indice}")
            indice = indice+8
        else:
            print(f"não foi encontrada.")
            return "Erro"

# Abrir o arquivo em modo escrita
with open("saida.txt", "w") as saida:
    # with open("RX(vetor)MQ_v2.txt", "r") as entrada:
    with open("exercicio_dado.txt", "r") as entrada:
        texto = entrada.read()
        substring = ''.join([c for c in texto if c in '01'])
        lido = leitura(substring)
        lido = ' '.join(lido)
        lido = quebrar_linha(lido, 128)
        saida.write(lido)
            

