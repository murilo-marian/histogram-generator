import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image

def calcular_histograma(img):
    histograma = [0] * 256  
    for linha in img:
        for pixel in linha:
            histograma[pixel] += 1  #cada ocorrência aumenta a frequência
    return histograma

def salvar_histograma_csv(histograma, nome_arquivo):
    intensidades = np.arange(256) #gera um n-dimensional array - legal de usar
    df = pd.DataFrame({"Intensidade": intensidades, "Frequência": histograma})
    df.to_csv(nome_arquivo, index=False)

#cinza
img_gray = Image.open('EntradaEscalaCinza.pgm')
img_gray_array = np.array(img_gray)
hist_gray = calcular_histograma(img_gray_array)
salvar_histograma_csv(hist_gray, "histograma_escala_cinza_manual.csv")

plt.figure()
plt.title("Histograma - Escala de Cinza")
plt.xlabel("Intensidade")
plt.ylabel("Frequência")
plt.bar(np.arange(256), hist_gray, color="gray")
plt.savefig("histograma_escala_cinza_manual.png")


# RGB
img_rgb = Image.open('EntradaRGB.ppm').convert("RGB")
img_rgb_array = np.array(img_rgb)

canais = ["R", "G", "B"]
cores = ["red", "green", "blue"]
plt.figure()
plt.title("Histograma - RGB")
plt.xlabel("Intensidade")
plt.ylabel("Frequência")

for i, canal in enumerate(canais): #separa os canais e manda calcular os histogramas
    canal_array = img_rgb_array[:, :, i]
    hist_canal = calcular_histograma(canal_array)
    salvar_histograma_csv(hist_canal, f"histograma_{canal}_manual.csv")
    plt.plot(hist_canal, color=cores[i], label=f"Canal {canal}")

plt.legend()
plt.savefig("histograma_rgb_manual.png")
plt.show()

def realce_por_histograma(output_path):
    Xmin = img_gray_array.min()
    Xmax = img_gray_array.max()
    
    a = 255.0 / (Xmax - Xmin)
    b = -a * Xmin
    
    # Y = aX + b
    img_realcada_array = (a * img_gray_array + b).clip(0, 255).astype(np.uint8)
    
    #formata o array numpy pra array normal [[P]]
    array_formatado = [ 
        [str(valor) for valor in linha]
        for linha in img_realcada_array
    ]
    
    saveIMG("imagemRealcada.pgm", "P2", 255, array_formatado, 800, 800)


def realce_rgb_por_histograma(output_path):
    canais_realçados = []
    for i in range(3):
        canal = img_rgb_array[:, :, i]
        Xmin = canal.min()
        Xmax = canal.max()
        
        a = 255.0 / (Xmax - Xmin)
        b = -a * Xmin
        
        canal_realcado = (a * canal + b).clip(0, 255).astype(np.uint8)
        canais_realçados.append(canal_realcado)
    
    img_realcada_array = np.stack(canais_realçados, axis=-1)
    
    #formata o array numpy pra array normal [[R G B]]
    array_formatado = [
        [" ".join(map(str, pixel)) for pixel in linha]
        for linha in img_realcada_array
    ]
    
    saveIMG("imagemRealcadaRGB.ppm", "P3", 255, array_formatado, 800, 800)


def saveIMG(filename, type, bits, pixels, width, height):
    with open(filename, "w") as newImage:
        newImage.write(type + "\n")
        newImage.write(str(width) + " " + str(height) + "\n")
        newImage.write(str(bits) + "\n")
        
        for row in pixels:
            newImage.write(" ".join(map(str, row)) + "\n")
        print("saved")


realce_por_histograma('ImagemRealcada.pgm')
realce_rgb_por_histograma('ImagemRGBRealcada.ppm')

