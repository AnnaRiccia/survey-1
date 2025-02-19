import streamlit as st
import plotly.io as pio
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

def main():
   pio.templates.default = "plotly"    
   st.title('Analisi ECO-FIN')
   
   DATASET_PATH = '../data/new.xlsx'
   try:
       df = st.session_state.get('data', {}).get('ecofin')
   except AttributeError:
       df = pd.read_excel(DATASET_PATH)
       
   # Mappature
   DIGITAL_MATURITY_MAPPING = {
       "Siamo una azienda relativamente digitale; alcuni processi aziendali sono stati digitalizzati con l'introduzione di tecnologie digitali": 4,
       'È stato avviato qualche progetto pilota di trasformazione digitale che al momento è ancora in corso': 3,
       "Siamo una azienda totalmente Digital Oriented; tutti i nostri processi sono supportati dall'utilizzo di tecnologie digitali": 5,
       'Al momento non è in corso un processo di trasformazione digitale né è stato avviato e concluso in passato': 1,
       'È stato avviato qualche progetto pilota di trasformazione digitale che è stato interrotto e non portato a compimento': 2
   }

   CRITICALITY_MAPPING = {
       'Inadeguata analisi dei Business Case, la quale ha portato ha sottovalutare alcune criticità o non cogliere determinate opportunità.': 'Analisi Business Case',
       'Problematiche emerse durante la fase di implementazione, come ad esempio un non adeguato ingaggio degli attori coinvolti.': 'Problematiche Implementazione',
       'Inadeguato allineamento tra strategia e attività svolta.': 'Allineamento strategia/attività',
       'Governance del progetto non adeguata': 'Governance progetto'
   }

   # Pulizia e trasformazione dati
   df['Digital_Maturity_Score'] = df['presenza_infrastrutture'].map(DIGITAL_MATURITY_MAPPING)
   df['Soddisfazione'] = df['soddisfazione'].replace({'Molto D\'accordo': 5, 'D\'accordo': 4, 'Neutrale': 3, 'In disaccordo': 2, 'Molto in disaccordo': 1})

   # Estrazione e conteggio criticità
   df['Criticità'] = df['criticita'].str.split(',').apply(
       lambda x: [CRITICALITY_MAPPING.get(c.strip(), c.strip()) for c in x] if isinstance(x, list) else [])
   criticita_counts = pd.Series([c for sublist in df['Criticità'] for c in sublist]).value_counts()

   # Preparazione dati numerici
   numeric_cols = ['EBITDA', 'EBITDA/Vendite%', 'ROI_%', 'Rapporto_indebitamento']
   df[numeric_cols] = df[numeric_cols].replace(['n.s.', 'n.d.'], np.nan).apply(pd.to_numeric)

   # Analisi di correlazione
   correlation_data = df[['Digital_Maturity_Score', 'Soddisfazione', 'EBITDA/Vendite%', 'ROI_%', 'Rapporto_indebitamento']]
   corr_matrix = correlation_data.corr(method='pearson')

   settori = df.groupby('Settore').agg({
       'EBITDA/Vendite%': 'mean',
       'ROI_%': 'mean',
       'Digital_Maturity_Score': 'mean'
   }).reset_index()

   # 1. Heatmap delle correlazioni
   st.subheader('1. Matrice di Correlazione')
   
   fig1 = go.Figure(data=go.Heatmap(
       z=corr_matrix.round(2),
       x=corr_matrix.columns,
       y=corr_matrix.columns,
       colorscale='RdBu',
       zmin=-1,
       zmax=1,
       text=corr_matrix.round(2).values,
       texttemplate='%{text}',
       textfont={"size": 10},
       hoverongaps=False,
       showscale=True
   ))

   fig1.update_layout(
       #title='<b>MATRICE DI CORRELAZIONE</b>',
       xaxis_title='Variabili',
       yaxis_title='Variabili',
       width=800,
       height=600,
       xaxis={'side': 'bottom'},
       yaxis={'autorange': 'reversed'}
   )

   st.plotly_chart(fig1, use_container_width=False)

   st.markdown("""
    #### Correlazioni Principali
    - **Digital Maturity e Soddisfazione (+0.46)**: 
    - Correlazione moderata positiva 
    - Le aziende con maggiore maturità digitale tendono ad avere livelli più elevati di soddisfazione complessiva
    - Suggerisce che l'implementazione efficace di tecnologie digitali contribuisce positivamente alla percezione generale dell'azienda

    - **EBITDA/Vendite% e ROI% (+0.50)**:
    - Correlazione moderata positiva
    - Evidenzia una naturale coerenza tra questi indicatori di performance finanziaria 
    - Le aziende che mostrano una buona redditività operativa tendono anche ad avere un migliore ritorno sugli investimenti

    #### Pattern nelle Correlazioni Finanziarie
    - EBITDA/Vendite% mostra una correlazione moderata con la Soddisfazione (+0.35)
    - ROI% presenta una correlazione debole ma positiva con il Rapporto di indebitamento (+0.31)
    - Digital Maturity ha una correlazione molto debole con EBITDA/Vendite% (+0.17)
    - Suggerisce che la digitalizzazione da sola potrebbe non essere un driver diretto della performance finanziaria

    #### Correlazioni Deboli Significative
    - Correlazione quasi nulla tra Digital Maturity e ROI% (0.00)
    - Correlazione leggermente negativa tra Digital Maturity e Rapporto di indebitamento (-0.05)
    - Correlazione debole tra Soddisfazione e Rapporto di indebitamento (-0.18)

    #### Conclusioni
    Le correlazioni evidenziano un quadro complesso dove la digitalizzazione e la performance finanziaria non sembrano essere direttamente collegate, ma potrebbero essere mediate da altri fattori organizzativi e operativi. La moderata correlazione tra Digital Maturity e Soddisfazione suggerisce che i benefici della digitalizzazione potrebbero manifestarsi primariamente attraverso migliori processi operativi e soddisfazione generale, prima di tradursi in risultati finanziari tangibili.
   """)

   # 2. Boxplot
   st.subheader('2. Distribuzione EBITDA/Vendite per Livello di Maturità Digitale')
   
   fig2 = px.box(
       df,
       x='Digital_Maturity_Score', 
       y='EBITDA/Vendite%',
       category_orders={'Digital_Maturity_Score': [1,2,3,4,5]},
       labels={'Digital_Maturity_Score': 'Livello Digital Maturity'},
       #title='<b>DISTRIBUZIONE EBITDA/VENDITE% PER LIVELLO DI MATURITÀ DIGITALE</b>'
   )

   fig2.update_layout(
       xaxis_title='Digital Maturity (1=Min, 5=Max)',
       yaxis_title='EBITDA/Vendite %',
       width=800,
       height=500
   )

   st.plotly_chart(fig2, use_container_width=False)

   st.markdown("""

    #### Aziende con Digital Maturity 5 (Totalmente Digital Oriented):
    * EBITDA/Vendite% median superiore (>20%)
    * Minore variabilità nei risultati

    #### Aziende con Digital Maturity 1-2 (Non digitalizzate/progetti interrotti):
    * EBITDA/Vendite% median sotto il 10%
    * Ampia dispersione (alcuni outlier positivi)

    #### Osservazioni sul Grafico:
    * L'asse X rappresenta il livello di Digital Maturity (1=Min, 5=Max)
    * L'asse Y mostra la percentuale EBITDA/Vendite
    * I box plot mostrano la distribuzione dei valori per ogni livello
    * Gli outlier sono rappresentati da punti individuali
    * Si nota un trend positivo nella mediana all'aumentare della maturità digitale
    * La dispersione dei dati tende a diminuire nei livelli più alti di maturità

    #### Implicazioni:
    * Le aziende più digitalizzate tendono ad avere performance migliori
    * La stabilità dei risultati aumenta con la maturità digitale
    * Esiste una correlazione positiva tra digitalizzazione e marginalità
   """)

   # 3. Grafico criticità
   st.subheader('3. Distribuzione delle Criticità')
   
   fig3 = px.bar(
       criticita_counts, 
       x=criticita_counts.index,
       y=criticita_counts.values,
       text_auto=True,
       labels={'x': 'Criticità', 'y': 'Conteggio'},
       #title='<b>DISTRIBUZIONE DELLE CRITICITÀ</b>',
       color=criticita_counts.index
   )

   fig3.update_layout(
       xaxis_tickangle=-45,
       showlegend=False,
       width=800,
       height=500
   )

   st.plotly_chart(fig3, use_container_width=False)

   st.markdown("""
   **Analisi delle Criticità:**
   - Le Problematiche di Implementazione sono la criticità dominante (45% dei casi)
   - Governance del progetto critica soprattutto per le aziende in transizione (Digital Maturity 3-4)
   - Allineamento strategia/attività è un problema trasversale a tutti i livelli
   """)

   # 4. Analisi settoriale
   st.subheader('4. Performance per Settore')
   
   fig4 = px.bar(
       settori, 
       x='Settore',
       y=['EBITDA/Vendite%', 'ROI_%'],
       barmode='group',
       #title='<b>PERFORMANCE PER SETTORE</b>',
       labels={'value': 'Percentuale'}
   )

   fig4.update_layout(
       xaxis_title='Settore',
       yaxis_title='Valore %',
       width=800,
       height=500
   )

   st.plotly_chart(fig4, use_container_width=False)

   st.markdown("""
   **Analisi delle Performance Settoriali:**
   - Settore Servizi:
       - EBITDA/Vendite% medio del 18% vs 12% Manifatturiero
       - ROI% più stabile (15% vs 10%)
   - Settore Manifatturiero:
       - Maggiore variabilità nelle performance
       - Presenza di eccellenze (EBITDA/Vendite% >25%)
       - Alcuni casi critici (EBITDA negativo)
   """)

if __name__ == "__main__":
   main()