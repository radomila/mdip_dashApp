# DashApp 

Tento projekt byl vytvořen v rámci předmětu MDIP a jedná se o dashboard vizualizující výši platů a situaci na trhu práce v oblasti umělé inteligence, strojového učení a data science. 

Zdroj dat: https://aijobs.net/salaries/download/

Projekt byl strukturován a rozdělen do několika složek: 

- `data` obsahuje soubor s daty využívanými pro vizualizaci
- `src` obsahuje zdrojové kódy aplikace, hlavní složka
    - `assets` obsahuje css styly 
    - `pages` obsahuje jednolivé stránky aplikace se zdrojovými kódy
    - `utils` obsahuje pomocné funkce

## Dokumentace 

Dokumentace je vygenerována za pomocí balíčku `pdoc` a v projektu je uchována v rámci složky `docs`.

## Instalace 

Pro instalaci je potřeba v rámci kořenové složky vytvořit a aktivovat virtuální prostředí, tj.: 

Linux/Mac:

```bashvirtualenv venv
virtualenv venv
source venv/bin/activate
pip3 install -e .
```

Windows: 
```powershell
virtualenv venv
venv\Scripts\activate
pip install -e .
```

## Použité nástroje

Mezi využívané balíčky patří: 

- `dash 2.18.2`
- `pandas 2.2.1`
- `dash-bootstrap-components 1.6.1rc2`
- `plotly 6.0.0rc0`
- `numpy 1.26.4`