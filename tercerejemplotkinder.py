# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 20:09:30 2018

@author: qwerty
"""
import numpy as np
from skimage import io
from skimage.feature import greycomatrix, greycoprops
from sklearn.cluster import KMeans
#from matplotlib import pyplot as plt
from scipy.spatial import distance
import scipy.misc

import tkinter
from tkinter.constants import *




def abrir1():
    ventana.filename = filedialog.askopenfilename(initialdir = "C:/Users/qwerty/Desktop/PDI_spyder/imagenes",title = "Elige Tu Archivo De Imagen:", filetypes = (("Imagenes PNG", "*.png"),("Imagenes GIF ", "*.gif")))    
    global ruta    
    ruta = ventana.filename
    imagenL = PhotoImage(file = ruta)
    print(imagenL)

    global abrirImagen
    abrirImagen = canvas.create_image(1, 150, anchor=NW, image=imagenL)
    ventana.mainloop()
    
def abrir2():
    ventana.filename2 = filedialog.askopenfilename(initialdir = "C:/Users/qwerty/Desktop/PDI_spyder/imagenes",title = "Elige Tu Archivo De Imagen:", filetypes = (("Imagenes PNG", "*.png"),("Imagenes GIF ", "*.gif")))    
    global ruta2
    ruta2 = ventana.filename2
    imagenL = PhotoImage(file = ruta2)
    print("imagen: " + imagenL)

    global abrirImagen2
    abrirImagen2 = canvas.create_image(600, 150, anchor=NW, image=imagenL)
    ventana.mainloop()





#-----------------INTERFAZ------------------------------------------------------------------
"""Creacion De Ventana Y Lienzo (Canvas)"""
ventana = Tk()
w = 1000
h = 650
extraW=ventana.winfo_screenwidth() - w
extraH=ventana.winfo_screenheight() - h
ventana.geometry("%dx%d%+d%+d" % (w, h, extraW / 2, extraH / 2))
canvas = Canvas(ventana, width=1200, height=650)
canvas.pack()
ventana.title("Procesamiento digital de imagenes")
entrada = IntVar()




#-----------------CODIGO--------------------------------
def todo():
    def lectura_de_imagenes():
        img_1 = urlopen(ruta)
        img_2 = urlopen(ruta1)

        ruta1 = Image.open(img_1)
        ruta22 = Image.open(img_2)
        return io.imread(ruta1, as_grey=True)*255, io.imread(ruta22)
    
    

    imo,im = lectura_de_imagenes()
    imout = np.zeros(im.size)  
    imn = imo
    csal = [237,28,36]
    cnosal = [0,0,255]


    def coordenadas():
        coordenadas_sal = []
        coordenadas_no_sal = []
        for filas, i in enumerate(im):
            for  columna, pixel in enumerate (i):
                if all(pixel == csal) :  
                    coordenadas_sal.append([filas,columna])
              
                if all(pixel == cnosal) :  
                    coordenadas_no_sal.append([filas,columna])
        return coordenadas_sal,coordenadas_no_sal
    
    
    coord_sal,coord_nosal= coordenadas()
    tamaño_ventana = 25
    mitadvent = int((tamaño_ventana-1)/2)
    [fi,ci] = imo.shape
    
    
    def propiedades_glcm():
        valsal = np.zeros((len(coord_sal),6))
        glcm = np.zeros((256,256,8), dtype=np.double)
        
            
        ventana_sal = []
        i = 0
        for loc in coord_sal:
        
            ventana_sal= (imo[loc[0]-mitadvent:loc[0] + mitadvent, loc[1]-mitadvent:loc[1] + mitadvent])
            venttemp=np.array(ventana_sal)
            glcm = greycomatrix(venttemp.astype(int), [5],[0,45,90,180,135,225,270,315], 256,symmetric=True, normed=True)
            valsal[i] = (np.mean(greycoprops(glcm,prop= 'correlation')),np.mean(greycoprops(glcm,prop= 'dissimilarity')),np.mean(greycoprops(glcm,prop='contrast')),np.mean(greycoprops(glcm,prop='homogeneity')),np.mean( greycoprops(glcm,prop='ASM')),np.mean(greycoprops(glcm, prop= 'energy')))
            i+=1
            print(i)   
    
        
        val_nosal = np.zeros((len(coord_nosal),6))
        ventana_no_sal = []
        i = 0
        for loc in coord_nosal:
            if (loc[0]+(tamaño_ventana+1)/2)<fi and (loc[0]-(tamaño_ventana+1)/2)>0 and (loc[1]+(tamaño_ventana+1)/2)<ci and (loc[1]-(tamaño_ventana+1)/2)>0:
               ventana_no_sal= (imo[loc[0]-mitadvent:loc[0] + mitadvent, loc[1]-mitadvent:loc[1] + mitadvent])
               venttemp=np.array(ventana_no_sal)
               glcm = greycomatrix(venttemp.astype(int), [5],[0,45,90,180,135,225,270,315], 256,symmetric=True, normed=True)
     
               val_nosal[i] = (np.mean(greycoprops(glcm,prop= 'correlation')),np.mean(greycoprops(glcm,prop= 'dissimilarity')),np.mean(greycoprops(glcm,prop='contrast')),np.mean(greycoprops(glcm,prop='homogeneity')),np.mean( greycoprops(glcm,prop='ASM')),np.mean(greycoprops(glcm, prop= 'energy')))
        
               i+=1
               print(i)   
        return valsal,val_nosal
    
    valsal,val_no_sal = propiedades_glcm()   
    def clustering():
    
        X = np.concatenate((valsal, val_no_sal))
        kmeans = KMeans(n_clusters=2, random_state=0)
        kmeans.fit(X)
         
        kmeans.labels_.tolist()
        return kmeans.cluster_centers_
    
    centroides = clustering()
    
    imo2 = imo
    def pintar():
        
        for fila, i in enumerate(imo):
            for  columna, j in enumerate (i):
                
                if (fila+(tamaño_ventana+1)/2)<fi and (fila-(tamaño_ventana+1)/2)>0 and (columna+(tamaño_ventana+1)/2)<ci and (columna-(tamaño_ventana+1)/2)>0:
                    ventana_imo = (imo[fila-mitadvent:fila + mitadvent, columna-mitadvent:columna + mitadvent])
                    venttemp=np.array(ventana_imo)
                    glcm = greycomatrix(venttemp.astype(int), [5],[0,45,90,180,135,225,270,315], 256,symmetric=True, normed=True)
     
                    L = (np.mean(greycoprops(glcm,prop= 'correlation')),np.mean(greycoprops(glcm,prop= 'dissimilarity')),np.mean(greycoprops(glcm,prop='contrast')),np.mean(greycoprops(glcm,prop='homogeneity')),np.mean( greycoprops(glcm,prop='ASM')),np.mean(greycoprops(glcm, prop= 'energy')))
               
                    dist1 = distance.euclidean(L,centroides[0])
                    dist2 = distance.euclidean(L, centroides[1])
                    if dist1 < dist2:
                        imo2[fila,columna] = 0
                    
        io.imshow(imo2)
        io.show()
        return scipy.misc.imsave('C:/Users/qwerty/Desktop/PDI_spyder/imagenes/finalhx.png',imo2)          
    
    pin = pintar()
    
    
    
    
#-----------------BOTON--------------------------------
botonI = tkinter.Button(ventana, text="Imprimir",width=13, height=2,fg="blue",command=todo).place(x=600, y=650)





#-----------------LABELS--------------------------------
Label(text = "IMAGEN ORIGINAL", font= ("Times New Roman",14)).place(x=190, y=120)
Label(text = "IMAGEN INTERPRETADA", font= ("Times New Roman",14)).place(x=800, y=120)
#Label(text = "IMAGEN PROCESADA", font= ("Times New Roman",14)).place(x=640, y=120)

#--------------------------MENU--------------------
"""Creacion De Los Menus"""
barraMenu = Menu(ventana)
mnuInicio = Menu(barraMenu)
#-------------OPCIONES DE MENU
"""Menu opciones"""
mnuInicio.add_command(label = "Abrir Imagen ORIGINAL", command = abrir)
mnuInicio.add_command(label = "Abrir Imagen INTERPRETADA", command = abrir2)
mnuInicio.add_separator()

############################################################################################

barraMenu.add_cascade(label = "Inicio", menu = mnuInicio)
ventana.config(menu = barraMenu)
ventana.mainloop()




