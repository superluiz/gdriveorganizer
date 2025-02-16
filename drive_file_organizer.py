import csv
import re
import yaml
from googleapiclient.discovery import build
from google.oauth2 import service_account
from collections import defaultdict

# Carregar configurações do arquivo YAML
with open("secrets/config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

SERVICE_ACCOUNT_FILE = f"secrets/{config['SERVICE_ACCOUNT_FILE']}"
SCOPES = ['https://www.googleapis.com/auth/drive']
FOLDER_ID = config['FOLDER_ID']
SUBFOLDERS = config['SUBFOLDERS']
PASTA_DUPLICADOS = config['PASTA_DUPLICADOS']
KEYWORDS = config['KEYWORDS']

# Autenticação na API do Google Drive
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
service = build('drive', 'v3', credentials=creds)

# Função para mover arquivos no Google Drive
def move_file(file_id, destination_folder_id):
    try:
        file_metadata = service.files().get(fileId=file_id, fields="parents").execute()
        previous_parents = file_metadata.get("parents", [])
        
        service.files().update(
            fileId=file_id,
            addParents=destination_folder_id,
            removeParents=",".join(previous_parents),
            fields="id, parents"
        ).execute()
        print(f"✅ Arquivo {file_id} movido para {destination_folder_id}")
    except Exception as e:
        print(f"⚠ Erro ao mover {file_id}: {e}")

# Função para processar o CSV e mover os arquivos
def process_and_move_files(classified_csv):
    with open(classified_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        processed_files = set()
        
        for row in reader:
            file_id = row["ID"]
            subdirectory = row["SubDiretório"]
            duplicate = row.get("Possível Duplicado", "Não")
            reference_id = row.get("Duplicado De", "")
            
            if duplicate == "Sim":
                if reference_id not in processed_files:
                    move_file(reference_id, SUBFOLDERS.get(subdirectory, PASTA_DUPLICADOS))
                    processed_files.add(reference_id)
                move_file(file_id, PASTA_DUPLICADOS)
            else:
                move_file(file_id, SUBFOLDERS.get(subdirectory, PASTA_DUPLICADOS))

# Executar as funções principais
if __name__ == "__main__":
    classified_csv = "csv_files/arquivos_classificados.csv"
    process_and_move_files(classified_csv)
