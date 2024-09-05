from helium import *

drive = helium.start_chrome('uol.com.br', headless=True)

# Encontra todos os elementos que contêm os links e títulos das matérias
articles = find_all(S('a'))

# Filtra e exibe os links e títulos
for article in articles:
    title = article.web_element.text
    link = article.web_element.get_attribute('href')
    if title and link:
        print(f'Título: {title}\nLink: {link}\n')


kill_browser()
