import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
from scipy.stats import linregress
import plotly.express as px
import seaborn as sns
import altair as alt
import math 
sns.set()

#Configuración de la página
st.set_page_config(page_title="Práctica 3: Deaimiento de Cesio-137", page_icon="☢️", layout="wide")

#diseño css y animación de los covichus
custom_css = """
<style>
/* Bordes laterales */
.stApp {
    border-left: 200px solid #D7C7F7; /* Color del borde izquierdo */
    border-right: 200px solid #D7C7F7; /* Color del borde derecho */
}

/* Animación del simbolo de radioactivo cayendo */
@keyframes falling {
    0% { transform: translateY(-100%); }
    100% { transform: translateY(100vh); }
}

/* Estilo para los cuidado peligro */
.falling-emoji {
    position: fixed;
    animation: falling 7s linear infinite;
    font-size: 3em;
}

/* posición cuidado peligro */
#emoji1 { left: 30px; }
#emoji2 { left: 120px; }
#emoji3 { right: 30px; }
#emoji4 { right: 120px; }
</style>
"""

# Se agrega el diseño CSS a streamlit
st.markdown(custom_css, unsafe_allow_html=True)

# Aquí se agregan los simbolos de CUIDADO PELIGRO 
st.markdown('<div class="falling-emoji" id="emoji1">☣</div>', unsafe_allow_html=True)
st.markdown('<div class="falling-emoji" id="emoji2">☣</div>', unsafe_allow_html=True)
st.markdown('<div class="falling-emoji" id="emoji3">☣</div>', unsafe_allow_html=True)
st.markdown('<div class="falling-emoji" id="emoji4">☣</div>', unsafe_allow_html=True)
st.markdown('<div class="falling-emoji" id="emoji1">☣</div>', unsafe_allow_html=True)
st.markdown('<div class="falling-emoji" id="emoji2">☣</div>', unsafe_allow_html=True)
st.markdown('<div class="falling-emoji" id="emoji3">☣</div>', unsafe_allow_html=True)
st.markdown('<div class="falling-emoji" id="emoji4">☣</div>', unsafe_allow_html=True)
st.markdown('<div class="falling-emoji" id="emoji1">☣</div>', unsafe_allow_html=True)
st.markdown('<div class="falling-emoji" id="emoji2">☣</div>', unsafe_allow_html=True)
st.markdown('<div class="falling-emoji" id="emoji3">☣</div>', unsafe_allow_html=True)
st.markdown('<div class="falling-emoji" id="emoji4">☣</div>', unsafe_allow_html=True)








# Menú lateral
with st.sidebar:
  selected=option_menu(
    menu_title="Menú",
    options = ["Principal", "Teoría"],
    icons = ["house-heart-fill", "envelope-heart-fill"],
    menu_icon = "heart-eyes-fill",
    default_index = 0,
  )
    

if selected == "Principal":
  #título
  st.markdown("<h1 style='text-align: center; color: #A2BDF1; text-shadow: 3px 3px #BEFBB3;'>- Decaimiento de Cesio-137 -</h1>", unsafe_allow_html=True)
  st.divider()
  st.markdown("<h2 style='text-align: left; color: #D3BEF1;'>Mediciones en el aire</h1>", unsafe_allow_html=True)
  st.markdown('<div style="text-align: justify;">Esta es la gráfica obtenida a partir de las mediciones tomadas, por el contador Geiger, en el aire. Para poder trabajar con estos datos, se separaron los casos y se agruparon para poder representarlos correctamente en la gráfica. Es decir, se contaron los casos donde se contaran 3 decaimientos y obtuvimos un total de 58, el cual es el caso mas frecuente. Además, para estos datos, se optó por utilizar una distribución de Poissón debido a la forma en que están distribuidos los datos, pues hay un evidente corriemiento hacia la derecha.</div>', unsafe_allow_html=True)
  #Primero vamos a definir el fit para la gráfica de las mediciones en el aire
  def fit(x):
      A=63.5733
      u=2.18871
      r=1.59884
      x = np.array(x, dtype=int)
      return A*math.exp(-((x-u)/r)**2/2)
  fit = np.vectorize(fit)
  #Ahora tomamos los datos que medimos con el contador geiger en el aire para poder graficarlos
  data_aire = pd.read_csv('https://raw.githubusercontent.com/Fabricio-mencos/LabRedDat/main/Practicas/Practica3/datos1.csv')
  df = pd.DataFrame(data_aire)
  value_range = np.arange(-3,df['Aire'].max()+1)
  count = df['Aire'].value_counts().reindex(value_range, fill_value=0).reset_index()
  print(count)
  #creamos la linea principal del gráfico
  plot_fit = px.line(x=value_range, y=fit(value_range))
  #Actualizamos el estilo del trazo
  plot_fit.update_traces(line_color='#9635E6', line_width=2.5, line_shape='spline')
  #cambiamos el color de fondo del gráfico
  plot_fit.update_layout({
    'plot_bgcolor': 'rgba(14, 7, 32, 0.8)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
   })
  #Cambiamos el nombre de los ejes del gráfico
  plot_fit.update_layout(
    xaxis_title='Decaimientos medidos',
    yaxis_title='Conteo de casos de decaimiento'
   )
  #agregamos las barras al gráfico
  plot_fit.add_bar(x=count['Aire'], y=count['count'],)
  #Por último, añadimos el gráfico a streamlit
  st.plotly_chart(plot_fit)
  st.divider()
  st.markdown("<h2 style='text-align: left; color: #D3BEF1;'>Mediciones con el Cesio-137</h1>", unsafe_allow_html=True)
  st.markdown('<div style="text-align: justify;">En este caso, de igual forma que en el anterior caso, agrupamos por casos la cantidad de decaimientos medidos para poder analizar correctamente toda la información. Para este caso, es evidennte ver que la distribución es una de tipo Gaussiana por la forma en que se distribuyeron los datos.</div>', unsafe_allow_html=True)
  #Ahora vamos a haer lo mismo que hicimos en la parte anterior, pero para los datos del cesio
  #Definimos el fit
  def fit2(x):
     A=25.382
     u=439.84
     r=19.6525
     x = np.array(x, dtype=int)
     return A*math.exp(-((x-u)/r)**2/2)
  fit2 = np.vectorize(fit2)
  #Tomamos los datos que medimos usando el cesio-137
  print(df['Cesio'].min())
  value_range2 = np.arange(df['Cesio'].min(),df['Cesio'].max()+1)
  count_2 = df['Cesio'].value_counts().reindex(value_range2, fill_value=0).reset_index()
  print(count_2)
  print(value_range2)
  group = np.arange(350, 505, 5)
  cesio_cut = df.groupby(pd.cut(df['Cesio'], group))['Cesio'].count()
  print(cesio_cut)
  data_cesio = pd.read_csv('https://raw.githubusercontent.com/Fabricio-mencos/LabRedDat/main/Practicas/Practica3/Cesio.csv')
  dfd = pd.DataFrame(data_cesio)
  #Ahora repetimos el proceso anterior para poder mostrar el fit y la gráfica en streamlit
  plot_fit2 = px.line(x=group, y=fit2(group))
  plot_fit2.update_traces(line_color='#9635E6', line_width=2.5, line_shape='spline')
  plot_fit2.update_layout({'plot_bgcolor': 'rgba(14, 7, 32, 0.8)','paper_bgcolor': 'rgba(0, 0, 0, 0)',})
  plot_fit2.update_layout(
    xaxis_title='Cantidad de Decaimientos',
    yaxis_title='Casos medidos'
   )
  plot_fit2.add_bar(x=group, y=dfd['count'])
  st.plotly_chart(plot_fit2)



        


    
  
if selected == "Teoría":
  st.divider()
  st.markdown("*USAC-ECFM. Laboratorio de reducción de datos.*")
  st.markdown("*Práctica 3. Decaimiento del Cesio-137*")
  st.markdown("*Mencos Calva, Allan Fabricio. 202106009,*")
  st.markdown("*Zapeta Hernández, Alejandra Dessiré. 202112959.*")
  st.divider()
  st.markdown("<h1 style='text-align: center; color: #A2BDF1; text-shadow: 3px 3px #BEFBB3;'>--- Cesio-137 ---</h1>", unsafe_allow_html=True)
  
  st.divider()
  st.markdown("<h3 style='text-align: left; color: black;'>Referencias</h1>", unsafe_allow_html=True)
  st.markdown("""  
  **1.**  Radionuclide Basics: Cesium-137 | US EPA. (2024, 5 febrero). US EPA. https://www.epa.gov/radiation/radionuclide-basics-cesium-137
          
  **2.**   Instrumentación, P. I. S. (2024, 27 abril). Contador Geiger | PCE Instruments. https://www.pce-instruments.com/espanol/instrumento-medida/medidor/contador-geiger-kat_163206.htm
                
  **3.**   colaboradores de Wikipedia. (2024, 8 abril). Distribución de poisson. Wikipedia, la Enciclopedia Libre. https://es.wikipedia.org/wiki/Distribuci%C3%B3n_de_Poisson

    """)
  st.divider()
