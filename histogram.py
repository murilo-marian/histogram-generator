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
