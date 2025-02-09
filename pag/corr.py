import streamlit as st
import pandas as pd
import plotly.express as px

class Correlazione:
    """
    A class for analyzing and visualizing digital transformation data.
    
    This class provides methods for data cleaning, transformation, and visualization
    of various aspects of digital transformation in companies, including budget
    allocation, digital maturity, and efficiency impacts.
    """
    
    # Constants for visualization
    PLOT_WIDTH = 1500
    PLOT_HEIGHT = 800
    FONT_FAMILY = 'Arial'
    
    # Color scales
    RED_COLOR_SCALE = ['#FAD0D0', '#F8A0A0', '#F57272', '#F44D4D', '#D32F2F']
    BLUE_COLOR_SCALE = ['#E4F1F9', '#C0D9E2', '#9ACBCF', '#6DB8C0', '#3C9D9A']
    GREEN_COLOR_SCALE = ["#E4F1E1", "#C0E0C6", "#9ACFA8", "#6DBE8D", "#3C9D74"]
    
    # Mapping dictionaries
    DIGITAL_MATURITY_MAPPING = {
                                'Siamo una azienda relativamente digitale; alcuni processi aziendali sono stati digitalizzati con l\'introduzione di tecnologie digitali': 'Relativamente digitale',
                'È stato avviato qualche progetto pilota di trasformazione digitale che al momento è ancora in corso': 'Qualche progetto avviato',
                'Siamo una azienda totalmente Digital Oriented; tutti i nostri processi sono supportati dall\'utilizzo di tecnologie digitali': 'Totalmente Digital Oriented',
                'Al momento non è in corso un processo di trasformazione digitale né è stato avviato e concluso in passato': 'Non digitalizzato',
                'È stato avviato qualche progetto pilota di trasformazione digitale che è stato interrotto e non portato a compimento': 'Qualche progetto interrotto'
            }
    
    SATISFACTION_MAPPING = {
                            5: "Molto soddisfatto",
                            4: "Soddisfatto",
                            3: "Neutro",
                            2: "Insoddisfatto",
                            1: "Per niente soddisfatto"
                            }
    
    CRITICALITY_MAPPING = {
                            'Inadeguata analisi dei Business Case, la quale ha portato ha sottovalutare alcune criticità o non cogliere determinate opportunità.': 'Analisi dei Business Case',
                            'Problematiche emerse durante la fase di implementazione, come ad esempio un non adeguato ingaggio degli attori coinvolti.': 'Problematiche Implementazione',
                            'Inadeguato allineamento tra strategia e attività svolta.': 'Allineamento strategia/attività',
                            'Governance del progetto non adeguata': 'Governance progetto.'
                            }

    def __init__(self, df=None):
        """
        Initialize the Correlazione class with an optional DataFrame.
        """
        self.df = df

    def _create_base_plotly_layout(self, title_text='', x_title='', y_title='', width=None, height=None):
        """
        Creates a base layout for Plotly figures with consistent styling.
        """
        return dict(
                    xaxis=dict(
                        title=dict(text=x_title, font=dict(size=16, family=self.FONT_FAMILY, weight='bold')),
                        tickfont=dict(size=14, family=self.FONT_FAMILY, weight='bold'),
                    ),
                    yaxis=dict(
                        title=dict(text=y_title, font=dict(size=16, family=self.FONT_FAMILY, weight='bold')),
                        tickfont=dict(size=14, family=self.FONT_FAMILY, weight='bold')
                    ),
                    title={'text': title_text, 'x': 0.5},
                    template='plotly_white',
                    font=dict(size=14),
                    width=width or self.PLOT_WIDTH,
                    height=height or self.PLOT_HEIGHT
                    )

    def semplifica_budget(self, df=None):
        """
        Simplifies budget values in the DataFrame.
        """
        df = df if df is not None else self.df
        df['budget_trans'] = df['budget_trans'].apply(lambda x: "Non specificato" if pd.isna(x) or x == 'Non so' else x)
        return df

    def mappa_maturita(self, df=None):
        """
        Maps digital maturity values to simplified categories.
        """
        df = df if df is not None else self.df
        df['maturita_digitale'] = df['maturita_digitale'].replace(self.DIGITAL_MATURITY_MAPPING)
        df['maturita_digitale'].fillna('Nessuna risposta', inplace=True)
        return df

    def categorizza_anni(self, df=None):
        """
        Categorizes years of activity into predefined ranges.
        """
        df = df if df is not None else self.df

        def categoria(anni):
            if pd.isna(anni):
                return 'Non specificato'
            try:
                anni = int(anni)
                if anni <= 5:
                    return '0-5 anni'
                elif anni <= 10:
                    return '6-10 anni'
                elif anni <= 15:
                    return '11-15 anni'
                elif anni <= 20:
                    return '16-20 anni'
                else:
                    return 'Oltre 20 anni'
            except ValueError:
                return 'Non specificato'

        df['anni_attivita_categoria'] = df['Anni'].apply(categoria)
        return df

    def heatmap_anni_maturita(self, df=None):
        """
        Creates a heatmap showing the relationship between years of activity and digital maturity.
        """
        df = df if df is not None else self.df
        df = self.mappa_maturita(df)
        df = self.categorizza_anni(df)
        
        ordine_anni = ['0-5 anni', '6-10 anni', '11-15 anni', '16-20 anni', 'Oltre 20 anni']
        pivot = pd.crosstab(df['anni_attivita_categoria'], df['maturita_digitale'])
        pivot = pivot.reindex(ordine_anni)
        
        fig = px.imshow(
            pivot,
            text_auto=True,
            color_continuous_scale=self.RED_COLOR_SCALE,
            labels={'x': 'Maturità Digitale', 'y': 'Fascia Anni Esperienza', 'color': 'Numero di Aziende'}
        )
        
        layout = self._create_base_plotly_layout(
            x_title='Maturità Digitale',
            y_title='Fascia di Anni',
            width=1500,
            height=800
        )
        layout.update(margin=dict(l=200, r=200, t=150, b=30))
        fig.update_layout(layout)
        
        st.plotly_chart(fig, use_container_width=True)

    def correlazione1_budget(self, df=None):
        """
        Creates a heatmap showing the relationship between budget and satisfaction levels.
        """
        df = df if df is not None else self.df
        df['budget_clean'] = df['budget_trans'].apply(lambda x: "Non specificato" if pd.isna(x) or x == 'Non so' else x)
        ordine_budget = ['Meno del 5%', '5%-10%', '11%-20%', '21%-30%', 'Più del 30%', 'Non specificato']
        
        pivot_budget_sodd = pd.crosstab(df['budget_clean'], df['soddisfazione'])
        pivot_budget_sodd = pivot_budget_sodd.reindex(ordine_budget)
        pivot_budget_sodd.columns = [self.SATISFACTION_MAPPING[val] for val in pivot_budget_sodd.columns]
        pivot_budget_sodd = pivot_budget_sodd.T
        
        fig = px.imshow(
                        pivot_budget_sodd,
                        text_auto=True,
                        color_continuous_scale=self.BLUE_COLOR_SCALE,
                        labels={'x': 'Budget (% sul fatturato)', 'y': 'Livello di Soddisfazione', 'color': 'Numero di Aziende'}
                        )
        
        fig.update_layout(self._create_base_plotly_layout(
                                                            x_title='Budget (% sul fatturato)',
                                                            y_title='Livello di Soddisfazione',
                                                            width=800,
                                                            height=800
                                                            ))
                                                        
        st.plotly_chart(fig, theme=None, use_container_width=True)

    def plot_criticita_budget(self, df=None):
        """
        Creates a heatmap showing the relationship between budget and criticality types.
        """
        df = df if df is not None else self.df
        # Clean criticality values
        df['criticita'] = df['criticita'].replace(self.CRITICALITY_MAPPING, regex=True)
        
        # Split multiple responses
        df_separato = df['criticita'].str.split(',', expand=True).stack().reset_index(level=1, drop=True)
        df_separato.name = 'criticita'
        df = df.drop('criticita', axis=1).join(df_separato)
        
        # Clean budget data
        df['budget_clean'] = df['budget_trans'].apply(lambda x: "Non specificato" if pd.isna(x) or x == 'Non so' else x)
        
        # Create pivot table
        pivot_budget_criticita = pd.crosstab(df['criticita'], df['budget_clean'])
        
        fig = px.imshow(
            pivot_budget_criticita,
            text_auto=True,
            color_continuous_scale=self.BLUE_COLOR_SCALE,
            labels={'x': 'Budget (% sul fatturato)', 'y': 'Tipo di Criticità', 'color': 'Numero di Aziende'}
        )
        
        fig.update_layout(self._create_base_plotly_layout(
            x_title='Budget (% sul fatturato)',
            y_title='Tipo di Criticità'
        ))
        
        st.plotly_chart(fig, use_container_width=True)

    def cor_budget_efficienza(self, df=None):
        """
        Creates a heatmap showing the relationship between budget and efficiency impact.
        """
        df = df if df is not None else self.df
        # Split efficiency impact into multiple rows
        df_exploded = df.assign(
            impatto_efficienza=df['impatto_efficienza'].str.split(',')
        ).explode('impatto_efficienza')
        
        # Clean whitespace
        df_exploded['impatto_efficienza'] = df_exploded['impatto_efficienza'].str.strip()
        
        # Create pivot table
        pivot_table = df_exploded.pivot_table(
                                                index='budget_trans',
                                                columns='impatto_efficienza',
                                                aggfunc='size',
                                                fill_value=0
                                                )
        
        # Add total responses column and sort
        pivot_table["Totale Risposte"] = pivot_table.sum(axis=1)
        pivot_table = pivot_table.sort_values(by="Totale Risposte", ascending=False)
        
        fig = px.imshow(
                        pivot_table.iloc[:, :-1].values,
                        labels=dict(x="Impatto Efficienza", y="Budget Investito", color="Conteggio"),
                        color_continuous_scale=self.GREEN_COLOR_SCALE,
                        x=pivot_table.columns[:-1],
                        y=pivot_table.index,
                        text_auto=True
                        )
        
        fig.update_layout(self._create_base_plotly_layout(
                                                        x_title="Impatto Efficienza",
                                                        y_title='Budget (% sul fatturato)',
                                                        width=800,
                                                        height=800
                                                        ))
        
        st.plotly_chart(fig, use_container_width=True)
