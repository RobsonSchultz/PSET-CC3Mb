# IDENTIFICAÇÃO DO ESTUDANTE:
# Preencha seus dados e leia a declaração de honestidade abaixo. NÃO APAGUE
# nenhuma linha deste comentário de seu código!
#
#    Nome completo: Robson Júnior Schultz Dias
#    Matrícula: 202307200
#    Turma: CC3Mb
#    Email: robsonjsd2003@gmail.com
#
# DECLARAÇÃO DE HONESTIDADE ACADÊMICA:
# Eu afirmo que o código abaixo foi de minha autoria. Também afirmo que não
# pratiquei nenhuma forma de "cola" ou "plágio" na elaboração do programa,
# e que não violei nenhuma das normas de integridade acadêmica da disciplina.
# Estou ciente de que todo código enviado será verificado automaticamente
# contra plágio e que caso eu tenha praticado qualquer atividade proibida
# conforme as normas da disciplina, estou sujeito à penalidades conforme
# definidas pelo professor da disciplina e/ou instituição.


# Imports permitidos (não utilize nenhum outro import!):
import sys
import math
import base64
import tkinter
from io import BytesIO
from PIL import Image as PILImage


def caixa_desfoque(n):
    """
    Cria um kernel de desfoque n por n que será usado para calcular
    o valor médio ao redor do pixel sendo analizado.
    """

    kernel = []                     # Cria o kernel.
    for i in range(n):              # Loop Y.
        linha = []                  # Cria as linhas do kernel.
        for j in range(n):          # Loop X.
            linha.append(1/n**2)    # Adiciona os valores nas linhas.
        kernel.append(linha)        # Adiciona a linha ao kernel.
    return kernel                   # Retorna o valor do kernel.

# Classe Imagem:
class Imagem:
    def __init__(self, largura, altura, pixels):
        self.largura = largura
        self.altura = altura
        self.pixels = pixels

    def get_pixel(self, x, y):
        """
        Retorna o valor contido no pixel na posição (x, y).
        """
        return self.pixels[x + (y * self.largura)]  # Com essa fórmula, pode-se ler a imagem como matriz
                                                    # mesmo que os pixels estejam armazenados num vetor.

    def get_pixel_fora_dos_limites(self, x, y):
        """
        Retorna o valor contido no pixel na posição (x, y).
        Se o valor do pixel estiver fora dos limites, retorna o valor do pixel válido mais próximo.
        """


        if x > self.largura - 1:        # Se o pixel estiver fora dos limites da matriz para a direita,
            x = self.largura - 1        # receberá x = largura - 1.
                                        #
        elif x < 0:                     # Se o pixel estiver fora dos limites da matriz para a esquerda,
            x = 0                       # receberá x = 0.
                                        #
        if y > self.altura - 1:         # Se o pixel estiver fora dos limites da matriz para baixo,
            y = self.altura - 1         # receberá y = largura - 1.
                                        #
        elif y < 0:                     # Se o pixel estiver fora dos limites da matriz para cima,
            y = 0                       # receberá y = 0.
                                        #
        return self.get_pixel(x, y)     # Valor é retornado para a função get_pixel.

    def set_pixel(self, x, y, c):
        """
        Define o valor do pixel na posição (x, y) com o valor c.
        """

        self.pixels[x + (y * self.largura)] = c  # Mesma fórmula utilizada no get_pixel.

    def aplicar_por_pixel(self, func):
        """
        Retorna uma nova imagem, onde os novos pixels são resultado da função func.
        """

        resultado = Imagem.nova(self.largura, self.altura)  # Altura e largura estavam invertidas nessa linha.
        for x in range(resultado.largura):                  # Loop x.
                                                            # Não faz sentido ter as variáveis nova cor e y dentro do
                                                            # loop for x, pois já serão alteradas no for y.
            for y in range(resultado.altura):               # Loop y.
                cor = self.get_pixel(x, y)                  # Recebe o valor do pixel.
                nova_cor = func(cor)                        # Define a nova cor do pixel.
                resultado.set_pixel(x, y, nova_cor)         # Esta linha deveria estar dentro do loop for, porém, no código
                                                            # original ela estava fora. x e y também estavam invertidos.
                                                            #
        return resultado                                    # Retorna o resultado.

    def invertida(self):
        """
        Retorna uma nova imagem com o valor invertido de cada pixel.
        """

        return self.aplicar_por_pixel(lambda c: 255 - c)    # O número de pixels estava como 256, o que não está correto.

    def faixa_de_pixels(self):
        """
        Quando um pixel tiver o valor menor que 0, ele receberá 0
        e quando tiver o valor maior que 255, receberá 255.
        """

        for i in range(len(self.pixels)):           # Loop dos pixels.
            self.pixels[i] = round(self.pixels[i])  # Arredonda e torna o valor inteiro.
            if self.pixels[i] < 0:                  # Se o valor do pixel for menor que 0,
                self.pixels[i] = 0                  # ele receberá 0.
            elif self.pixels[i] > 255:              # Se o valor do pixel for maior que 255,
                self.pixels[i] = 255                # ele receberá 255.

    def correlacao(self, kernel):
        """
        Retorna uma nova imagem, aplicando o processo de correlação
        entre a imagem de entrada e o kernel
        """

        saida = Imagem.nova(self.largura, self.altura)                                                          # Cria uma nova imagem para armazenar o resultado da correlação.
        tamanho_kernel = len(kernel)//2                                                                         # Distância do centro para a borda do kernel.
        for x in range(self.largura):                                                                           # Loop X da imagem.
            for y in range(self.altura):                                                                        # Loop Y da imagem.
                pixel_correlacionado = 0                                                                        # inicia o valor do pixel correlacionado como 0.
                for x1 in range(len(kernel)):                                                                   # Loop X do kernel.
                    for y1 in range(len(kernel)):                                                               # Loop Y do kernel.
                        posx = x - tamanho_kernel + x1                                                          # Posição retornada para X.
                        posy = y - tamanho_kernel + y1                                                          # Posição retornada para Y.
                        pixel_correlacionado += self.get_pixel_fora_dos_limites(posx, posy) * kernel[y1][x1]    # Realiza a correlação entre o pixel da imagem original e o valor do kernel.
                    saida.set_pixel(x, y, pixel_correlacionado)                                                 # Define o valor do pixel.
        return saida                                                                                            # Retorna a saida.

    def borrada(self, n):
        """
        Cria uma nova imagem borrada
        usando uma kernel de desfoque n por n.
        """

        saida = self.correlacao(caixa_desfoque(n))  # Faz a correlação usando um kernel de desfoque.
        saida.faixa_de_pixels()                     # Elimina valores de pixel menores que 0 ou maiores que 255.
        return saida                                # Retorna a imagem borrada.

    def focada(self, n):
        """
        Cria uma nova imagem focada
        usando uma versão borrada da propria imagem.
        """
        saida = Imagem.nova(self.largura, self.altura)                      # Cria uma nova imagem.
        borrada = self.correlacao(caixa_desfoque(n))                        # Carrega a imagem borrada que será usada na função.
        for x in range(self.largura):                                       # Loop X.
            for y in range(self.altura):                                    # Loop Y.
                sxy = 2 * self.get_pixel(x, y) - borrada.get_pixel(x, y)    # Fórmula da imagem focada, como exemplificada no arquivo do PSET.
                saida.set_pixel(x, y, sxy)                                  # Define o valor do pixel.
        saida.faixa_de_pixels()                                             # Elimina valores de pixel menores que 0 ou maiores que 255.
        return saida                                                        # Retorna a imagem focada.

    def bordas(self):
        """
        Cria uma nova imagem com as bordas da imagem original
        resultante da aplicação do operador sobel.
        """

        saida = Imagem.nova(self.largura, self.altura)
        kx = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]                                   # Cria o kernel X.
        ky = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]                                   # Cria o kernel Y.
        ox = self.correlacao(kx)                                                    # Faz a correlação usando o kernel X.
        oy = self.correlacao(ky)                                                    # Faz a correlação usando o kernel Y.
        for x in range(self.largura):                                               # Loop X.
            for y in range(self.altura):                                            # Loop Y.
                oxy = math.sqrt((ox.get_pixel(x, y)**2) + (oy.get_pixel(x, y)**2))  # Fórmula do operador Sobel, como exemplificada no arquivo do PSET.
                saida.set_pixel(x, y, oxy)                                          # Define o valor do pixel.
        saida.faixa_de_pixels()                                                     # Elimina valores de pixel menores que 0 ou maiores que 255.
        return saida                                                                # Retorna a imagem com as bordas.


    # Abaixo deste ponto estão utilitários para carregar, salvar e mostrar
    # as imagens, bem como para a realização de testes. Você deve ler as funções
    # abaixo para entendê-las e verificar como funcionam, mas você não deve
    # alterar nada abaixo deste comentário.
    #
    # ATENÇÃO: NÃO ALTERE NADA A PARTIR DESTE PONTO!!! Você pode, no final
    # deste arquivo, acrescentar códigos dentro da condicional
    #
    #                 if __name__ == '__main__'
    #
    # para executar testes e experiências enquanto você estiver executando o
    # arquivo diretamente, mas que não serão executados quando este arquivo
    # for importado pela suíte de teste e avaliação.
    def __eq__(self, other):
        return all(getattr(self, i) == getattr(other, i)
                   for i in ('altura', 'largura', 'pixels'))

    def __repr__(self):
        return "Imagem(%s, %s, %s)" % (self.largura, self.altura, self.pixels)

    @classmethod
    def carregar(cls, nome_arquivo):
        """
        Carrega uma imagem do arquivo fornecido e retorna uma instância dessa
        classe representando essa imagem. Também realiza a conversão para tons
        de cinza.

        Invocado como, por exemplo:
           i = Imagem.carregar('test_images/cat.png')
        """
        with open(nome_arquivo, 'rb') as guia_para_imagem:
            img = PILImage.open(guia_para_imagem)
            img_data = img.getdata()
            if img.mode.startswith('RGB'):
                pixels = [round(.299 * p[0] + .587 * p[1] + .114 * p[2]) for p in img_data]
            elif img.mode == 'LA':
                pixels = [p[0] for p in img_data]
            elif img.mode == 'L':
                pixels = list(img_data)
            else:
                raise ValueError('Modo de imagem não suportado: %r' % img.mode)
            l, a = img.size
            return cls(l, a, pixels)

    @classmethod
    def nova(cls, largura, altura):
        """
        Cria imagens em branco (tudo 0) com a altura e largura fornecidas.

        Invocado como, por exemplo:
            i = Imagem.nova(640, 480)
        """
        return cls(largura, altura, [0 for i in range(largura * altura)])

    def salvar(self, nome_arquivo, modo='PNG'):
        """
        Salva a imagem fornecida no disco ou em um objeto semelhante a um arquivo.
        Se o nome_arquivo for fornecido como uma string, o tipo de arquivo será
        inferido a partir do nome fornecido. Se nome_arquivo for fornecido como
        um objeto semelhante a um arquivo, o tipo de arquivo será determinado
        pelo parâmetro 'modo'.
        """
        saida = PILImage.new(mode='L', size=(self.largura, self.altura))
        saida.putdata(self.pixels)
        if isinstance(nome_arquivo, str):
            saida.save(nome_arquivo)
        else:
            saida.save(nome_arquivo, modo)
        saida.close()

    def gif_data(self):
        """
        Retorna uma string codificada em base 64, contendo a imagem
        fornecida, como uma imagem GIF.

        Função utilitária para tornar show_image um pouco mais limpo.
        """
        buffer = BytesIO()
        self.salvar(buffer, modo='GIF')
        return base64.b64encode(buffer.getvalue())

    def mostrar(self):
        """
        Mostra uma imagem em uma nova janela Tk.
        """
        global WINDOWS_OPENED
        if tk_root is None:
            # Se Tk não foi inicializado corretamente, não faz mais nada.
            return
        WINDOWS_OPENED = True
        toplevel = tkinter.Toplevel()
        # O highlightthickness=0 é um hack para evitar que o redimensionamento da janela
        # dispare outro evento de redimensionamento (causando um loop infinito de
        # redimensionamento). Para maiores informações, ver:
        # https://stackoverflow.com/questions/22838255/tkinter-canvas-resizing-automatically
        tela = tkinter.Canvas(toplevel, height=self.altura,
                              width=self.largura, highlightthickness=0)
        tela.pack()
        tela.img = tkinter.PhotoImage(data=self.gif_data())
        tela.create_image(0, 0, image=tela.img, anchor=tkinter.NW)

        def ao_redimensionar(event):
            # Lida com o redimensionamento da imagem quando a tela é redimensionada.
            # O procedimento é:
            #  * converter para uma imagem PIL
            #  * redimensionar aquela imagem
            #  * obter os dados GIF codificados em base 64 (base64-encoded GIF data)
            #    a partir da imagem redimensionada
            #  * colocar isso em um label tkinter
            #  * mostrar a imagem na tela
            nova_imagem = PILImage.new(mode='L', size=(self.largura, self.altura))
            nova_imagem.putdata(self.pixels)
            nova_imagem = nova_imagem.resize((event.width, event.height), PILImage.NEAREST)
            buffer = BytesIO()
            nova_imagem.save(buffer, 'GIF')
            tela.img = tkinter.PhotoImage(data=base64.b64encode(buffer.getvalue()))
            tela.configure(height=event.height, width=event.width)
            tela.create_image(0, 0, image=tela.img, anchor=tkinter.NW)

        # Por fim, faz o bind da função para que ela seja chamada quando a tela
        # for redimensionada:
        tela.bind('<Configure>', ao_redimensionar)
        toplevel.bind('<Configure>', lambda e: tela.configure(height=e.height, width=e.width))

        # Quando a tela é fechada, o programa deve parar
        toplevel.protocol('WM_DELETE_WINDOW', tk_root.destroy)


# Não altere o comentário abaixo:
# noinspection PyBroadException
try:
    tk_root = tkinter.Tk()
    tk_root.withdraw()
    tcl = tkinter.Tcl()


    def refaz_apos():
        tcl.after(500, refaz_apos)


    tcl.after(500, refaz_apos)
except:
    tk_root = None

WINDOWS_OPENED = False

if __name__ == '__main__':
    # O código neste bloco só será executado quando você executar
    # explicitamente seu script e não quando os testes estiverem
    # sendo executados. Este é um bom lugar para gerar imagens, etc.

    # Questão 2
    '''img = Imagem.carregar('test_images/bluegill.png')
    inv = img.invertida()
    inv.salvar('test_results/lligeulb.png')'''

    '''img = Imagem.carregar('test_images/whiteSox.png')
    inv = img.invertida()
    inv.salvar('test_results/realwhiteSox.png')'''

    '''img = Imagem.carregar('test_images/whiteSox.png')
        inv = img.invertida()
        inv.salvar('test_results/realwhiteSox.png')'''

    # Questão 4
    '''kernel = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [1, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0]]

    imagem = Imagem.carregar("test_images/pigbird.png")
    img_correlacao = imagem.correlacao(kernel)
    img_correlacao.salvar("porcassaro.png")
    img_correlacao.mostrar()'''

    '''img = Imagem.carregar('test_images/cat.png')
    bor = img.borrada(5)
    bor.mostrar()
    bor.salvar('test_results/bocarto.png')'''

    img = Imagem.carregar('test_images/fatu.png')
    foc = img.focada(11)
    foc.mostrar()
    foc.salvar('test_results/fatu.png')

    '''img = Imagem.carregar('test_images/construct.png')
    bord = img.bordas()
    bord.mostrar()
    bord.salvar('test_results/constroibordas.png')'''

    pass

    # O código a seguir fará com que as janelas de Imagem.mostrar
    # sejam exibidas corretamente, quer estejamos executando
    # interativamente ou não:
    if WINDOWS_OPENED and not sys.flags.interactive:
        tk_root.mainloop()
