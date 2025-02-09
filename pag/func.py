import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
import plotly.io as pio
import pandas as pd
import plotly.express as px
import numpy as np

pio.templates.default = "plotly"

class Funz:
    def __init__(self):
        self.colors_blue = ['#a8c8f8', '#74aaff', '#4687e1', '#1d5b9b', '#134c6b']
        self.colors_red = ['#f8a8a8', '#f07474', '#e14444', '#b93333', '#7d1c1c']
        self.colors_green = ['#2e8b57', '#8fbc8f', '#66cdaa']
        self.colors_mixed = ['#9370DB', '#1E90FF', '#006D5B']

    def categorize_years(self, years):
        if years <= 5:
            return '0-5 anni'
        elif years <= 10:
            return '6-10 anni'
        elif years <= 15:
            return '11-15 anni'
        elif years <= 20:
            return '16-20 anni'
        else:
            return 'Oltre 20 anni'

    def plot_infr(self, df):
        infr_counts = df['presenza_infrastrutture'].value_counts()
        fig = go.Figure()

        fig.add_trace(
            go.Pie(
                labels=infr_counts.index,
                values=infr_counts.values,
                marker=dict(colors=self.colors_green),
                textinfo='percent+label',
                textposition='outside',
                pull=[0.1, 0.1],
                showlegend=False
            )
        )

        fig.update_layout(
            title=" ",
            title_x=0.5,
            height=500,
            width=1000,
            template='plotly_white'
        )

        st.plotly_chart(fig)

    def plot_fasce_anni(self, df):
        df['fascia_anni'] = df['Anni'].apply(self.categorize_years)
        counts = df['fascia_anni'].value_counts()

        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=(' ', ' '),
            specs=[[{'type': 'pie'}, {'type': 'bar'}]]
        )

        fig.add_trace(
            go.Pie(
                labels=counts.index,
                values=counts.values,
                name='Da quanto tempo lavori presso questa azienda?',
                marker=dict(colors=self.colors_blue),
                textinfo='percent+label',
                textposition='outside',
                pull=[0.1] * len(counts),
                showlegend=False
            ),
            row=1, col=1
        )

        fig.add_trace(
            go.Bar(
                x=counts.index,
                y=counts.values,
                name="Distribuzione fasce di anni",
                marker=dict(color='#4687e1'),
                showlegend=False
            ),
            row=1, col=2
        )

        fig.update_layout(
            showlegend=True,
            height=500,
            width=1000,
            template="plotly",
            bargap=0.1,
            bargroupgap=0.1,
            plot_bgcolor='white',  # Sfondo del grafico bianco
            paper_bgcolor='white',  # Sfondo esterno bianco
        )

        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)
        st.plotly_chart(fig, theme=None, use_container_width=True)

        
    def plot_role_distribution(self, df):
        it_roles = [
            'IT Manager', 'CIO', 'CFO', 'Coordinatore Data Unit', 'Chief Information Officer',
            'Responsabile IT', 'R&D Manager', 'Quality Assurance, Organization & Sustainability',
            'ICT Manager', 'AMMINISTRATORE DI SISTEMA', 'QHSE & IT Manager', 'Innovation Manager',
            'Co-founder e CTO', 'IT Manager', 'Direttore Innovation', 'Executive Assistant'
        ]

        df['Ruolo Informatico'] = df['ruolo'].apply(
            lambda x: 'Ruolo informatico' if x in it_roles else 'Altro ruolo'
        )
        role_counts = df['Ruolo Informatico'].value_counts()

        pie_fig = go.Pie(
            labels=role_counts.index,
            values=role_counts.values,
            textinfo='percent+label',
            marker=dict(colors=['#1d5b9b', '#a8c8f8'])
        )

        it_role_list = df[df['Ruolo Informatico'] == 'Ruolo informatico']['ruolo'].unique()

        fig = make_subplots(
            rows=1, cols=2,
            column_widths=[0.5, 0.5],
            specs=[[{'type': 'pie'}, {'type': 'table'}]]
        )

        fig.add_trace(pie_fig, row=1, col=1)
        fig.add_trace(
            go.Table(
                header=dict(values=["Ruoli Informatici"], fill_color='white', font=dict(color='black')),
                cells=dict(values=[it_role_list], fill_color='white', font=dict(color='black'))
            ),
            row=1, col=2
        )

        fig.update_layout(
            title_text=" ",
            height=500,
            width=1000,
            showlegend=False,
            plot_bgcolor='white',  # Sfondo del grafico bianco
            paper_bgcolor='white',  # Sfondo esterno bianco
        )

        # Rimuove la griglia
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)

        st.plotly_chart(fig, use_container_width=True)

    def plot_Rel(self, df):
        infr_counts = df['ecosistema_valore'].value_counts()
        fig = go.Figure()

        fig.add_trace(
            go.Pie(
                labels=infr_counts.index,
                values=infr_counts.values,
                marker=dict(colors=self.colors_mixed),
                textinfo='percent+label',
                textposition='outside',
                pull=[0.1, 0.1],
                showlegend=False
            )
        )

        fig.update_layout(
                            title=" ",
                            title_x=0.5,
                            height=500,
                            width=1000,
                            plot_bgcolor='white', 
                            paper_bgcolor='white', 
                    
                            )

        st.plotly_chart(fig)

    def analyze_digital_maturity(self, df):
            values_map = {
                'Siamo una azienda relativamente digitale; alcuni processi aziendali sono stati digitalizzati con l\'introduzione di tecnologie digitali': 'Relativamente digitale',
                'È stato avviato qualche progetto pilota di trasformazione digitale che al momento è ancora in corso': 'Qualche progetto avviato',
                'Siamo una azienda totalmente Digital Oriented; tutti i nostri processi sono supportati dall\'utilizzo di tecnologie digitali': 'Totalmente Digital Oriented',
                'Al momento non è in corso un processo di trasformazione digitale né è stato avviato e concluso in passato': 'Non digitalizzato',
                'È stato avviato qualche progetto pilota di trasformazione digitale che è stato interrotto e non portato a compimento': 'Qualche progetto interrotto'
            }

            df_copy = df.copy()
            df_copy['maturita_digitale'] = df_copy['maturita_digitale'].replace(values_map)
            maturity_levels = df_copy['maturita_digitale'].value_counts()
            total = maturity_levels.sum()
            percentages = (maturity_levels / total) * 100

            fig = make_subplots(
                rows=1, cols=2,
                specs=[[{'type': 'pie'}, {'type': 'bar'}]],
                subplot_titles=('Distribuzione percentuale', 'Distribuzione assoluta'),
                horizontal_spacing=0.2,
                column_widths=[0.5, 0.5]
            )

            # Add pie chart
            fig.add_trace(
                go.Pie(
                    labels=maturity_levels.index,
                    values=maturity_levels.values,
                    marker=dict(colors=self.colors_red[:len(maturity_levels)]),
                    textinfo='percent+label',
                    textposition='outside',
                    pull=[0.1] * len(maturity_levels),
                    hovertemplate="<b>%{label}</b><br>" +
                                "Valore: %{value}<br>" +
                                "Percentuale: %{percent:.1f}%<extra></extra>"
                ),
                row=1, col=1
            )

            # Add bar chart without text labels
            fig.add_trace(
                go.Bar(
                    x=maturity_levels.index,
                    y=maturity_levels.values,
                    marker=dict(color=self.colors_red[:len(maturity_levels)]),
                    hovertemplate="<b>%{x}</b><br>" +
                                "Valore: %{y}<br>" +
                                "Percentuale: %{text}<extra></extra>"
                ),
                row=1, col=2
            )

            # Update layout
            fig.update_layout(
                title=dict(
                    text="Livello di maturità digitale presente in azienda",
                    x=0.5,
                    y=0.98,
                    xanchor='center',
                    yanchor='top',
                    font=dict(size=16)
                ),
                height=700,
                width=1200,
                showlegend=False,
                bargap=0.3,
                margin=dict(l=50, r=50, t=80, b=150), 
                xaxis2=dict(
                    tickangle=90,  # Vertical text
                    tickmode='array',
                    ticktext=maturity_levels.index,
                    tickvals=list(range(len(maturity_levels))),
                    title=None  # Removed x-axis title
                ),
                yaxis2=dict(
                    title="Numero di aziende",
                    range=[0, max(maturity_levels.values) * 1.1],
                    tickmode='linear',
                    dtick=10  # Changed to 10
                ),
                    plot_bgcolor='white',  
            paper_bgcolor='white'
            )
            
            # Update subplot titles - make them smaller and closer to the plots
            fig.update_annotations(font_size=12, y=0.95)
            
            # Add additional title at the bottom
            fig.add_annotation(
                text="Analisi del livello di maturità digitale nelle aziende",
                xref="paper",
                yref="paper",
                x=0.5,
                y=-0.2,  # Position below the plot
                showarrow=False,
                font=dict(size=14),
                xanchor='center'
            )
            fig.update_xaxes(tickfont=dict(size=10))
            fig.update_yaxes(tickfont=dict(size=10))

            st.plotly_chart(fig, theme=None, use_container_width=True)
            
            return df_copy['maturita_digitale']

    def plot_strategie_talent(self, df):
        strategy_counts = {
            'Nessuna delle precedenti': 0,
            "Reclutamento di nuovi talenti con competenze digitali ": 0,
            "Formazione continua e sviluppo professionale": 0,
            "Collaborazioni con università e istituti di ricerca ": 0,
            "Programmi di mentoring e coaching ": 0,
            "Organizzazione di hackathon e conferenze tecnologiche ": 0
        }

        for response in df['strategie_talent'].fillna(''):
            for key in strategy_counts.keys():
                if key in response:
                    strategy_counts[key] += 1

        total = sum(strategy_counts.values())
        percentages = [(val / total) * 100 if total > 0 else 0 for val in strategy_counts.values()]

        fig = go.Figure(data=[go.Pie(
            labels=list(strategy_counts.keys()),
            values=percentages,
            textinfo='percent+label',
            textposition='outside',
            pull=[0.1] * len(strategy_counts),
            marker=dict(colors=['#ffcc66', '#ff9933', '#ff6600', '#cc3300', '#990000']),
            showlegend=False
        )])

        fig.update_layout(
            title='   ',
            height=500,
            width=800,
            margin=dict(l=40, r=40, t=40, b=40),
            template="plotly"
        )

        st.plotly_chart(fig, use_container_width=True)

    def plot_trans(self, df):
        trans_counts = df['trans_digitale'].value_counts()
        fig = go.Figure()

        fig.add_trace(
            go.Pie(
                labels=trans_counts.index,
                values=trans_counts.values,
                marker=dict(colors=self.colors_red[:3]),
                textinfo='percent+label',
                textposition='outside',
                pull=[0.1, 0.1],
                showlegend=False
            )
        )

        fig.update_layout(
            title=" ",
            title_x=0.5,
            height=500,
            width=1000
        )

        st.plotly_chart(fig)

    def inizio_trans(self, df):
        df['inizio_trans'].fillna('Nessuna risposta', inplace=True)
        distribution_counts = df['inizio_trans'].value_counts()
        total = distribution_counts.sum()
        percentages = (distribution_counts / total) * 100

        fig = make_subplots(
            rows=1, cols=2,
            specs=[[{'type': 'pie'}, {'type': 'bar'}]],
            column_widths=[0.48, 0.48],
            horizontal_spacing=0.2
        )

        fig.add_trace(
            go.Pie(
                labels=distribution_counts.index,
                values=distribution_counts.values,
                textinfo='percent+label',
                textposition='outside',
                pull=[0.1] * len(distribution_counts),
                marker=dict(colors=self.colors_red[:len(distribution_counts)]),  # Pie charts use 'colors' (plural)
                showlegend=True
            ),
            row=1, col=1
        )

        fig.add_trace(
            go.Bar(
                x=distribution_counts.index,
                y=distribution_counts.values,
                text=percentages.round(1).astype(str) + '%',
                textposition='outside',
                marker=dict(color=self.colors_red[:len(distribution_counts)]),  # Bar charts use 'color' (singular)
                showlegend=False
            ),
            row=1, col=2
        )

        fig.update_layout(
            title="  ",
            title_x=0.5,
            height=500,
            width=1000,
            template='plotly_white',
            plot_bgcolor='white',  
            paper_bgcolor='white', )
        
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)
        st.plotly_chart(fig, theme=None, use_container_width=True)

    ##################################################################################################### stimoli trans ###########################################################################################

    def plot_stimoli_trans_funnel(self, df):
        df['stimoli_trans'] = df['stimoli_trans'].fillna('Nessuna risposta')
        df['stimoli_trans'] = df['stimoli_trans'].replace(
            'Stimoli da associazioni di categoria/centri di ricerca/ istituzioni universitarie',
            'Stimoli da associazioni e centri di ricerca'
            )

        stimuli_counts = {
                        'Business partner a seguito di attività di formazione e aggiornamento': 0,
                        'Competitors': 0,
                        'Sollecitazioni interne': 0,
                        'Stimoli da associazioni e centri di ricerca': 0,
                        'Nessuna risposta': 0,
                    }

        for response in df['stimoli_trans']:
            for key in stimuli_counts.keys():
                if key in response:
                    stimuli_counts[key] += 1

        df_stimoli = pd.DataFrame(
                                    list(stimuli_counts.items()),
                                    columns=['Stimoli', 'Conteggi']
                                    )

        fig = px.bar(
                    df_stimoli,
                    x='Stimoli',
                    y='Conteggi',
                    color='Stimoli',
                    color_discrete_sequence=self.colors_red,
                    text='Conteggi',
                    title="   ",
                    width=500,
                    height=500,
                    )
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)
        
        fig.update_layout(showlegend=False,
                          plot_bgcolor='white', 
                        paper_bgcolor='white', )
        st.plotly_chart(fig, theme=None, use_container_width=True)
## originale 488
########################################################## COINVOGLIEMNTO LEADER ###################################################################
    def plot_coinvolgimento_leader(self, df):
        mappa_coinvolgimento = {
            0: 'Per niente coinvolto',
            2: 'Poco coinvolto',
            3: 'Parzialmente coinvolto',
            4: 'Molto coinvolto',
            5: 'Pienamente coinvolto'
        }

        df['coinvolgimento_leader'] = df['coinvolgimento_leader'].map(mappa_coinvolgimento)
        coinvolgimento_counts = df['coinvolgimento_leader'].value_counts().sort_index()

        total = coinvolgimento_counts.sum()
        percentages = (coinvolgimento_counts / total) * 100

        fig = make_subplots(
            rows=1, cols=2,
            specs=[[{'type': 'pie'}, {'type': 'bar'}]],
            horizontal_spacing=0.2
        )

        fig.add_trace(
            go.Pie(
                labels=coinvolgimento_counts.index.astype(str),
                values=coinvolgimento_counts.values,
                marker=dict(colors=self.colors_red[:len(coinvolgimento_counts)]),
                textinfo='percent+label',
                textposition='outside',
                pull=[0.1] * len(coinvolgimento_counts)
            ),
            row=1, col=1
        )

        fig.add_trace(
            go.Bar(
                x=coinvolgimento_counts.index.astype(str),
                y=coinvolgimento_counts.values,
                text=percentages.round(1).astype(str) + '%',
                textposition='auto',
                marker=dict(color=self.colors_red[:len(coinvolgimento_counts)])
            ),
            row=1, col=2
        )

        # Imposta sfondo bianco e rimuove la griglia
        fig.update_layout(
            height=500,
            width=500,
            showlegend=False,
            bargap=0.1,
            margin=dict(l=40, r=40, t=0, b=40),
            plot_bgcolor='white',  
            paper_bgcolor='white'   
        )

        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)

        st.plotly_chart(fig, theme=None, use_container_width=True)


############################################################################################### responsabilità dipendenti ######################################################################

    def plot_resp_dipendenti_funnel(self, df):
        df['resp_dipendenti'] = df['resp_dipendenti'].fillna('Nessuna risposta')

        dizionario_resp_dipendenti = {
                                        'Assegnazione di obiettivi individuali': 0,
                                        'Creazione di un senso condiviso di responsabilità': 0,
                                        'Promozione della collaborazione interfunzionale': 0,
                                        'Definizione di ruoli chiari': 0,
                                        'Incentivi per l\'innovazione e il miglioramento continuo': 0,
                                        'Nessuna risposta': 0
                                        }

        for x in df['resp_dipendenti']:
            for key in dizionario_resp_dipendenti.keys():
                if key in x:
                    dizionario_resp_dipendenti[key] += 1

        df_resp_dipendenti = pd.DataFrame(
            list(dizionario_resp_dipendenti.items()),
            columns=['Stimoli', 'Conteggi']
        )

        fig = px.bar(
                    df_resp_dipendenti,
                    x='Stimoli',
                    y='Conteggi',
                    color='Stimoli',
                    color_discrete_sequence=self.colors_red,
                    text='Conteggi',
                    title="  ",
                    width=800,
                    height=800
                    )
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)
        fig.update_layout(showlegend=False,
                        plot_bgcolor='white',  
                        paper_bgcolor='white'  
        )
        st.plotly_chart(fig, theme=None, use_container_width=True)

############################################################################ cosa #############################################################################################################################################

    def analyze_fase_trans(self, df):
        values = {
            'Adozione e Utilizzo di Risorse Digitali': 'Adozione e utilizzo',
            'Analisi e mappatura dei processi esistenti': 'Analisi dei processi',
            'Definizione della strategia e degli obiettivi': 'Definizione strategia',
            'Progettazione e pianificazione': 'Pianificazione e progettazione',
            'nan': 'Nessuna risposta'
        }

        df['fase_trans'] = df['fase_trans'].replace(values)
        fase_levels = df['fase_trans'].value_counts()
        total = fase_levels.sum()
        percentages = (fase_levels / total) * 100

        fig = make_subplots(
            rows=1, cols=2,
            specs=[[{'type': 'pie'}, {'type': 'bar'}]],
            horizontal_spacing=0.2
        )

        # Pie chart - uses 'colors'
        fig.add_trace(
            go.Pie(
                labels=fase_levels.index,
                values=fase_levels.values,
                marker=dict(colors=self.colors_red[:len(fase_levels)]),
                textinfo='percent+label',
                textposition='outside',
                pull=[0.1] * len(fase_levels)
            ),
            row=1, col=1
        )

        # Bar chart - uses 'color'
        fig.add_trace(
            go.Bar(
                x=fase_levels.index,
                y=fase_levels.values,
                text=percentages.round(1).astype(str) + '%',
                textposition='auto',
                marker=dict(color=self.colors_red[:len(fase_levels)])  # Changed from colors to color
            ),
            row=1, col=2
        )

        fig.update_layout(
            height=500,
            width=800,
            showlegend=False,
            bargap=0.1,
            margin=dict(l=40, r=40, t=0, b=40),
            template="plotly",
            plot_bgcolor='white',  
            paper_bgcolor='white'  
        )
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)

        st.plotly_chart(fig, theme=None, use_container_width=True)

############################################################################ cosa #############################################################################################################################################

    def analyze_budget_trans(self, df):
        values = {
            '11%-20%': '11%-20% del budget',
            '21%-30%': '21%-30% del budget',
            '5%-10%': '5%-10% del budget',
            'Meno del 5%': 'Meno del 5% del budget',
            'Non so': 'Non so',
            'Più del 30%': 'Più del 30% del budget',
            'nan': 'Nessuna risposta'
        }

        df['budget_trans'] = df['budget_trans'].replace(values)
        budget_levels = df['budget_trans'].value_counts()
        total = budget_levels.sum()
        percentages = (budget_levels / total) * 100

        fig = make_subplots(
            rows=1, cols=2,
            specs=[[{'type': 'pie'}, {'type': 'bar'}]],
            horizontal_spacing=0.2
        )

        # Pie chart - uses 'colors'
        fig.add_trace(
            go.Pie(
                labels=budget_levels.index,
                values=budget_levels.values,
                marker=dict(colors=self.colors_red[:len(budget_levels)]),
                textinfo='percent+label',
                textposition='outside',
                pull=[0.1] * len(budget_levels)
            ),
            row=1, col=1
        )

        # Bar chart - uses 'color'
        fig.add_trace(
            go.Bar(
                x=budget_levels.index,
                y=budget_levels.values,
                text=percentages.round(1).astype(str) + '%',
                textposition='auto',
                marker=dict(color=self.colors_red[:len(budget_levels)])  # Changed from colors to color
            ),
            row=1, col=2
        )

        fig.update_layout(
            height=500,
            width=1000,
            showlegend=False,
            bargap=0.1,
            margin=dict(l=40, r=40, t=0, b=40),
            plot_bgcolor='white', 
            paper_bgcolor='white'
        )
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)

        st.plotly_chart(fig, theme=None, use_container_width=True)

    def plot_processi_digit(self, df):
        df['processi_digit'] = df['processi_digit'].fillna('Nessuna risposta')

        dizionario_processi_digit = {
            'Consegna del Prodotto e del Servizio (Produzione, consegna del servizio, Gestione dell\'ambiente operativo, Gestione della manutenzione e del supporto)': 'Consegna Servizio',
            'Gestione della Catena di Approvvigionamento (Pianificazione della catena di approvvigionamento, Approvvigionamento, Produzione, Logistica e distribuzione)': 'Catena di Approvv.',
            'Gestione Ambientale, Sanità e Sicurezza (Pianificazione della salute e della sicurezza, Gestione della salute e della sicurezza sul lavoro, Gestione della salute ambientale e dei sistemi di sicurezza)': 'Sicurezza e Ambiente',
            'Gestione e Amministrazione dell\'Organizzazione': 'Amministrazione',
            'Marketing e Vendite': 'Marketing e Vendite',
            'Sviluppo del Prodotto e del Servizio': 'Sviluppo Prodotto',
            'Nessuna risposta': 'Nessuna risposta'
        }

        dizionario_abbreviato = {abbreviazione: 0 for abbreviazione in dizionario_processi_digit.values()}

        for x in df['processi_digit']:
            for key, abbreviazione in dizionario_processi_digit.items():
                if key in x:
                    dizionario_abbreviato[abbreviazione] += 1

        df_processi_digit = pd.DataFrame(
            list(dizionario_abbreviato.items()),
            columns=['Processi Digitali', 'Conteggi']
        )

        fig = px.bar(
                    df_processi_digit,
                    x='Processi Digitali',
                    y='Conteggi',
                    color='Processi Digitali',
                    color_discrete_sequence=self.colors_red,
                    text='Conteggi',
                    title="  ",
                    width=500,
                    height=500,
                    )
        fig.update_layout(
            plot_bgcolor='white', 
            paper_bgcolor='white', 
            showlegend=False # Sfondo esterno bianco
        )
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)
        st.plotly_chart(fig, theme=None, use_container_width=True)

    def plot_criticita(self, df):
        df['criticita'] = df['criticita'].str.replace(
            r'Inadeguata analisi dei Business Case, la quale ha portato a sottovalutare alcune criticità o non cogliere determinate opportunità.',
            'Inadeguata analisi dei Business Case', regex=True
        )
        df['criticita'] = df['criticita'].str.replace(
            r'Problematiche emerse durante la fase di implementazione, come ad esempio un non adeguato ingaggio degli attori coinvolti.',
            'Problematiche emerse durante la fase di implementazione', regex=True
        )
        df['criticita'] = df['criticita'].str.replace(
            r'Inadeguato allineamento tra strategia e attività svolta.',
            'Inadeguato allineamento tra strategia e attività svolta', regex=True
        )

        dizionario1 = {
            'Inadeguata analisi dei Business Case': 0,
            'Problematiche emerse durante la fase di implementazione': 0,
            'Inadeguato allineamento tra strategia e attività svolta': 0,
            'Governance del progetto non adeguata': 0
        }

        for risposta in df['criticita'].fillna(''):
            for key in dizionario1.keys():
                if key in risposta:
                    dizionario1[key] += 1

        df_criticita = pd.DataFrame({
            'Criticità': list(dizionario1.keys()),
            'Conteggi': list(dizionario1.values())
        })

        fig = px.bar(
            df_criticita,
            x='Criticità',
            y='Conteggi',
            color='Criticità',
            color_discrete_sequence=self.colors_red[:4],
            text='Conteggi',
            title="Distribuzione delle criticità",
            width=400,
            height=500
        )
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)
        fig.update_layout(showlegend=False,
                        plot_bgcolor='white', 
                        paper_bgcolor='white' )
        st.plotly_chart(fig, theme=None, use_container_width=True)

    def analyze_soddisfazione(self, df):
        if 'soddisfazione' not in df.columns:
            st.error("Colonna 'soddisfazione' non trovata nel DataFrame.")
            return

        satisfaction_map = {
                            1.0: "Per niente soddisfatto",
                            2.0: "Poco soddisfatto",
                            3.0: "Soddisfatto",
                            4.0: "Molto soddisfatto",
                            5.0: "Pienamente soddisfatto",
                            }

        soddisfazione_values = df['soddisfazione'].dropna()
        mapped_values = soddisfazione_values.map(satisfaction_map)
        value_counts = mapped_values.value_counts()

        colors = ['#FAD02E', '#F28D35', '#D83367', '#1F4068', '#5B84B1']
        
        fig = go.Figure(data=[go.Pie(
            labels=value_counts.index,
            values=value_counts.values,
            marker=dict(colors=colors * (len(value_counts) // 5 + 1)),
            textinfo='percent+label',
            textposition='outside',
            pull=[0.1] * len(value_counts),
        )])

        fig.update_layout(
                            height=500,
                            width=800,
                            title="   ",
                            margin=dict(l=40, r=40, t=40, b=40),
                            plot_bgcolor='white', 
                        paper_bgcolor='white'
                        )
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)

        st.plotly_chart(fig, use_container_width=True)

    def analyze_impatto_efficienza(self, df):
        """
        Analizza una colonna in cui ogni cella può contenere più valori separati da virgola,
        conta le occorrenze di ogni valore e visualizza solo il risultato con un grafico a barre.
        
        Args:
            df (pd.DataFrame): DataFrame contenente i dati.
        """
        
        # Verifica se la colonna 'impatto_efficienza' esiste nel DataFrame
        if 'impatto_efficienza' not in df.columns:
            st.error("Colonna 'impatto_efficienza' non trovata nel DataFrame.")
            return

        # Crea una lista di tutti i valori unici separati da virgola
        all_values = []

        # Estrai tutti i valori separati da virgola e aggiungili alla lista
        for entry in df['impatto_efficienza']:
            if isinstance(entry, str):  # Verifica che l'entry sia una stringa
                values = entry.split(',')
                all_values.extend([v.strip() for v in values])  # Rimuove spazi indesiderati
            else:
                continue

        # Conta le occorrenze di ciascun valore
        value_counts = pd.Series(all_values).value_counts()

        # Creazione del grafico a barre
        fig = go.Figure(data=[go.Bar(
            x=value_counts.index, 
            y=value_counts.values,
            text=value_counts.values,  # Mostra il conteggio sopra le barre
            textposition='auto',  # Posiziona il testo sopra le barre
            marker=dict(color=['#FAD02E', '#F28D35', '#D83367', '#1F4068', '#5B84B1'] * (len(value_counts) // 5 + 1))  # Colori dinamici
        )])

        # Personalizzazione del layout
        fig.update_layout(
            height=500, 
            width=800,
            title="   ",  # Titolo del grafico 
            margin=dict(l=40, r=40, t=40, b=40),
            template="plotly"
        )

        # Mostra il grafico in Streamlit
        st.plotly_chart(fig, use_container_width=True)

    def analyze_miglioramenti(self, df):
        """
        Analizza una colonna in cui ogni cella può contenere più valori separati da virgola,
        conta le occorrenze di ogni valore e visualizza solo il risultato con un grafico a torta.
        
        Args:
            df (pd.DataFrame): DataFrame contenente i dati.
        """
        
        # Verifica se la colonna 'miglioramenti' esiste nel DataFrame
        if 'miglioramenti' not in df.columns:
            st.error("Colonna 'miglioramenti' non trovata nel DataFrame.")
            return

        # Crea una lista di tutti i valori unici separati da virgola
        all_values = []

        # Estrai tutti i valori separati da virgola e aggiungili alla lista
        for entry in df['miglioramenti']:
            if isinstance(entry, str):  # Verifica che l'entry sia una stringa
                values = entry.split(',')
                all_values.extend([v.strip() for v in values])  # Rimuove spazi indesiderati
            else:
                continue

        # Conta le occorrenze di ciascun valore
        value_counts = pd.Series(all_values).value_counts()

        # Creazione del grafico a torta
        fig = go.Figure(data=[go.Pie(
            labels=value_counts.index, 
            values=value_counts.values,
            marker=dict(colors=['#FAD02E', '#F28D35', '#D83367', '#1F4068', '#5B84B1'] * (len(value_counts) // 5 + 1)),  # Colori dinamici
            textinfo='percent+label', 
            textposition='outside', 
            pull=[0.1] * len(value_counts)  # Aggiunge un po' di distacco per ogni fetta
        )])

        # Personalizzazione del layout
        fig.update_layout(
                        height=500, 
                        width=800,
                        title="  ",  # Titolo del grafico
                        showlegend=False, 
                        margin=dict(l=40, r=40, t=40, b=40),
                        template="plotly",
                        )
        # Mostra il grafico in Streamlit
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)
        st.plotly_chart(fig, use_container_width=True)

#########################################################################
#########################################################################
class GraficoFigure:
    def __init__(self, df):
        """
        Inizializza la classe con il dataframe.
        """
        self.df = df  # Memorizza il dataframe nell'istanza
        
        # Dizionario per mappare le risposte
        self.mappa_risposte = {
            "Molto D'accordo": 4,
            "D'accordo": 3,
            "Neutrale": 2,
            "In disaccordo": 1,
            np.nan: 0  # Se np.nan è una risposta, mappiamola a 0
        }
        self.custom_colors = ['#ffcc66', '#ff9933', '#ff6600', '#cc3300', '#990000']
    def plot_graph(self, column_name):
        """
        Genera un grafico a torta e a barre per una colonna specifica del dataframe.
        """
        df = self.df.copy()  # Usa una copia del dataframe per non modificare l'originale
        df[column_name] = df[column_name].map(self.mappa_risposte)
        competency_counts = df[column_name].value_counts()

        # Mappa inversa per visualizzare le risposte originali
        response_map_inverse = {
            4: "Molto D'accordo",
            3: "D'accordo",
            2: "Neutrale",
            1: "In disaccordo",
            0: "Nessuna risposta"
        }

        competency_counts.index = competency_counts.index.map(response_map_inverse)
        total = competency_counts.sum()
        percentages = (competency_counts / total) * 100

        # Creazione del grafico
        fig = make_subplots(
            rows=1, cols=2, 
            specs=[[{'type': 'pie'}, {'type': 'bar'}]],
            column_widths=[0.48, 0.48],
            horizontal_spacing=0.2
        )

        fig.add_trace(
            go.Pie(
                labels=competency_counts.index, 
                values=competency_counts.values,
                texttemplate='%{label}<br><b>%{percent}</b>',
                textposition='outside',
                pull=[0.1] * len(competency_counts),
                showlegend=False,
            marker=dict(colors=self.custom_colors)
            ),
            row=1, col=1
        )

        fig.add_trace(
            go.Bar(
                x=competency_counts.index,
                y=competency_counts.values,
                text=percentages.round(1).astype(str) + '%',
                textposition='auto',
                marker=dict(color=self.custom_colors)
            ),
            row=1, col=2
        )

        return fig

    # Metodi specifici per ogni colonna (richiamano plot_graph)
    def plot_cdh_conoscenze(self):
        st.plotly_chart(self.plot_graph("cdh_conoscenze"), use_container_width=True)

    def plot_cdh_competenze_tecniche(self):
        st.plotly_chart(self.plot_graph('cdh_competenze_tecniche'), use_container_width=True)

    def plot_cdh_abilita_analitiche(self):
        st.plotly_chart(self.plot_graph('cdh_abilita_analitiche'), use_container_width=True)

    def plot_cdh_innovazione(self):
        st.plotly_chart(self.plot_graph('cdh_innovazione'), use_container_width=True)

    def plot_cdh_formazione(self):
        st.plotly_chart(self.plot_graph('cdh_formazione'), use_container_width=True)

#################################################################################### INFRASTRUTTURE DIGITALI ####################################################################################

class GraficoInfrastruttura:
    def __init__(self, df):
        self.df = df
        self.mappa_risposte = {
            'Molto D\'accordo': 4,
            'D\'accordo': 3,
            'Neutrale': 2,
            'In disaccordo': 1,
            np.nan: 0  # Se np.nan è una risposta, mappiamola a 0
        }
                # Mappa inversa per visualizzare le risposte originali
        self.mappa_risposte_inversa = {
            4: "Molto D\'accordo",
            3: "D\'accordo",
            2: "Neutrale",
            1: "In disaccordo",
            0: "Nessuna risposta"
        }
        self.colori = ['#228B22', '#8fbc8f', '#66cdaa', '#2e8b57', '#006400']

    def plot_graph(self, column_name):
        self.df[column_name] = self.df[column_name].map(self.mappa_risposte)
        competency_counts = self.df[column_name].value_counts()
        competency_counts.index = competency_counts.index.map(self.mappa_risposte_inversa)

        total = competency_counts.sum()
        percentages = (competency_counts / total) * 100

        fig = make_subplots(
            rows=1, cols=2, 
            specs=[[{'type': 'pie'}, {'type': 'bar'}]],
            column_widths=[0.48, 0.48],
            horizontal_spacing=0.2
        )

        fig.add_trace(
            go.Pie(
                labels=competency_counts.index, 
                values=competency_counts.values,
                marker=dict(colors=self.colori),
                texttemplate='%{label}<br><b>%{percent}</b>',
                textposition='outside',
                pull=[0.1] * len(competency_counts),
                showlegend=False
            ),
            row=1, col=1
        )

        fig.add_trace(
            go.Bar(
                x=competency_counts.index,
                y=competency_counts.values,
                marker=dict(color=self.colori[:len(competency_counts)]),
                text=[f"{p:.1f}%" for p in percentages],
                #text=percentages.values.round(1).astype(str) + '%',
                textposition='outside',
                showlegend=False
            ),
            row=1, col=2
        )

        fig.update_layout(
            title=" ",
            title_x=0.5,
            height=500, 
            width=1000,
            template='plotly_white'
        )

        return fig

    def plot_hardware(self):
        st.plotly_chart(self.plot_graph('infr_hardware'), use_container_width=True, key='hardware_button')

    def plot_software(self):
        st.plotly_chart(self.plot_graph('infr_software'), use_container_width=True, key='software_button')

    def plot_cloud(self):
        st.plotly_chart(self.plot_graph('infr_cloud'), use_container_width=True, key='cloud_button')

    def plot_sicurezza(self):
        st.plotly_chart(self.plot_graph('infr_sicurezza'), use_container_width=True, key='sicurezza_button')

###################################################### ECOSISTEMA RELAZIONI #########################################################################################################

class GraficoRelazioni:
    def __init__(self, df):
        self.df = df
        self.mappa_risposte = {
            'Molto D\'accordo': 4,
            'D\'accordo': 3,
            'Neutrale': 2,
            'In disaccordo': 1,
            np.nan: 0  # Se np.nan è una risposta, mappiamola a 0
        }
        self.mappa_risposte_inversa = {
                4: 'Molto D\'accordo',
                3: 'D\'accordo',
                2: 'Neutrale',
                1: 'In disaccordo',
                0: 'Nessuna risposta'
            }
        self.colori = ['#228B22', '#8fbc8f', '#66cdaa', '#2e8b57', '#006400']

# Funzione generica per creare grafici a torta e a barre per una colonna
    def plot_graph2(self, column_name):
            self.df[column_name] = self.df[column_name].map(self.mappa_risposte)
            competency_counts = self.df[column_name].value_counts()

            # Riorganizza l'indice e applica la mappa inversa per ottenere le etichette originali
            competency_counts.index = competency_counts.index.map(self.mappa_risposte_inversa)

            # Calcola la percentuale di ciascun valore
            total = competency_counts.sum()
            percentages = (competency_counts / total) * 100

            # Crea un subplot con 1 riga e 2 colonne (grafico a torta e grafico a barre)
            fig = make_subplots(
                rows=1, cols=2, 
                specs=[[{'type': 'pie'}, {'type': 'bar'}]],  # Usa 'bar' per il grafico a barre
                column_widths=[0.48, 0.48],  # Imposta la larghezza delle colonne (più vicine)
                horizontal_spacing=0.2  # Riduce la distanza orizzontale tra i grafici
            )

            # Aggiungi il grafico a torta
            fig.add_trace(
                go.Pie(
                    labels=competency_counts.index, 
                    values=competency_counts.values,
                    marker=dict(
                        colors=['#9370DB', '#1E90FF', '#006D5B', '#6A5ACD', '#4B0082']  # Gradazione di colori
                    ),
                    texttemplate='%{label}<br><b>%{percent}</b>',  # Mostra percentuale e etichetta
                    textposition='outside',  # Posiziona il testo fuori dalle fette
                    pull=[0.1] * len(competency_counts),  # Aggiungi un po' di spazio tra le fette
                    showlegend=False  # Nascondi la legenda
                ),
                row=1, col=1
            )
            # Aggiungi il grafico a barre con asse Y e X invertiti
            fig.add_trace(
                go.Bar(
                    x=competency_counts.index,  # Etichette ordinate
                    y=competency_counts.values,  # Conteggi ordinati
                    text=[f"{p:.1f}%" for p in percentages],
                    textposition='outside',  # Posiziona il testo sopra le barre
                    marker=dict(
                        color=['#9370DB', '#1E90FF', '#006D5B', '#6A5ACD', '#4B0082'][:len(competency_counts)],  # Applica i colori nell'ordine specificato
                    ),
                    showlegend=False,  # Nascondi la legenda per il grafico a barre
                ),
                row=1, col=2
            )

            # Aggiungi titolo e layout
            fig.update_layout(
                title=" ",  # Non inserire alcun titolo
                title_x=0.5,  # Centra il titolo orizzontalmente
                height=500, 
                width=1000,  # Imposta la larghezza del grafico
                template='plotly_white',
                xaxis=dict(title='Conteggio', showgrid=True),  # Aggiungi l'asse X
                yaxis=dict(title='Risposte', showgrid=True),  # Aggiungi l'asse Y
            )

            return fig

        # Funzione per il grafico delle interazioni digitali
    def plot_cdh_interazione(self):
            """
            Genera il grafico per la colonna 'eco_interazione' in formato a torta e a barre.
            """
            st.plotly_chart(self.plot_graph2('eco_interazione'), use_container_width=True, key='eco_interazione')

        # Funzione per il grafico delle piattaforme digitali
    def plot_cdh_piattaforme(self):
            """
            Genera il grafico per la colonna 'eco_piattaforme' in formato a torta e a barre.
            """
            st.plotly_chart(self.plot_graph2('eco_piattaforme'), use_container_width=True, key='eco_piattaforme')

        # Funzione per il grafico dei processi digitalizzati
    def plot_cdh_processi(self):
            """
            Genera il grafico per la colonna 'eco_processi' in formato a torta e a barre.
            """
            st.plotly_chart(self.plot_graph2('eco_processi'), use_container_width=True, key='eco_processi')
