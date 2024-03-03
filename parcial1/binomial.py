#Primero, importamos todas las librerias necesarias
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import math
import streamlit as st
import streamlit.components.v1 as components
from scipy.stats import binom

#Ahora, haremos los ajustes necesarios para la pagina de streamlit
st.set_page_config(page_title="Pacrial 1", page_icon="🌍", layout="wide")
st.markdown("<h1 style='text-align: center; color: blue;'>Distribución Binomial</h1>", unsafe_allow_html=True)
st.markdown("""
La **distribución binomial** es un modelo de probabilidad que describe el número de éxitos en una secuencia de ensayos independientes, donde cada ensayo tiene exactamente dos resultados posibles: éxito o fracaso. 

Esta distribución está definida por dos parámetros: la probabilidad de éxito en un solo ensayo (p) y el número total de ensayos (n).
""")
st.markdown("""La fórmula para calcular la probabilidad de exactamente k éxitos en n ensayos, con una probabilidad de éxito p, es:""")

st.latex(r''' P(x = k) = \binom{n}{k} p^{k} (1-p)^{n-k} ''')

st.markdown("""Donde:
- (n k) es el coeficiente binomial.
- p es la probabilidad de éxito en un solo ensayo.
- (1 - p) es la probabilidad de fracaso en un solo ensayo.
""")
st.markdown(""" En el caso de esta paágina de streamlit, lo que se realizó fue: Crear tres inputs para que el usuario pueda ingresar la probabilidad de que el evento deseado suceda, la cantidad de intentos y la cantidad de intentos que se desea que sean exitosos. Tras esto se utilizó la libreria scipy para calcular la distribución binomial y plotearla dentro de la gráfica que se muestra en la parte de abajo, la cual cambiará dependiendo de los valores que el usuario ingrese. En cuanto a los widget inputs que se utilizaron, estos fueron solamente tres number inputs, los cuales tienen limitados los números que pueden ser elegidos para que no se generen errores a la hora de hacer los cálculos.""")
st.sidebar.header("Ingreso de Datos")
st.sidebar.markdown("""Esta sección esta destinada para ingresar los datos necesarios para calcular una distribución binomial. Apartir de los datos que sean ingresados en cada recuadro, se le mostrará la distribución binomial equivalente a esos""")
st.sidebar.image("ECFMLOGO.png")

#Aquí vamos a solicitar al usuario que ingrese todos los datos necesarios para calcular la distribución
prob_exit=st.sidebar.number_input(f"Ingresar la probabilidad de encontrar", min_value=0.00, max_value=1.00,step=0.01, value=0.5)
num_intentos=st.sidebar.number_input(f"Ingresar el número de intentos", min_value=0, max_value=90, step=1, value=10)
num_exit=st.sidebar.number_input(f"Ingrese el número de casos exitosos deseados", min_value=0, max_value=90, step=1, value=5)

#Agragamos el logo de la escuela para que se vea elegante

#Aquí usamos scipy para calcular la probabilidad de obtener cierto resultado
x = list(range(num_intentos + 1))
prob = binom.pmf(x, num_intentos, prob_exit)

#Calculamos la probabilidad esperada
prob_esp = binom.pmf(num_exit, num_intentos, prob_exit) if num_exit is not None else None

#Ya con toda la información, podemos plotear la distribución binomial
fig = px.bar(x=x, y=prob, labels={'x': 'Número de casos exitosos', 'y': 'Probabilidad'})
fig.update_layout(
    title='DISTRIBUCIÓN BINOMIAL PARA DATOS SELECCIONADOS',
    xaxis_title='Número de casos exitosos',
    yaxis_title='Probabilidad',
    plot_bgcolor='rgba(0, 0, 0, 0)', #Establece el color del plot background (transparente)
    paper_bgcolor='rgba(0, 0, 0, 0)', #Establece el color del paper background (transparente)
    xaxis=dict(showgrid=True, gridcolor='#cecdcd'), #Establece el color del eje x
    yaxis=dict(showgrid=True, gridcolor='#cecdcd'), #Establece el color del eje y
    font=dict(color='#cecdcd'), #Hace que el texto sea de color negro 
    showlegend=True 
)
#Ahora, para que se vea mejor, haremos que una linea remarque el número de casos exitosos que se escogió
if num_exit is not None:
    fig.add_vline(x=num_exit, line_dash='dash', line_color='red',
                  annotation_text=f"Casos exitosos seleccionados: {num_exit}", annotation_position="top right")
st.plotly_chart(fig, use_container_width=True)

#Este es un recuadro que va a mostrar la probabilidad esperada para el caso seleccionado
if prob_esp is not None:
    st.success(f"**La probabilidad esperada para {num_exit} casos de exito es: {prob_esp}**")

data = {'Número de Éxitos (x)': x, 'Probabilidad': prob}
st.table(data)
