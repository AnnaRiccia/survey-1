import streamlit as st
from PIL import Image
from streamlit_option_menu import option_menu
import importlib
import pandas as pd
import os

st.set_page_config(
                    page_title="Template Project",
                    page_icon=Image.open("img/icon_site.png"),
                    layout="wide",
                    )

@st.cache_resource
def load_dataset():
    data = {}    
    data_config = {
                    'survey': 'data/cleaned_data.xlsx',
                    'ecofin': 'data/new.xlsx',
                    }
    for dataset, datatset_path in data_config.items():
        if os.path.exists(datatset_path):
            data[dataset] = pd.read_excel(datatset_path)
            st.session_state['data'] = data
        else:
            st.error(f"Dataset non trovato: {datatset_path}")
    return data


def get_pages():
 

    PAGES = 'pag' # cartella con le pagine, non usare pages!!!
    pages = []
    icons = []
    modules = []
    
    BLACKLIST_FILES = ['__init__', 'test','key','func','corr','ANNINA']  # aggiungi qui i file da escludere    
    # page_order = []
    page_order = ['analisi descrittiva','analisi dimensione','analisi correlazione','analisi ecofin','self analysis']

    files = [f[:-3] for f in os.listdir(PAGES) if f.endswith('.py') and f[:-3] not in BLACKLIST_FILES]
    files.sort(key=lambda x: page_order.index(x) if x in page_order else len(page_order))
    
    # Mapping icon 
    icon_mapping = {
                    #https://icons.getbootstrap.com/
                    'analisi descrittiva': 'bi-bullseye',
                    'analisi dimensione': 'bi-fire',
                    'analisi correlazione': 'bi-feather',
                    'analisi ecofin': 'bi-currency-euro',
                    'self analysis': 'bi-graph-up',
                    }
    
    for file in files:
        page_name = file.capitalize()
        pages.append(page_name)        
        icons.append(icon_mapping.get(file, 'bi-file'))        
        module = importlib.import_module(f'{PAGES}.{file}')
        modules.append(module)
    return pages, icons, modules

pages, icons, modules = get_pages()

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, function):
        self.apps.append({
                        "title": title,
                        "function": function
                        })

    def main():
        # Carica i modelli/dati all'avvio
        #st.session_state['models'] = load_models()
        st.session_state['data'] = load_dataset()

        with st.sidebar:
            app = option_menu(
                                menu_title="Menu",
                                options=pages,
                                icons=icons,
                                menu_icon="bi-list",
                                default_index=0,
                                styles={
                                        "container": {"padding": "5!important", "background-color": "white"},
                                        "icon": {"color": "black", "font-size": "21px"},
                                        "nav-link": {"color": "black", "font-size": "17px", "text-align": "left", "margin": "0px"},
                                        "nav-link-selected": {"color": "black", "background-color": "#eb5e67"}
                                        }
                                        )        
        selected_index = pages.index(app)
        modules[selected_index].main()


if __name__ == "__main__":
    MultiApp.main()