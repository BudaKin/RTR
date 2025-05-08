from enum import Enum

PAQ = "10011011"
Quadro = 256
Bit = 1
Byte = 8

class Estado(Enum):
  Realinhando=0
  Alinhado=1
  Finalizado=2

class Protocolo:

  def __init__(self):
    self.estado = Estado.Realinhando
    self.indice = 0
    self.cstring = ""

  def mef(self, sstring):
    # este método identifica o estado atual, e chama o tratador correspondente
    if self.estado == Estado.Realinhando:
      self.handle_realinhando(sstring)
    elif self.estado == Estado.Alinhado:
      self.handle_alinhado(sstring)
    elif self.estado == Estado.Finalizado:
      self.handle_finalizado(sstring)

  def handle_realinhando(self, sstring):
    # tratador de eventos no estado Realinhando
    if sstring[indice: indice + Byte] == PAQ:
      indice += Quadro
      if sstring[indice + Bit] == 1:
         indice += Quadro
         if sstring[indice: indice + Byte] == PAQ:
          self.estado = Estado.Alinhado
    self.estado = Estado.Realinhando

  def handle_alinhado(self, sstring):
    # tratador de eventos no estado Alinhado
    indice += 2*Quadro
    if sstring[indice: indice + Byte] != PAQ:
      indice += 2*Quadro
      if sstring[indice: indice + Byte] != PAQ:
        indice += 2*Quadro
        if sstring[indice: indice + Byte] != PAQ:
          self.estado = Estado.Realinhando
    self.estado = Estado.Alinhado

  def handle_finalizado(self, sstring):
    # tratador de eventos no estado Finalizado
    pass
  
# Abrir o arquivo em modo escrita

def quebrar_linha(texto, tamanho):
    return '\n'.join([texto[i:i+tamanho] for i in range(0, len(texto), tamanho)])

def leitura(texto: str):
    prot:Protocolo
    indice = texto.find(PAQ, indice)
    if indice != -1 and len(texto) > 512 + indice:
      sstring = texto[indice:]
      while prot.estado != Estado.Finalizado:
        prot.mef(sstring)
    else:
      print(f"não foi encontrada.")
      return "Erro"
    

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

arquivo = "RX(vetor)MQ_v2.txt"

with open("saida.txt", "w") as saida:
    with open(arquivo, "r") as entrada:
        texto = entrada.read()
        substring = ''.join([c for c in texto if c in '01'])
        lido = leitura(substring)
        lido = ' '.join(lido) # seapara cada bit por um espaço
        lido = quebrar_linha(lido, 128) # quebra a linha a cada 128 bits
        saida.write(lido)
