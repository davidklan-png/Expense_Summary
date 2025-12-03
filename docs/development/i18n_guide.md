# **Streamlit Multi-Language Architecture (English/Japanese)**

## **1\. Project Structure**

The architecture utilizes Streamlit's native multi-page app feature and a dedicated Python module for translation strings. This ensures separation of concerns (Content, Logic, UI).

.  
├── app.py                      \# Main entry point (Landing page, Global config, Language Selector)  
├── translations.py             \# I18n Core: Python dictionary holding all translated strings  
├── pages/  
│   ├── 01\_data\_explorer.py     \# Example Page 1 (Uses I18n utility)  
│   └── 02\_report\_view.py       \# Example Page 2 (Uses I18n utility)  
└── utils.py                    \# Utility functions (Language fetching logic)

## **2\. Core I18n Strategy**

The entire internationalization is handled by a Python dictionary in translations.py and a core utility function in utils.py.

### **2.1. Translation Bundle (translations.py)**

All user-facing text will be stored in a nested dictionary structure.

* **Top Level:** Language codes ('en', 'ja').  
* **Second Level:** Page/Component names ('homepage', 'data\_explorer').  
* **Third Level:** Translation keys ('title', 'greeting').

**Handling Dynamic Text:** Variables (like a user's name or a data count) should use Python f-string or .format() syntax within the translation string (e.g., 'output\_message': 'Nice to meet you, {}\!'.format(name)).

### **2.2. Session State Management (app.py)**

The main application file will initialize and manage the global language state using Streamlit's st.session\_state.

* **Key State Variable:** st.session\_state\['lang'\] will store the current language code (defaulting to 'en').  
* **Configuration:** The sidebar will contain a st.selectbox or st.radio widget bound to this state variable, triggering an automatic rerun when the language changes.

## **3\. Implementation Outline (For Coding Agent)**

### **File 1: translations.py (Translation Bundle)**

1. **Define TRANSLATIONS Dictionary:** Create a large Python dictionary.  
   * Include keys for global elements (e.g., 'global': {'language\_selector\_label'}).  
   * Include keys for each page (e.g., 'homepage': {'title', 'introduction'}).  
   * Ensure all keys exist for both 'en' and 'ja'.

### **File 2: utils.py (I18n Utility)**

1. **Define load\_translations() function:** A function that imports TRANSLATIONS and stores it in st.session\_state if it doesn't already exist.  
2. **Define get\_text(key\_path) function:** The main utility function used across the app.  
   * Accepts a key\_path (e.g., 'homepage.title').  
   * Reads the current language from st.session\_state\['lang'\].  
   * Fetches the corresponding text from the global translation dictionary.

### **File 3: app.py (Entry Point & Global Config)**

1. **Import:** Import streamlit and the utility functions from utils.py.  
2. **Initialize:** Call load\_translations() to ensure the translation bundle is available in session state.  
3. **Language Selector:**  
   * Create a mapping of display names to language codes (e.g., {'English': 'en', '日本語': 'ja'}).  
   * Implement a st.sidebar.selectbox to allow the user to choose a language. The selection updates st.session\_state\['lang'\].  
4. **Page Content:** Use get\_text() for all displayed strings on the main page (e.g., st.title(get\_text('homepage.title'))).

### **File 4 & 5: pages/01\_data\_explorer.py and pages/02\_report\_view.py**

1. **Structure:** These files will automatically be recognized as separate pages.  
2. **Rendering:** Each page will import and use get\_text() to render its specific content, automatically displaying the language selected in the global state (app.py).

