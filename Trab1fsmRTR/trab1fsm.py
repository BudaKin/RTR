from enum import Enum

PAQ = "10011011"
PAMQ = "0000"
DIST_PAMQ = 128
Quadro = 256
MultiQuadro = 4096
Bit = 1
Byte = 8

class Estado(Enum):
  Realinhando=0
  Alinhado=1
  Finalizado=2

class ProtPAMQ:

  def __init__(self):
    self.estado = Estado.Realinhando
    self.indice = 0

  def mef(self, sstring, canal):
    # este método identifica o estado atual, e chama o tratador correspondente
    # print(f"[DEBUG] Estado: {self.estado}, Indice: {self.indice}")
    if self.estado == Estado.Realinhando:
      self.handle_realinhando(sstring)
    elif self.estado == Estado.Alinhado:
      self.handle_alinhado(sstring, canal)
    elif self.estado == Estado.Finalizado:
      self.handle_finalizado(sstring)

  def handle_realinhando(self, sstring):
      # tratador de eventos no estado Realinhando
    if self.indice + DIST_PAMQ > len(sstring):
      self.estado = Estado.Finalizado
      return
    if sstring[self.indice + DIST_PAMQ : self.indice + DIST_PAMQ + 4*Bit] == PAMQ:
      self.estado = Estado.Alinhado
    else:
      self.indice += Quadro
      self.estado = Estado.Realinhando

  def handle_alinhado(self, sstring, canal):
    # tratador de eventos no estado Alinhado
    canal_r = canal
    salto = 0

    if canal_r > 16:
      canal_r -= 15
      salto += 4*Bit

    Dist_desejada = self.indice + Quadro * canal_r + DIST_PAMQ + salto

    if Dist_desejada > len(sstring):
      self.estado = Estado.Finalizado
      return
    elif sstring[self.indice + DIST_PAMQ : self.indice + DIST_PAMQ + 4*Bit] != PAMQ:
      print(f"Desalinhado!")
      self.estado = Estado.Realinhando
      return
    else:
      info = sstring[Dist_desejada : Dist_desejada + 4*Bit]
      print(f"Canal: {canal}, informação: {info}")
      self.indice += MultiQuadro
      self.estado = Estado.Alinhado

  def handle_finalizado(self, sstring):
    # tratador de eventos no estado Finalizado
    pass

class ProtPAQ:

  def __init__(self):
    self.estado = Estado.Realinhando
    self.indice = 0
    self.cstring = []

  def mef(self, sstring):
    # este método identifica o estado atual, e chama o tratador correspondente
    # print(f"[DEBUG] Estado: {self.estado}, Indice: {self.indice}")
    if self.estado == Estado.Realinhando:
      self.handle_realinhando(sstring)
    elif self.estado == Estado.Alinhado:
      self.handle_alinhado(sstring)
    elif self.estado == Estado.Finalizado:
      self.handle_finalizado(sstring)

  def handle_realinhando(self, sstring):
    # tratador de eventos no estado Realinhando
    indice_local = self.indice
    indice_local = sstring.find(PAQ, indice_local)
    print(f"Sequência parecida com um PAQ encontrado no Indice: {indice_local}")
    if indice_local == -1:
      print(f"Fim do Arquivo.")
      self.estado = Estado.Finalizado
      return
    self.indice = indice_local
    indice_local += Quadro
    if indice_local + Bit < len(sstring) and sstring[indice_local + Bit] == '1':
        indice_local += Quadro
        if indice_local + Byte < len(sstring) and sstring[indice_local: indice_local + Byte] == PAQ:
          print(f"Era um PAQ mesmo, Alinhado.")
          self.estado = Estado.Alinhado
          return
    if self.indice > len(sstring):
      self.estado = Estado.Finalizado
    else:
      self.indice += Byte
      self.estado = Estado.Realinhando

  def handle_alinhado(self, sstring):
    # tratador de eventos no estado Alinhado
    if self.indice + 2*Quadro > len(sstring):
      self.estado = Estado.Finalizado
      return
    self.cstring.append(sstring[self.indice: self.indice + 2*Quadro])
    self.indice += 2*Quadro
    if self.indice + Byte < len(sstring) and sstring[self.indice: self.indice + Byte] != PAQ:
      self.cstring.append(sstring[self.indice: self.indice + 2*Quadro])
      self.indice += 2*Quadro
      if self.indice + Byte < len(sstring) and sstring[self.indice: self.indice + Byte] != PAQ:
        self.cstring.append(sstring[self.indice: self.indice + 2*Quadro])
        self.indice += 2*Quadro
        if self.indice + Byte < len(sstring) and sstring[self.indice: self.indice + Byte] != PAQ :
          print(f"Perda de Alinhamento, Realinhando...")
          self.estado = Estado.Realinhando
          return
    self.estado = Estado.Alinhado

  def handle_finalizado(self, sstring):
    # tratador de eventos no estado Finalizado
    pass
  
# Abrir o arquivo em modo escrita

def quebrar_linha(texto, tamanho):
    return '\n'.join([texto[i:i+tamanho] for i in range(0, len(texto), tamanho)])

def leitura(texto: str):
  prot = ProtPAQ()
  while prot.estado != Estado.Finalizado:
    prot.mef(texto)
  print(f"Leitura Finalizada!")
  return ''.join(prot.cstring)

def ver_pamq(texto: str, canal: int):
  prot = ProtPAMQ()
  while prot.estado != Estado.Finalizado:
    prot.mef(texto, canal)
  print(f"Verificação do PAMQ concluída!")

arquivo = "RX(vetor)MQ_v2.txt"
canal_desejado = 30

if canal_desejado < 1 or canal_desejado > 30:
  print(f"Escolha um canal válido! (entre 1 e 30)")
  exit(-1)

with open("saida_fsm.txt", "w") as saida:
    with open(arquivo, "r") as entrada:
        texto = entrada.read()
        substring = ''.join([c for c in texto if c in '01'])
        lido = leitura(substring)
        ver_pamq(lido, canal_desejado)
        lido = ' '.join(lido) # seapara cada bit por um espaço
        lido = quebrar_linha(lido, 128) # quebra a linha a cada 128 bits
        saida.write(lido)
