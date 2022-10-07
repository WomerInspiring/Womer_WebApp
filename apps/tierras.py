import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pandas.api.types import CategoricalDtype


# Data upload
# enter to project / details / API / endpoints
url_info= "https://five.epicollect.net/api/export/entries/mujeres-y-tierras?form_ref=53c94816cee44815a184eeb52f374d87_63025ec233674&format=csv&per_page=1000&page=1"

data = pd.read_csv(url_info)

dict = {'4_Este_hogar_ha_trab':  "trabajo_agricola",
        '5_La_actividad_agrco': "agricola_actividad", 
        '6_Este_hogar_ha_cria': "cria_animales", 
        '7_La_cra_o_el_cuidad': "cria_actividad", 
        '8_Este_hogar_ha_cria': "cria_peces", 
        '9_Realiz_la_pesca_pa' : 'pesca_actividad',
        '10_Cuntos_adultos_vi': "total_adultos", 
        '11_Es_propietaria_ut': "mujer_propietaria", 
        '12_Existe_algn_docum': "doc_propiedad",
        '13_Cal_es_el_otro_do' : "otro_doc", 
        '14_La_persona_duea_d': "hogar_propietario", 
        '15_La_persona_propie': "otra_propietaria",
        '16_La_persona_propie': "otra_vender", 
        '17_La_persona_propie': "otra_trasmitir", 
        '18_Tiene_derecho_a_v': "derecho_vender",
        '19_Tiene_derecho_a_t': "derecho_trasmitir", 
        '20_Cul_es_su_estado_': "estado_civil", 
        '21_En_caso_de_separa': "derecho_por_separacion",
        '22_Cul_es_la_razn_po': "razon", 
        '23_Despues_de_la_sep': "recibio_tierra", 
        '24_Cul_es_la_razn_po': "razon_no_recibirtierra",
        '25_Este_hogar_tiene_': "hogar_con_bosques", 
        '26_Es_usted_propieta': "propietaria_bosques", 
        '27_Usted_puede_acced': "acceso_bosques",
        '28_Cul_es_la_razn_po': "razon_no_bosques", 
        '29_Participa_en_espa': "participacion_manejo_rn", 
        '30__Cul_es_su_papel_': "role_participacion",
        '31_Eres_parte_de_la_': "participacion_turismo", 
        '32_Tienes_un_telfono': "tel_mobil", 
        '33__Tienes_servicio_':"internet",
        '34_Tienes_acceso_a_c': "free_internet", 
        '35_Ha_recibido_educa': "educacion_igualdad"
        }

# call rename () method
data.rename(columns=dict,
          inplace=True)

df = data.copy(deep=True)


def app():
    """
    Main app that streamlit will render.
    """
    st.title("⚫ Indicadores de derecho a tierras")
    st.markdown ('---')
    st.write("El indicador 5.a.1 se centra en las tierras agrícolas, ya que constituyen un insumo fundamental en países de ingresos bajos y medianos en los que, con frecuencia, las estrategias de reducción de la pobreza y desarrollose basan en el sector agrícola")
 
   
    # DEFINE FUNTIONS

    # df in percentage
    def percentage(column):
        df = (column.value_counts()/column.count())*100
        df = (df.to_frame().reset_index())
        df = df.round(decimals = 1)
        return df

    # Titles charts
    def format_title(title, subtitle=None, subtitle_font_size=16):
        title = f'<b>{title}</b>'
        if not subtitle:
            return title
        subtitle = f'<span style="font-size: {subtitle_font_size}px;">{subtitle}</span>'
        return f'{title}<br>{subtitle}'   

    # creation of columns
    def hogar_agricola(df):    
        if (df['trabajo_agricola'] == 'No se trabaja ninguna de las anteriores')  or (df['agricola_actividad'] == 'Trabajo asalariado para otros')  or (df['cria_actividad'] == 'Trabajo asalariado para otros'):
            return 'No'
        else:
            return "Si"

    def hogar_propio(df):    
        if (df['mujer_propietaria'] ==  '"No soy propietaria, No uso, No ocupo alguna de las anteriores tierras agrícolas"') and (df['hogar_propietario'] == "No"):
            return 'No'
        elif (df['mujer_propietaria'] ==  '"No soy propietaria, uso u ocupo alguna de las anteriores tierras agrícolas"') and (df['hogar_propietario'] == "Si"):
            return "Si"
        elif (df['mujer_propietaria'] !=  '"No soy propietaria, uso u ocupo alguna de las anteriores tierras agrícolas"'):
            return "Si"

    def mujer_propietaria(df):    
        if (df['hogar_propio'] ==  'Si') and (df['otra_propietaria'] == "Hombre mayor de 18 años"):
            return 'Hombre'
        elif (df['hogar_propio'] ==  'Si') and (df['otra_propietaria'] != "Hombre mayor de 18 años"):
            return 'Mujer'
        elif (df['hogar_propio'] ==  'Si') and (df['mujer_propietaria'] == '"No soy propietaria, No uso, No ocupo alguna de las anteriores tierras agrícolas"'):
            return 'Mujer' 
        else:
            return "Hombre"

    def document(s):
        if (s == "No existe ningún documento") or (s== "No lo sabe ") or (s== 0): 
            return "No"
        else:
            return "Si"


    df['hogar_agricola'] = df.apply(hogar_agricola, axis=1)
    df['hogar_propio'] = df.apply(hogar_propio, axis=1)
    df["total_mujeres"] = df.apply(mujer_propietaria, axis=1)
    df["doc_propiedad"] = df["doc_propiedad"].fillna(0)
    df["document"] = df["doc_propiedad"].apply(document)

    # df hogares agricolas
    hogares_agricolas = df.loc[df['hogar_agricola'] == "Si"]

    #Column personas con derecho_tierra
    def people_land_right(df):    
        if (df['hogar_agricola'] ==  'Si') and (df['hogar_propio'] ==  'Si')  and ((df['document'] == 'Si') or (df['otra_vender'] == "Si") or (df['otra_trasmitir'] == "Si") or (df["derecho_vender"] == "Si") or (df["derecho_trasmitir"] == "Si")):
            return 'Si'
        else:
            return "No"

    # column mujeres  con derecho_tierra
    def mujeres_land_right(df):    
        if (df['people_land_right'] ==  'Si')  and (df['total_mujeres'] == 'Mujer'):
            return 'Mujer'
        else:
            return "Hombre"

    df["people_land_right"] = df.apply(people_land_right, axis=1)
    df["mujeres_land_right"] = df.apply(mujeres_land_right, axis=1)

    new_df = df[['hogar_agricola',  
            'hogar_propio',
            'mujer_propietaria',
            'otra_propietaria',
            'total_mujeres', 
            'doc_propiedad',
            'document',
            'hogar_propietario',
            'otra_vender',
            'otra_trasmitir', 
            'derecho_vender',
            'derecho_trasmitir',"people_land_right", "mujeres_land_right"]].copy()

    indicator = st.selectbox("SELECCIONE UN INDICADOR",
        ("Total hogares agricolas",
         'Indicador 5.a.1(a). Porcentaje de personas con propiedad o derechos seguros sobre tierras agrícolas',
         'Indicador 5.a.1.(b). Proporción de mujeres entre los propietarios o titulares de derechos de tierras agrícolas',
         
        ))    


    

    #STATE AN ERROR AND DON'T SHOW THE KEYERROR 
    if not indicator :
        st.error(" ⚠️ Por favor seleccione un indicador")
        st.stop()

        # Interactive visualization 
    if indicator == "Total hogares agricolas": 
            
        # hogares agricolas
        total_hogaresAgric =  percentage(new_df.hogar_agricola)

        fig_pie = px.pie(total_hogaresAgric, values='hogar_agricola', names='index', color='index',
                                color_discrete_map={'No':'lightslategray',  'Si':'#97F08A'},
                                                    width = 500, height = 300)
        fig_pie.update_layout(title = format_title("% de Hogares agrícolas",
                                            " "),
                        title_font_size = 20)
        #fig_pie.update_layout(title="Porcentaje de Hogares usando lengua indígena", title_font_size = 20)
        fig_pie.update_traces(textposition='inside', textfont_size=20)
        fig_pie.update_layout(margin={"r":80,"t":110,"l":0,"b":0})
        st.plotly_chart(fig_pie, unsafe_allow_html=True)
















    with st.expander("ℹ️ Indicador 5.a.1 INFO"):
        st.markdown(""" El 5.a.1 solo se refiere a: 
            
        🟢 La población adulta agrícola como todos los adultos que viven en hogares agrícolas.
            • Hogares que hayan trabajado la tierra con fines agrícolas 
            • Hogares que hayan criado o cuidado ganado en los últimos 12 meses, con independencia del destino final de la producción. 
            • Cabe señalar que quedarán excluidos de la población de referencia los hogares cuyos miembros participen en la agricultura solo como asalariados.
            
        🟢 El indicador 5.a.1 se basa en tres medidas indirectas para determinar los derechos de tenencia:
            • la posesión de un documento reconocido legalmente a nombre de la persona;
            • el derecho de la persona a vender la tierra;
            • el derecho de la persona de transmitir por herencia la tierra.

        🟢La presencia de una de las tres medidas indirectas es suficiente para definir a una persona como propietaria o titular de facto de derechos de tenencia de tierras agrícolas. La ventaja de este sistema es su aplicabilidad en países con distinto grado de difusión de documentos jurídicamente vinculantes.
            
            More info in: (https://www.fao.org/3/ca4885es/CA4885ES.pdf)""")

                          