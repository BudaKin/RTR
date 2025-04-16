def quebrar_linha(texto, tamanho):
    return '\n'.join([texto[i:i+tamanho] for i in range(0, len(texto), tamanho)])

def leitura(texto: str):
    indice = 0
    PAQ = "10011011"
    while 1:
        indice = texto.find(PAQ, indice)
        # Verificando se a sequência foi encontrada
        if indice != -1 and len(texto) > 512 + indice:
            if texto[indice+257] == "1":
                if (texto.find(PAQ, indice+8) == 512 + indice):
                    substring = texto[indice:]
                    print(f"foi encontrado a primeira flag: {indice}")
                    return substring
            print(f"flag errada em: {indice}")
            indice = indice+8
        else:
            print(f"não foi encontrada.")
            return "Erro"


# Abrir o arquivo em modo escrita

arquivo = "RX(vetor)MQ_v2.txt"

with open("saida.txt", "w") as saida:
    with open(arquivo, "r") as entrada:
        texto = entrada.read()
        substring = ''.join([c for c in texto if c in '01'])
        lido = leitura(substring)
        lido = ' '.join(lido)
        lido = quebrar_linha(lido, 128)
        saida.write(lido)
            

