
def leitura(texto: str):
    PAQ = "1 0 0 1 1 0 1 1"
    indice = texto.find(PAQ)
    # Verificando se a sequência foi encontrada
    if indice != -1:
        # Armazenando a parte da string a partir da sequência encontrada
        substring = texto[indice:]
        print(f"foi encontrado")
        return substring
    else:
        print(f"não foi encontrada.")
        return "Erro"

# Abrir o arquivo em modo escrita
with open("saida.txt", "w") as saida:
    with open("RX(vetor)MQ_v2.txt", "r") as entrada:
        for linha in entrada:
            saida.write(leitura(linha))
            

