from dotenv import load_dotenv
import xml.etree.ElementTree as ET
import psycopg as pg
import os


load_dotenv()

def connectDatabase():
    try:
        conn = pg.connect(host=os.getenv('HOST'),
                          user=os.getenv('USER'),
                          password=os.getenv('PASS'),
                          dbname=os.getenv('DATABASE'))
        return conn

    except pg.Error as e:
        print("Error: ", e)

def listXmlFiles(folder='xml'):
    path = [os.path.join(folder, name) for name in os.listdir(folder)]
    files = [arq for arq in path if os.path.isfile(arq)]
    xmlfiles = [arq for arq in files if arq.lower().endswith(".xml")]
    return xmlfiles

def listSqlFiles(folder='schemas'):
   sqlfiles = [os.path.join(folder,f) for f in os.listdir(folder) if f.endswith('.sql')]
   return sqlfiles

def createTables():
    try:
        for file in listSqlFiles():
            with open(file, 'r') as content:
                script_sql = content.read()

            # Executa o script SQL no banco de dados
            with conn.cursor() as cursor:
                cursor.execute(script_sql)
                print(f"Tabela do arquivo {file} criadas com sucesso.")

        # Confirma as alterações no banco de dados
        conn.commit()
        createFK()

    except (Exception, pg.Error) as error:
        print(f"Erro ao processar os scripts SQL: {error}")
        conn.rollback()


def createFK():
    try:
        for file in listSqlFiles('schemas\\FK'):
            with open(file, 'r') as content:
                script_sql = content.read()

            # Executa o script SQL no banco de dados
            with conn.cursor() as cursor:
                cursor.execute(script_sql)
                print(f"Arquivo {file} executado com sucesso.")

        # Confirma as alterações no banco de dados
        conn.commit()

    except (Exception, pg.Error) as error:
        print(f"Erro ao processar os scripts SQL: {error}")
        conn.rollback()


def getTableKeys(table):
    """Return an array of the keys for a given table"""
    keys = None
    if table == "Users":
        keys = [
            "Id",
            "Reputation",
            "CreationDate",
            "DisplayName",
            "LastAccessDate",
            "WebsiteUrl",
            "Location",
            "AboutMe",
            "Views",
            "UpVotes",
            "DownVotes",
            "ProfileImageUrl",
            "Age",
            "AccountId",
        ]
    elif table == "Badges":
        keys = ["Id", "UserId", "Name", "Date"]
    elif table == "PostLinks":
        keys = ["Id", "CreationDate", "PostId", "RelatedPostId", "LinkTypeId"]
    elif table == "Comments":
        keys = ["Id", "PostId", "Score", "Text", "CreationDate", "UserId"]
    elif table == "Votes":
        keys = ["Id", "PostId", "VoteTypeId", "UserId", "CreationDate", "BountyAmount"]
    elif table == "Posts":
        keys = [
            "Id",
            "PostTypeId",
            "AcceptedAnswerId",
            "ParentId",
            "CreationDate",
            "Score",
            "ViewCount",
            "Body",
            "OwnerUserId",
            "LastEditorUserId",
            "LastEditorDisplayName",
            "LastEditDate",
            "LastActivityDate",
            "Title",
            "Tags",
            "AnswerCount",
            "CommentCount",
            "FavoriteCount",
            "ClosedDate",
            "CommunityOwnedDate",
        ]
    elif table == "Tags":
        keys = ["Id", "TagName", "Count", "ExcerptPostId", "WikiPostId"]
    elif table == "PostHistory":
        keys = [
            "Id",
            "PostHistoryTypeId",
            "PostId",
            "RevisionGUID",
            "CreationDate",
            "UserId",
            "Text",
        ]
    elif table == "Comments":
        keys = ["Id", "PostId", "Score", "Text", "CreationDate", "UserId"]
    return keys


def processXml(path):
    cursor = conn.cursor()
    table = os.path.splitext(os.path.basename(path))[0]
    cursor.execute(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE")
    count = 0
    fields = getTableKeys(table)
    if not fields:
        raise ValueError(f"Tabela '{table}' não possui campos definidos em getTableKeys.")

    try:
        for event, elem in ET.iterparse(path, events=('end',)):
            if elem.tag == 'row':  # Cada elemento <row> é um registro
                # Extrai os atributos do elemento <row>
                data = {k: v for k, v in elem.attrib.items() if k in fields}
                # Gera os nomes e valores para a inserção
                columns = ', '.join(data.keys())
                values = ', '.join(['%s'] * len(data))
                query = f"INSERT INTO {table} ({columns}) VALUES ({values})"

                count+=1
                # Executa a inserção
                cursor.execute(query, list(data.values()))

                # Libera memória do elemento processado
                elem.clear()
                # Confirma as alterações no banco de dados
        conn.commit()
        print(f"{count} Dados do arquivo {path} inseridos com sucesso na tabela {table}.")

    except Exception as e:
        print(f"Erro ao processar o arquivo {path}: {e}")
        conn.rollback()

if __name__ == '__main__':
    conn = connectDatabase()
    createTables()
    xmlFiles = listXmlFiles()
    #for files in xmlFiles:
    #    processXml(files)

