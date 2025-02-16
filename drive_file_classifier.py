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
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
FOLDER_ID = config['FOLDER_ID']
SUBFOLDERS = config['SUBFOLDERS']
PASTA_DUPLICADOS = config['PASTA_DUPLICADOS']
KEYWORDS = config['KEYWORDS']
IGNORED_WORDS = config['PALAVRAS_IGNORADAS']

# Função para listar arquivos do Google Drive com paginação
def list_drive_files():
    # Autenticação na API do Google Drive
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    service = build('drive', 'v3', credentials=creds)

    all_files = []
    page_token = None
    while True:
        results = service.files().list(
            q=f"'{FOLDER_ID}' in parents",
            fields="nextPageToken, files(id, name, mimeType, size, createdTime, modifiedTime, webViewLink, webContentLink)",
            pageSize=100,
            pageToken=page_token
        ).execute()
        files = results.get('files', [])
        all_files.extend(files)
        page_token = results.get('nextPageToken')
        if not page_token:
            break
    return all_files

# Salvar a lista de arquivos em CSV
def save_file_list_csv(files, filename):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Nome", "Tipo", "Tamanho (bytes)", "Criado em", "Modificado em", "Link de Visualização", "Link de Download"])
        for file in files:
            writer.writerow([
                file.get("id", "N/A"),
                file.get("name", "N/A"),
                file.get("mimeType", "N/A"),
                file.get("size", "N/A"),
                file.get("createdTime", "N/A"),
                file.get("modifiedTime", "N/A"),
                file.get("webViewLink", "N/A"),
                file.get("webContentLink", "N/A")
            ])
    print(f"Lista salva em '{filename}'")

# Função para identificar duplicatas
def identify_duplicates(input_csv, output_csv):
    file_size_dict = defaultdict(list)
    duplicates = []
    with open(input_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            size = row["Tamanho (bytes)"]
            name = name_cleaner(row["Nome"].lower())
            file_size_dict[size].append((row["Nome"],name, row["ID"], row["Tamanho (bytes)"]))
    
    for size, files in file_size_dict.items():
        if len(files) > 1:
            files.sort(key=lambda x: x[1])  # Ordenar pelo nome normalizado
            for i in range(len(files) - 1):
                name1, name_cleaned1, id1, size1 = files[i]
                name2, name_cleaned2, id2, size2 = files[i + 1]
                if (int(size1)-int(size2)>50) or (int(size1)-int(size2)<50):
                    # Se os nomes forem muito parecidos, marcar como duplicata
                    if name_cleaned1 in name_cleaned2 or name_cleaned2 in name_cleaned1:
                        duplicates.append([id1, name1, size1, "Sim", id2])
    
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Nome", "Tamanho (bytes)", "Possível Duplicado", "Duplicado De"])
        writer.writerows(duplicates)
    print(f"Relatório de duplicatas salvo em '{output_csv}'")

def name_cleaner(name):
    nome = name.lower().strip()  # Converter para minúsculas e remover espaços extras
    nome = re.sub(r"\(\d+\)", "", nome)  # Remover números entre parênteses (ex: "Livro (2)")
    nome = re.sub(r"[-_]", " ", nome)  # Substituir traços e underscores por espaços
    nome = re.sub(r"\s+", " ", nome)  # Substituir múltiplos espaços por um único
    nome = re.sub(r"(\w+)pdf", r"\1", nome)  # Corrigir "vidapdf" → "vida"
    nome = re.sub(r"\bpdf\b", "", nome)  # Remover "pdf" solto no final
    words = nome.split()  # Separar words
    
    # Remover palavras comuns
    words = [p for p in words if p not in IGNORED_WORDS]
    
    return " ".join(words).strip()  # Juntar as palavras de volta

# Função para classificar os arquivos
def classify_files(input_csv, output_csv):
    with open(input_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        classified_files = []
        
        for row in reader:
            name = name_cleaner(row["Nome"].lower())
            subdirectory = "Outros"
            for category, keywords in KEYWORDS.items():
                if any(keyword in name for keyword in keywords):
                    subdirectory = category
                    break
            
            row["SubDiretório"] = subdirectory
            classified_files.append(row)
    
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(classified_files[0].keys()))
        writer.writeheader()
        writer.writerows(classified_files)
    print(f"Arquivos classificados salvos em '{output_csv}'")

# Executar as funções principais
if __name__ == "__main__":
    file_list = list_drive_files()
    csv_file = "csv_files/lista_completa_arquivos.csv"
    duplicates_csv = "csv_files/possiveis_duplicatas.csv"
    classified_csv = "csv_files/arquivos_classificados.csv"
    
    save_file_list_csv(file_list, csv_file)
    identify_duplicates(csv_file, duplicates_csv)
    classify_files(csv_file, classified_csv)
