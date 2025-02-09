import streamlit as st
import plotly.io as pio
import pandas as pd
from .corr import Correlazione



def create_section(title, function, df=None, explanation=None):
    """Create a section with a plot and optional explanation."""
    col_left, col_center, col_right = st.columns([1, 4, 1])
    with col_center:
        st.markdown(f"### {title}")
        if callable(function):
            function()
        if explanation:
            st.markdown(explanation)
        st.markdown("<hr>", unsafe_allow_html=True)

def main():
    pio.templates.default = "plotly"    
    st.title('Digital Transformation Dashboard')
    DATASET_PATH = '../data/cleaned_data.xlsx'
    try:
        df = st.session_state.get('data', {}).get('survey')
    except AttributeError:
        df = pd.read_excel(DATASET_PATH)

    # Initialize function class
    corr = Correlazione(df)

    #####################################################################
       
    def display_metrics(df):
        """Display key metrics about the dataset."""
        def simplify_maturity(x):
            if pd.isna(x):
                return "Non specificato"
            elif "totalmente Digital Oriented" in x:
                return "Totalmente Digital"
            elif "relativamente digitale" in x:
                return "Relativamente Digital"
            elif "progetto pilota" in x:
                return "Fase Pilota"
            else:
                return "Nessuna Trasformazione"
        
        # Add simplified maturity column
        df['maturita_semplificata'] = df['maturita_digitale'].apply(simplify_maturity)
        
        # Display metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        with col3:
            st.metric("Numero totale aziende", len(df))
        with col4:
            df['soddisfazione'] = pd.to_numeric(df['soddisfazione'], errors='coerce')
            st.metric("Media soddisfazione", f"{df['soddisfazione'].mean():.2f}")
    create_section(     title='Correlazione tra la maturità digitale raggiunta dall\'azienda e l\'esperienza dell\'intervistato',
                        function= lambda: corr.heatmap_anni_maturita(),
                        explanation="""
                            - Aggiungo spiegazione
                        """
                        )
    create_section(     title='Correlazione tra il budget investito e il grado di soddisfazione del vertice aziendale',
                        function= lambda: corr.correlazione1_budget(),
                        explanation="""
                            - Aggiungo spiegazione
                        """
                        )
    create_section(     title='Correlazione tra il budget investito e le criticità riscontrate',
                        function= lambda: corr.plot_criticita_budget(),
                        explanation="""
                            - Aggiungo spiegazione
                        """
                        )
    create_section(     title='Correlazione tra il budget investito e l\'efficienza riscontrata',
                        function= lambda: corr.cor_budget_efficienza(),
                        explanation="""
                            - Aggiungo spiegazione
                        """
                        )
    display_metrics(df)
    #######################################################################

if __name__ == "__main__":
    main()