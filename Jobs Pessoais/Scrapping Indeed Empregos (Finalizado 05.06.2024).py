# -*- coding: utf-8 -*-
# Import necessary libraries
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
import datetime

# Set up Chrome options to customize the browser behavior
options = webdriver.ChromeOptions() 

# Set user-agent to mimic a browser behavior
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36')

# Initialize a Chrome WebDriver instance with customized options
driver = webdriver.Chrome(options=options) 

vaga = input(str('Qual o Cargo Procurado: '))

# URL of the webpage to scrape
url = f"https://br.indeed.com/jobs?q={vaga}&l=Grande%20S%C3%A3o%20Paulo%2C%20SP&sort=date"

# # URL of the webpage to scrape
# url = "https://br.indeed.com/jobs?q=analista&l=Grande%20S%C3%A3o%20Paulo%2C%20SP&sort=date"

# Open the URL in the Chrome WebDriver instance
driver.get(url)

# Sleep for 5 seconds to ensure the page loads completely before scraping
sleep(5)

# Get the HTML source code of the page after it has fully loaded
html = driver.page_source

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

def get_data(job_listing) -> tuple:
    # Extract job title
    title = job_listing.find("a").find("span").text.strip()
    
    try:
        link = job_listing.find("a", class_="jcs-JobTitle css-jspxzf eu4oa1w0")['href']
        link = ('https://br.indeed.com'+f'{link}')
    except AttributeError:
        link = ''
    
    
    # Extract company name if available, otherwise assign an empty string
    try:
        company = job_listing.find('span', class_='css-63koeb eu4oa1w0').text.strip()
    except AttributeError:
        company = ''
    
    # Extract job location if available, otherwise assign an empty string
    try:
        location  = job_listing.find('div', class_='css-1p0sjhy eu4oa1w0').text.strip()
    except AttributeError:
        location = ''
        
    # Extract salary information if available, otherwise assign an empty string
    try:
        salary  = job_listing.find('div', class_='metadata salary-snippet-container css-5zy3wz eu4oa1w0').text.strip()
    except AttributeError:
        salary = ''
    
    # Extract job type if available, otherwise assign an empty string
    try:
        job_type = job_listing.find('div', class_='metadata css-5zy3wz eu4oa1w0').text.strip()
    except AttributeError:
        job_type = ''
    
    # Extract date posted
    date_posted = job_listing.find('span', class_='css-qvloho eu4oa1w0').text.strip()
    date_posted = date_posted.split('d')
    date_posted = date_posted[1]
    
    # Extract job summary
    summary = job_listing.find('div', class_='css-9446fg eu4oa1w0').text.strip()
    
    # Return a tuple containing all the extracted information
    return (title, link, company, location, salary, job_type, date_posted, summary)

records = []

# Loop to scrape data from multiple pages until there are no more pages available
while True:
    try:
        # Extract the URL of the next page if available
        url = 'https://br.indeed.com/' + soup.find('a', {'aria-label':'Next Page'}).get('href')
    except AttributeError:
        # If there are no more pages available, break the loop
        break
    
    # Open the next page in the browser
    driver.get(url)
    
    # Get the HTML source code of the next page
    html = driver.page_source
    
    # Parse the HTML of the next page using BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find all job listings on the next page
    job_listings = soup.find_all('div', class_='job_seen_beacon') 

    # Iterate through each job listing on the page
    for job_listing in job_listings:
        # Extract data from the current job listing
        record = get_data(job_listing)
        
        # Append the extracted data to the records list
        records.append(record)

# Close the Chrome WebDriver instance
driver.quit()


agora = datetime.datetime.now().strftime("%d-%m-%Y, %H.%M")

# Convert list of records into a DataFrame
df = pd.DataFrame(records, columns=['Vaga', 'Link', 'Empresa', 'Cidade', 'Salário', 'Contratação', 'Data', 'Descrição'])

# Abra o arquivo CSV com codificação UTF-8 e modo de anexação ('a')
with open(f"Vagas_" + str(vaga) + "_Indeed (" + str(agora) + ").csv", 'a', encoding='latin-1') as f:
    # Salve o DataFrame no arquivo CSV
    df.to_csv(f"Vagas_" + str(vaga) + "_Indeed (" + str(agora) + ").csv", sep=';', index=False, encoding='latin-1', errors='ignore') 

print("Data saved to job_data.csv")
