##### Versão em Português logo abaixo / Portuguese version below/
# 📌 Google Drive File Organizer

This repository contains two Python scripts to organize files on Google Drive:

1. **drive_file_classifier.py** → Lists Google Drive files, identifies duplicates, and classifies them based on keywords.
2. **drive_file_organizer.py** → Moves files to the correct folders based on the classification performed.

---

## 🛠️ Requirements

- Python **3.8 or higher**
- **Google Cloud** account with access to the Google Drive API
- JSON credential file from a Google Drive service account

### 📦 Install dependencies:

```sh
pip install google-auth google-auth-httplib2 google-api-python-client pyyaml
```

---

## 📂 Configuration

1. **Obtain your Google Drive credentials**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Enable the **Google Drive API**
   - Create **service account** credentials
   - Download the JSON file and save it in `secrets/`
2. **Get the Google Drive folder IDs**:
   - Open the folder in Google Drive
   - Copy the ID from the URL (example: `https://drive.google.com/drive/folders/FOLDER_ID_HERE`)
3. **Configure `config.yaml` in `secrets/`**:

```yaml
SERVICE_ACCOUNT_FILE: "your_credentials_file.json"
FOLDER_ID: "MAIN_FOLDER_ID"

SUBFOLDERS:
  Espiritismo e Religião: "SPIRITISM_FOLDER_ID"
  Autoajuda e Espiritualidade: "SELF_HELP_FOLDER_ID"
  Magia e Ocultismo: "MAGIC_FOLDER_ID"
  Filosofia e Conhecimento: "PHILOSOPHY_FOLDER_ID"
  Autores Populares: "POPULAR_AUTHORS_FOLDER_ID"
  Outros: "OTHER_FOLDER_ID"

PASTA_DUPLICADOS: "DUPLICATES_FOLDER_ID"

KEYWORDS:
  Espiritismo e Religião: ["espiritismo", "kardec", "mediunidade"]
  Autoajuda e Espiritualidade: ["vida", "amor", "luz"]
  Magia e Ocultismo: ["magia", "cabala", "umbanda"]
  Filosofia e Conhecimento: ["curso", "filosofia", "manual"]
  Autores Populares: ["xavier", "divaldo", "augusto"]
```

---

## 🚀 How to Use

### **1️⃣ List, detect duplicates, and classify files**

```sh
python drive_file_classifier.py
```

This will generate three CSV files inside the `csv_files/` folder:

- `lista_completa_arquivos.csv` → Lists all Google Drive files
- `possiveis_duplicatas.csv` → Contains identified duplicate files
- `arquivos_classificados.csv` → Files classified according to keywords

### **2️⃣ Move files to the correct folders**

```sh
python drive_file_organizer.py
```

This will move files to their respective directories in Google Drive, including the duplicates folder.

---

## 📌 Customization

- You can **modify or add keywords** in `config.yaml` to better organize files.
- To add new categories, simply include them in `KEYWORDS` and `SUBFOLDERS`.

---

## 📖 License

This project is distributed under the MIT license.


---
---
---

# 📌 Google Drive File Organizer

Este repositório contém dois scripts Python para organizar arquivos no Google Drive:

1. **drive\_file\_classifier.py** → Lista arquivos do Google Drive, identifica duplicatas e os classifica com base em palavras-chave.
2. **drive\_file\_organizer.py** → Move os arquivos para as pastas corretas conforme a classificação realizada.

---

## 🛠️ Requisitos

- Python **3.8 ou superior**
- Conta no **Google Cloud** com acesso à API do Google Drive
- Arquivo JSON de credenciais da conta de serviço do Google Drive

### 📦 Instalar dependências:

```sh
pip install google-auth google-auth-httplib2 google-api-python-client pyyaml
```

---

## 📂 Configuração

1. **Obtenha suas credenciais do Google Drive**:
   - Acesse [Google Cloud Console](https://console.cloud.google.com/)
   - Ative a **Google Drive API**
   - Crie credenciais de **conta de serviço**
   - Baixe o arquivo JSON e salve em `secrets/`
2. **Obtenha os IDs das pastas do Google Drive**:
   - Acesse a pasta no Google Drive
   - Copie o ID da URL (exemplo: `https://drive.google.com/drive/folders/PASTA_ID_AQUI`)
3. **Configure o `config.yaml` em `secrets/`**:

```yaml
SERVICE_ACCOUNT_FILE: "seu_arquivo_de_credenciais.json"
FOLDER_ID: "ID_DA_PASTA_PRINCIPAL"

SUBFOLDERS:
  Espiritismo e Religião: "ID_DA_PASTA_ESPIRITISMO"
  Autoajuda e Espiritualidade: "ID_DA_PASTA_AUTOAJUDA"
  Magia e Ocultismo: "ID_DA_PASTA_MAGIA"
  Filosofia e Conhecimento: "ID_DA_PASTA_FILOSOFIA"
  Autores Populares: "ID_DA_PASTA_AUTORES"
  Outros: "ID_DA_PASTA_OUTROS"

PASTA_DUPLICADOS: "ID_DA_PASTA_DUPLICADOS"

KEYWORDS:
  Espiritismo e Religião: ["espiritismo", "kardec", "mediunidade"]
  Autoajuda e Espiritualidade: ["vida", "amor", "luz"]
  Magia e Ocultismo: ["magia", "cabala", "umbanda"]
  Filosofia e Conhecimento: ["curso", "filosofia", "manual"]
  Autores Populares: ["xavier", "divaldo", "augusto"]
```

---

## 🚀 Como Usar

### **1️⃣ Listar, detectar duplicatas e classificar os arquivos**

```sh
python drive_file_classifier.py
```

Isso gerará três arquivos CSV dentro da pasta `csv_files/`:

- `lista_completa_arquivos.csv` → Lista todos os arquivos do Google Drive
- `possiveis_duplicatas.csv` → Contém os arquivos identificados como duplicados
- `arquivos_classificados.csv` → Arquivos classificados conforme as palavras-chave

### **2️⃣ Mover os arquivos para as pastas corretas**

```sh
python drive_file_organizer.py
```

Isso moverá os arquivos para seus respectivos diretórios dentro do Google Drive, incluindo a pasta de duplicados.

---

## 📌 Personalização

- Você pode **alterar ou adicionar palavras-chave** no `config.yaml` para organizar melhor os arquivos.
- Para adicionar novas categorias, basta incluí-las no `KEYWORDS` e no `SUBFOLDERS`.

---

## 📖 Licença

Este projeto é distribuído sob a licença MIT.

