import pandas as pd
import numpy as np
import streamlit as st
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
from scipy.stats import binom
from scipy.optimize import curve_fit



#Nombre e ícono de la pestaña
st.set_page_config(page_title="Practica 1: Distribución Binomial", page_icon="🌍", layout="wide")
with st.sidebar:
    selected=option_menu(
        menu_title="Menú",
        options = ["Principal", "Teoria"],
        icons = ["house-heart-fill", "envelope-heart-fill"],
        menu_icon = "heart-eyes-fill",
        default_index = 0,
    )

if selected == "Principal":
    def binomial_distribution(x, n, p):
        return binom.pmf(x, n, p)
    st.markdown("<h1 style='text-align: center; color: #A2BDF1;'>Distribución Binomial: Lanzamiento de monedas</h1>", unsafe_allow_html=True)
    data = pd.read_csv('https://raw.githubusercontent.com/Fabricio-mencos/LabRedDat/main/Practicas/Practica1/Copia%20de%20ConteosDeCarasPorPareja%20-%20Sheet1%20(1).csv')
    
    #cantidad de tiros
    m = st.slider('Seleccione la cantidad de tiros (m)', 0, 100, value=100)
    m_t = data.head(m)

    #Aquí calculamos el promedio de los datos y su desviación estandar
    pro = np.mean(m_t)
    desv_estd = np.std(m_t, ddof=1)
    
    # Crear histograma
    fig, ax = plt.subplots(figsize=(10, 6))
    hist, bins, _ = ax.hist(m_t['DF'], bins=np.arange(min(m_t['DF']), max(m_t['DF']) + 1.5) - 0.5, alpha=0.7, label='Datos', color='blue', density=True)
    
    # Ajuste de la distribución binomial a los datos
    x_values = np.linspace(0, max(m_t['DF']), len(hist))
    params, _ = curve_fit(binomial_distribution, x_values, hist)
    
    # Trazar la distribución binomial ajustada
    ax.plot(x_values, binomial_distribution(x_values, *params), marker='o', linestyle='-', color='orange', label='Distribución Binomial')
    
    # Configuración de la gráfica
    ax.set_xlabel('Número de éxitos')
    ax.set_ylabel('Densidad de probabilidad')
    ax.set_title('Histograma y distribución binomial')
    ax.legend()
    
    # Mostrar la gráfica en Streamlit
    st.pyplot(fig)

    #Mostramos el promedio y la desviación estandar calculados
    if pro is not None:
        st.success(f"**El promedio de los datos ingresados es: {pro}**")
    if desv_estd is not None:
        st.success(f"**La desviación estandar para los datos ingresados es: {desv_estd}**")
    st.divider()
    with st.expander("Click para ver la tabla de datos"):
        st.table(m_t)
    


if selected == "Teoria":
    st.markdown("<h1 style='text-align: center; color: #A2BDF1;'>Teoria de la Distribución Binomial</h1>", unsafe_allow_html=True)  

    st.markdown("""La distribución binomial es modelo probabilistico discreto. Este describe el número de éxitos en una serie de ensayos secuenciales independientes, donde cada uno tiene siempre la misma probabilidad de exito. Este modelo es utilizado con mucha frecuencia en experimentos donde se obtengan resultados binarios, es decir, si el resultado se puede categorizar como Éxito o Fracaso.""")
    st.markdown("""Para definir a la distribución binomial, se requieren dos parametros. El primero de ellos es el **número total de intentos (n)** y la **probabilidad de exito de cada ensayo (p)**. Agregado a esto, regularmente se utiliza el simbolo X para denotar una variable que cuenta el número de éxitos en n cantidad de ensayos. """)
    st.markdown("""La fórmula para calcular la probabilidad de exactamente k éxitos en n ensayos, con una probabilidad de éxito p, es:""")

    st.latex(r''' P(x = k) = \binom{n}{k} p^{k} (1-p)^{n-k} ''')

    st.markdown("""Donde:  
    ▶ (n k) es el coeficiente binomial.  
    ▶ p es la probabilidad de éxito en un solo ensayo.  
    ▶ (1 - p) es la probabilidad de fracaso en un solo ensayo.  
    ▶ k es el número de exitos en n ensayos.
    """)
    st.divider()
    st.markdown("<h2 style='text-align: left; color: #D3BEF1;'>Acerca de esta practica</h1>", unsafe_allow_html=True)  
    st.markdown("""En esta practica, cada pareja, lanzó un grupo de 10 monedas un total de 100 veces para poder observar la tendencia de las monedas a caer en el lado de la cara. Tras recopilar todos los datos, estos fueron ingresados en un archivo csv para su analisis posterior. Lo primero que se realizó fue un histograma que muestra la fomra en que se distribuyó una cierta cantidad m de tiros de las monedas, donde la m puede ser elegida por el usuario. Añadido a lo anterior, se realizó un ajuste a los datos que se muestran en el histograma. Dicho ajuste fue hecho a paritr de un función binomial. Por último, se muestran los valores obtenidos a partir del ajuste, los valores obtenidos en los conteos de monedas y la desviación estandar de todos estos datos. """)  
    st.markdown("""En el caso donde se utilizaron los datos de toda la clase, se realizó un proceso muy similar al caso anterior, con la diferencia que en este histograma no se puede varias la m, por lo cual se muestra la información de todos los datos obtenidos. De igual manera se presenta el ajuste binomial, los valores del ajuste, los valores de ocnteo medio de caras y su desviación estandar. """)
    st.divider()
    st.markdown("<h2 style='text-align: left; color: #A2BDF1;'>Análisis de Resultados</h1>", unsafe_allow_html=True)  
    st.divider()
    st.markdown("<h2 style='text-align: left; color: #D3BEF1;'>Conclusiones</h1>", unsafe_allow_html=True)  
    st.divider()
    st.markdown("<h3 style='text-align: left; color: black;'>Referencias</h1>", unsafe_allow_html=True)
    st.markdown("""  
    **1.** Johnson, N.L., Kotz, S., & Kemp, A.W. (1992). "Univariate Discrete Distributions". John Wiley and Sons.  
                  
    **2.** Devore, J.L. (2011). "Probability and Statistics for Engineering and the Sciences". Cengage Learning.  
                
    **3.** Wackerly, D., Mendenhall III, W., & Scheaffer, R.L. (2008). "Mathematical Statistics with Applications". Cengage Learning.  
    """)
    st.divider()
