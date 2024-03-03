#Primero vamos a importar todos los paquetes necesarios
import streamlit as st
import pandas as pd
import plotly.express as px
from scipy.stats import binom
import pip
pip.main(["install", "openpyxl"])

#Ahora, haremos los ajustes necesarios para la pagina de streamlit
st.set_page_config(page_title="Pacrial 1", page_icon="🌍", layout="wide")
st.subheader("DISTRIBUCIÓN BINOMIAL DE UNA VARIABLE")

#Aquí no supe como hacerle para meter las probabilidades, entonces metí los diferentes valores de probabilidad a un excel e hice que python lo leyera
df=pd.read_excel("probabilidades.xlsx")

#En esta parte pondremos la parte concerniente a seleccionar los valores para la distribución binomimial
Elegir_probabilidad=st.sidebar.selectbox("Elegir probabilidad", df["Porcentaje"])

#Obtener el objeto seleccionado
inf_escen=df[df["Porcentaje"]==Elegir_probabilidad]
prob_exito=float(inf_escen['Probabilidad'])

#Hallar la probabilidad de la variable, cuadno la varible puede ser cualquiera
num_exitos=st.sidebar.number_input(f"Ingresar la probabilidad de encontrar", min_value=0, max_value=90)
num_intentos=st.sidebar.number_input(f"Ingresar el número de intentos", min_value=0, max_value=90)

#Aquí vamos a calcular la distribución binomial
x = list(range(num_intentos + 1))
probabilidad_pred = binom.pmf(num_exitos, num_intentos, prob_exito) if num_exitos is not None else None

#Ahora ploteamos la distribución binomial
fig = px.bar(x=x, y=probabilidad_pred, labels={'x': 'Número de exitos', 'y': 'Probabilidad'})
fig.update_layout(
    title=f'BINOMIAL DISTRIBUTION FOR {Elegir_probabilidad}',
    xaxis_title='Número de exitos',
    yaxis_title='Probabilidad',
    plot_bgcolor='rgba(0, 0, 0, 0)',  # Set plot background color to transparent
    paper_bgcolor='rgba(0, 0, 0, 0)',  # Set paper background color to transparent
    xaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Show x-axis grid and set its color
    yaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Show y-axis grid and set its color
    font=dict(color='#cecdcd'),  # Set text color to black
    showlegend=True)

#Con esto de aquí remarcamos el número de exitos que el usuario haya seleccionado
if num_exitos is not None:
    fig.add_vline(x=num_exitos,line_dash='dash', line_color='red',
                  annotation_text=f"Cantidad de eitos seleccionados: {num_exitos}", annotation_position="top right")
    
#En esta parte haremos que la probabilidad esperada se muestre en la página de streamlit
if probabilidad_pred is not None:
    st.success(f"**La probabilidad esperada de** {num_exitos} es : {probabilidad_pred:.4f}")

with st.expander("Data Source"):
    st.write('Student Exam Data:')
    st.dataframe(df,use_container_width=True)

with st.expander("Data Collection"):
    st.warning(f"**Probabilidad de exito en** {inf_escen}: {prob_exito}")
    st.info(f"**Número de intentos en** {inf_escen}: {num_intentos}")

st.plotly_chart(fig,use_container_width=True)