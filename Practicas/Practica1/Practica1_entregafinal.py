import pandas as pd
import numpy as np
import streamlit as st
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
from scipy.stats import binom
from scipy.optimize import curve_fit
from scipy import stats
import plotly.express as px
from scipy import optimize as sco
import math




#Nombre e ícono de la pestaña
st.set_page_config(page_title="Practica 1: Distribución Binomial", page_icon="🌍", layout="wide")


#Aquí ponemos los ajustes de la barra lateral
with st.sidebar:
    selected=option_menu(
        menu_title="Menú",
        options = ["Principal", "Teoria"],
        icons = ["house-heart-fill", "envelope-heart-fill"],
        menu_icon = "heart-eyes-fill",
        default_index = 0,
    )

#Aquí está toda la información de la página principal
if selected == "Principal":
    def binomial_distribution(x, n, p):
        return binom.pmf(x, n, p)
    st.markdown("<h1 style='text-align: center; color: #A2BDF1;'>Distribución Binomial: Lanzamiento de monedas</h1>", unsafe_allow_html=True)
    st.markdown("""Esta primera gráfica, muestra los resultados obtenidos en 100 lanzamientos hechos por Dessiré y Fabricio. En la inferior de la gráfica se muestra el promedio, desviación estandar  los valores para n y p que se obtuvieron al realizar el ajuste de la gráfica. Si desea obtener más información acerca de lo que se realizó o los conceptos matemáticos utilizados, puede dirigirse a la pestaña de Teoria.""")
    data = pd.read_csv('https://raw.githubusercontent.com/Fabricio-mencos/LabRedDat/main/Practicas/Practica1/Copia%20de%20ConteosDeCarasPorPareja%20-%20Sheet1%20(1).csv')
    
    #cantidad de tiros
    m = st.slider('Seleccione la cantidad de tiros (m)', 0, 100, value=100)
    m_t = data.head(m)

    def binom(x,n,p):
    # print('binom(',x,n,p,')')
    
        x = int(x)
        n = int(n)
        
        comb = math.comb(n,x)
        p_x = p**x
        q_nx = (1-p)**(n-x)

        return comb*p_x*q_nx
    

    binom = np.vectorize(binom)

    print(f'data:\n{data}')

    data = data.loc[:m]

    counts_non_sort = data['DF'].value_counts()
    counts = pd.DataFrame(np.zeros(11))
#En toda esta parte hacemos el fit para el histograma

    for row, value in counts_non_sort.items():
        counts.loc[row,0] = value

    print(f'counts:\n{counts}')
    print(f'index: {counts.index.values}')
    print(f'normalized counts: {list(counts[0]/m)}')


    fit, cov_mat = sco.curve_fit(binom,counts.index.values,counts[0]/m,[10,0.5],bounds=[(0,0),(np.inf,1)])

    print(f'Fit:\n{fit}\ncov_mat\n{cov_mat}')

    n = fit[0]
    p = fit[1]

    print(f'Este es el valor de n: {n}\nEste es el valor de p: {p}')




    binomial_plot = px.line(x=counts.index.values, y=binom(counts.index.values,n,p), title="Lanzamiento de fichas")

    binomial_plot.add_bar(x=counts.index.values, y=counts[0]/m, name='Lanzamientos experimentales')

    binomial_plot.show()


    #Aquí calculamos el promedio de los datos y su desviación estandar
    pro = np.mean(m_t)
    desv_estd = np.std(m_t, ddof=1)
    
   # Crear histograma
    fig, ax = plt.subplots(figsize=(3, 3))
    hist, bins, _ = ax.hist(m_t['DF'], bins=np.arange(min(m_t['DF']), max(m_t['DF']) + 1.5) - 0.5, alpha=0.7, label='Datos', color='blue', density=True)
    
    # Configuración de la gráfica
    ax.set_xlabel('Número de éxitos')
    ax.set_ylabel('Densidad de probabilidad')
    ax.set_title('Histograma y distribución binomial')
    ax.legend()
    


    #Mostramos el promedio y la desviación estandar calculados
    st.pyplot(fig)
    if pro is not None:
        st.success(f"**El promedio de los datos ingresados es: {pro}**")
    if desv_estd is not None:
        st.success(f"**La desviación estandar para los datos ingresados es: {desv_estd}**")
    if n is not None:
        st.success(f"**El valor calculado de n es: {n}**")
    if p is not None:
        st.success(f"**El valor calculado para p es: {p}**")
    st.divider()
    with st.expander("Click para ver la tabla de datos"):
        st.table(m_t)
    st.divider()
    #--------------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------------

    st.markdown("<h1 style='text-align: center; color: #A2BDF1;'>Lanzamiento de monedas: Todos los grupos</h1>", unsafe_allow_html=True)
    st.markdown("""Esta segunda gráfica muestra los datos recopilados por toda la clase. Además de mostrar los datos obtenidos al realizar el ajuste a la gráfica.""")
    datos = pd.read_csv("https://raw.githubusercontent.com/Fabricio-mencos/LabRedDat/main/Practicas/Practica1/Conteostotales%20-%20Sheet1.csv")

    print(f'data:\n{datos}')
    k = 500

    data = data.loc[:m]

    counts_non_sort = datos['Datos'].value_counts()
    counts = pd.DataFrame(np.zeros(11))
# print(counts)

    for row, value in counts_non_sort.items():
        counts.loc[row,0] = value

    print(f'counts:\n{counts}')
    print(f'index: {counts.index.values}')
    print(f'normalized counts: {list(counts[0]/k)}')


    fit_1, cov_mat_1 = sco.curve_fit(binom,counts.index.values,counts[0]/k,[10,0.5],bounds=[(0,0),(np.inf,1)])

    print(f'Fit:\n{fit_1}\ncov_mat\n{cov_mat_1}')

    n_1 = fit_1[0]
    p_1 = fit_1[1]

    print(f'Este es el valor de n: {n_1}\nEste es el valor de p: {p_1}')




    binomial_plot_1 = px.line(x=counts.index.values, y=binom(counts.index.values,n,p), title="Lanzamiento de fichas")

    binomial_plot_1.add_bar(x=counts.index.values, y=counts[0]/k, name='Lanzamientos experimentales')
    

    #Aquí calculamos el promedio de los datos y su desviación estandar
    prom = np.mean(datos)
    desv_estdar = np.std(datos, ddof=1)
    
   # Crear histograma
    figur, ax = plt.subplots(figsize=(3, 3))
    hist, bins, _ = ax.hist(datos['Datos'], bins=np.arange(min(datos['Datos']), max(datos['Datos']) + 1.5) - 0.5, alpha=0.7, label='Datos', color='blue', density=True)
    
    # Configuración de la gráfica
    ax.set_xlabel('Número de éxitos')
    ax.set_ylabel('Densidad de probabilidad')
    ax.set_title('Histograma y distribución binomial')
    ax.legend()

    #Mostramos el promedio y la desviación estandar calculados
    st.pyplot(figur)
    if prom is not None:
        st.success(f"**El promedio de los datos ingresados es: {prom}**")
    if desv_estdar is not None:
        st.success(f"**La desviación estandar para los datos ingresados es: {desv_estdar}**")
    if n_1 is not None:
        st.success(f"**El valor calculado de n es: {n_1}**")
    if p_1 is not None:
        st.success(f"**El valor calculado para p es: {p_1}**")
    st.divider()
    with st.expander("Click para ver la tabla de datos"):
        st.table(datos)




if selected == "Teoria":
    #Los tipos de cuadros, morado palido y azul pálido
    estilo_cuadro = """
    <style>
    .cuadro-morado {
        padding: 20px;
        background-color: #F4E8FF; 
        border-radius: 10px;
    }
    </style>
    """

    estilo_cuadro_azul = """
    <style>
    .cuadro-azul {
        padding: 20px;
        background-color: #D4EEF0; 
        border-radius: 10px;
    }
    </style>
    """
    #se agregan a streamlit
    st.markdown(estilo_cuadro, unsafe_allow_html=True)
    st.markdown(estilo_cuadro_azul, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center; color: #A2BDF1;'>Resumen</h1>", unsafe_allow_html=True)
    st.markdown("""
    <div class= "cuadro-azul">
        <p>Existen diferentes métodos para conocer la probabilidad de obtener un caso especifico. La distribución binomial es uno de ellos, las condiciones de uso son: conocer el número de lanzamientos que se quiere, en este caso con monedas; conocer la probabilidad de obtener lo esperado y saber el número de monedas a lanzar. Durante la realización de esta práctica su uso nos ayudará a predecir, conocer y calcular la probabilidad de obtener cierto lado de varias monedas en ciertos tiros y esto lo modelaremos usando herramientas como Python y Streamlit.</p>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    st.markdown("<h2 style='text-align: left; color: #D3BEF1;'>Objetivos</h1>", unsafe_allow_html=True)
    st.markdown("""
    <div class="cuadro-morado">
        <p>▶ Obtener de forma experimental la cantidad de caras al lanzar diez monedas del mismo valor. </p>
        <p>▶ Realizar un histograma con los datos obtenidos usando Python y mostrarlos en una app de Streamlit.</p>
        <p>▶ Ajustar los valores obtenidos en el histograma y mostrarlos en la app.</p>
    </div>
    """, unsafe_allow_html=True)
    st.divider()
    
    st.markdown("<h1 style='text-align: center; color: #A2BDF1;'>Teoría de la Distribución Binomial</h1>", unsafe_allow_html=True)

    st.markdown("""
    <div class= "cuadro-azul">
        <p>La distribución binomial es un modelo probabilístico discreto que describe el número de éxitos en una serie de ensayos secuenciales independientes, donde cada uno tiene siempre la misma probabilidad de éxito. Este modelo es utilizado con mucha frecuencia en experimentos donde se obtengan resultados binarios, es decir, si el resultado se puede categorizar como Éxito o Fracaso.</p>
        <p>Para definir a la distribución binomial, se requieren dos parámetros. El primero de ellos es el <strong>número total de intentos (n)</strong> y la <strong>probabilidad de éxito de cada ensayo (p)</strong>. Agregado a esto, regularmente se utiliza el símbolo X para denotar una variable que cuenta el número de éxitos en n cantidad de ensayos.</p>
        <p>La fórmula para calcular la probabilidad de exactamente k éxitos en n ensayos, con una probabilidad de éxito p, es:</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.latex(r''' P(x = k) = \binom{n}{k} p^{k} (1-p)^{n-k} ''')
    st.markdown("""
    <div class= "cuadro-azul">
        <p>Donde:</p>
        <ul>
            <li>(n k) es el coeficiente binomial.</li>
            <li>p es la probabilidad de éxito en un solo ensayo.</li>
            <li>(1 - p) es la probabilidad de fracaso en un solo ensayo.</li>
            <li>k es el número de éxitos en n ensayos.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    st.markdown("<h2 style='text-align: left; color: #D3BEF1;'>Acerca de esta practica</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="cuadro-morado">
        <p>En esta práctica, cada pareja lanzó un grupo de 10 monedas un total de 100 veces para poder observar la tendencia de las monedas a caer en el lado de la cara. Tras recopilar todos los datos, estos fueron ingresados en un archivo CSV para su análisis posterior. Lo primero que se realizó fue un histograma que muestra la forma en que se distribuyó una cierta cantidad m de tiros de las monedas, donde la m puede ser elegida por el usuario. Añadido a lo anterior, se realizó un ajuste a los datos que se muestran en el histograma. Dicho ajuste fue hecho a partir de una función binomial. Por último, se muestran los valores obtenidos a partir del ajuste, los valores obtenidos en los conteos de monedas y la desviación estándar de todos estos datos.</p>
        <p>En el caso donde se utilizaron los datos de toda la clase, se realizó un proceso muy similar al caso anterior, con la diferencia de que en este histograma no se puede variar la m, por lo cual se muestra la información de todos los datos obtenidos. De igual manera, se presenta el ajuste binomial, los valores del ajuste, los valores de conteo medio de caras y su desviación estándar.</p>
    </div>
    """, unsafe_allow_html=True)
    st.divider()
    st.markdown("<h2 style='text-align: left; color: #A2BDF1;'>Análisis de Resultados</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class= "cuadro-azul">
        <p>▶ Al variar el número de veces que se lanzan las monedas la gráfica de barras cambia, notamos que mientras mayor es este número más se parece a lo teóricamente esperado.</p>
        <p>▶ Se utilizaron monedas de diez centavos, sin embargo un lado de la moneda no es simétrico respecto al otro, lo cual podría alterar nuestra toma de datos.</p>
    </div>
    """, unsafe_allow_html=True) 
    st.divider()
    st.markdown("<h2 style='text-align: left; color: #D3BEF1;'>Conclusiones</h1>", unsafe_allow_html=True)

    st.markdown("""
    <div class="cuadro-morado">
        <p>▶ En nuestra gráfica podemos observar que el valor que más se repite es el cinco, este es el valor promedio de los datos tomados. Lo que concuerda con la teoría, ya que es el caso más probable.</p>
        <p>▶ Nuestros datos han sido aterados de forma mínima por las condiciones en la toma de datos (el peso de las monedas, el suelo, aire, entre otros.), esto se ve reflejado en la comparación de estos datos con los valores teóricos esperados. Los valores experimentales son similares a los valores teóricos, podemos decir entonces que no se cometieron errores significativos en la toma de datos.</p>
    </div>
    """, unsafe_allow_html=True)
    st.divider()
    st.markdown("<h3 style='text-align: left; color: black;'>Referencias</h1>", unsafe_allow_html=True)
    st.markdown("""  
    **1.** Johnson, N.L., Kotz, S., & Kemp, A.W. (1992). "Univariate Discrete Distributions". John Wiley and Sons.  
                  
    **2.** Devore, J.L. (2011). "Probability and Statistics for Engineering and the Sciences". Cengage Learning.  
                
    **3.** Wackerly, D., Mendenhall III, W., & Scheaffer, R.L. (2008). "Mathematical Statistics with Applications". Cengage Learning.  
    """)
    st.divider()


