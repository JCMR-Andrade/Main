from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pandas as pd
import os

# Se modificar esses escopos, delete o arquivo token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# O ID da planilha de exemplo.
SAMPLE_SPREADSHEET_ID = ''

def authenticate():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def main():
    creds = authenticate()
    try:
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()

        # Lê os dados da planilha
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='').execute()
        values = result.get('values', [])

        if not values:
            print('Nenhum dado encontrado.')
            return

        # Obtém o cabeçalho
        header = values[0]
        num_columns = len(header)

        # Ajusta o número de colunas em cada linha de dados
        adjusted_values = []
        for row in values[1:]:
            if len(row) < num_columns:
                row.extend([''] * (num_columns - len(row)))  # Adiciona colunas vazias
            elif len(row) > num_columns:
                row = row[:num_columns]  # Trunca colunas extras
            adjusted_values.append(row)

        # Converte os dados ajustados para um DataFrame do pandas
        df = pd.DataFrame(adjusted_values, columns=header)

        # Salva o DataFrame como um arquivo Excel
        df.to_excel(' .xlsx', index=False)
        print('Arquivo Excel salvo com sucesso!')

    except TypeError as err:
        print(err)

if __name__ == '__main__':
    main()
print('Fim')
