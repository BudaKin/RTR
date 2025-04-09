
def leitura(texto: str):
    indice = 0
    substring = texto.replace(" ", "")
    PAQ = "10011011"
    while 1:
        indice = substring.find(PAQ, indice)
        # Verificando se a sequência foi encontrada
        if indice != -1 and indice + 257 < len(substring):
            if substring[indice+257] == "1":
                substring = substring[indice:]
                substring = ' '.join(substring)
                print(f"foi encontrado a primeira flag: {indice}")
                return substring
            indice = indice+8
            print(f"flag errada em: {indice}")
        else:
            print(f"não foi encontrada.")
            return "Erro"

# Abrir o arquivo em modo escrita
with open("saida.txt", "w") as saida:
    with open("RX(vetor)MQ_v2.txt", "r") as entrada:
    # with open("exercicio_dado.txt", "r") as entrada:
        texto = entrada.read()
        substring = texto.replace("\n", "")
        saida.write(leitura(texto))
            

