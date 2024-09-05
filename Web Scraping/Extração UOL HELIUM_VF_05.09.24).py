from helium import start_chrome, find_all, S

# Inicia o navegador e navega até o site do UOL
drive = start_chrome('https://pt.dotabuff.com/players/36423302/matches?enhance=overview', headless=True)


# Encontra todos os elementos que contêm os links e títulos das matérias
email_cells = find_all(S("table > tr > td", below="section"))
emails = [cell.web_element.text for cell in email_cells]

print(emails)

# # Filtra e exibe os links e títulos
# for article in articles:
#     title = article.web_element.text
#     link = article.web_element.get_attribute('href')
#     if title and link:
#         print(f'Título: {title}\nLink: {link}\n')
