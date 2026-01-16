from http.server import BaseHTTPRequestHandler
import json
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_sheets_client():
    """Inicializa cliente do Google Sheets"""
    creds_json = os.environ.get('SHEETS_CREDENTIALS')
    if not creds_json:
        raise Exception("SHEETS_CREDENTIALS não configurada")
    
    creds_dict = json.loads(creds_json)
    scopes = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scopes)
    return gspread.authorize(creds)


def converter_valor(valor, tipo):
    """Converte valor para o tipo especificado"""
    if valor is None or valor == "":
        return 0
    
    valor_str = str(valor).strip()
    
    if tipo == "int":
        try:
            valor_limpo = valor_str.replace('R$', '').replace(' ', '').replace(',', '.')
            return int(float(valor_limpo))
        except:
            return 0
    elif tipo == "float":
        try:
            valor_limpo = valor_str.replace('R$', '').replace(' ', '').replace(',', '.').replace('-', '')
            return float(valor_limpo)
        except:
            return 0
    else:
        return valor_str


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Lista todas as faturas da planilha"""
        try:
            client = get_sheets_client()
            spreadsheet_id = os.environ.get('SHEETS_SPREADSHEET_ID', 'GESTÃO FORZA')
            
            planilha = client.open(title=spreadsheet_id)
            aba = planilha.worksheet("Forza Informações da fatura")
            
            # Pegar todos os dados
            dados = aba.get_all_values()
            
            faturas = []
            for i, row in enumerate(dados[1:], start=2):  # Pular cabeçalho
                if len(row) >= 24:
                    fatura = {
                        "id": f"row_{i}",
                        "vencimento": row[0] if len(row) > 0 else "",
                        "diasLeitura": converter_valor(row[1], "int") if len(row) > 1 else 0,
                        "energiaInjetada": converter_valor(row[2], "float") if len(row) > 2 else 0,
                        "saldoUtilizado": converter_valor(row[3], "float") if len(row) > 3 else 0,
                        "saldoAtualizado": converter_valor(row[4], "float") if len(row) > 4 else 0,
                        "totalPagar": converter_valor(row[5], "float") if len(row) > 5 else 0,
                        "consumoKwh": converter_valor(row[9], "float") if len(row) > 9 else 0,
                        "unidadeConsumidora": row[23] if len(row) > 23 else "",
                        "numeroCliente": row[24] if len(row) > 24 else "",
                        "status": "concluido",
                        "createdAt": ""
                    }
                    faturas.append(fatura)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(faturas).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
    
    def do_POST(self):
        """Insere nova fatura na planilha"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            fatura = json.loads(post_data)
            
            client = get_sheets_client()
            spreadsheet_id = os.environ.get('SHEETS_SPREADSHEET_ID', 'GESTÃO FORZA')
            
            planilha = client.open(title=spreadsheet_id)
            aba = planilha.worksheet("Forza Informações da fatura")
            
            # Montar linha de dados
            tipos = {
                "1": "text", "2": "int", "3": "float", "4": "float", "5": "float",
                "6": "float", "7": "text", "8": "text", "9": "text", "10": "float",
                "11": "float", "12": "float", "13": "float", "14": "float",
                "15": "float", "16": "float", "17": "float", "18": "float",
                "19": "float", "20": "float", "21": "float", "22": "float",
                "23": "float", "24": "text"
            }
            
            valores = [
                fatura.get('vencimento', ''),
                fatura.get('diasLeitura', 0),
                fatura.get('energiaInjetada', 0),
                fatura.get('saldoUtilizado', 0),
                fatura.get('saldoAtualizado', 0),
                fatura.get('totalPagar', 0),
                fatura.get('leituraAnteriorData', ''),
                fatura.get('leituraAtualData', ''),
                fatura.get('proximaLeituraData', ''),
                fatura.get('consumoKwh', 0),
                fatura.get('leituraAtual', 0),
                fatura.get('leituraAnterior', 0),
                fatura.get('energiaAtivaTE', 0),
                fatura.get('energiaAtivaTUSD', 0),
                fatura.get('energiaInjetadaTE', 0),
                fatura.get('energiaInjetadaTUSD', 0),
                fatura.get('bandeiraAmarelaComp', 0),
                fatura.get('bandeiraVermelhaComp', 0),
                fatura.get('bandeiraAmarela', 0),
                fatura.get('bandeiraVermelha', 0),
                fatura.get('iluminacaoPublica', 0),
                fatura.get('valoresNegativos', 0),
                fatura.get('valoresPositivos', 0),
                fatura.get('unidadeConsumidora', ''),
                fatura.get('numeroCliente', '')
            ]
            
            # Encontrar próxima linha vazia
            coluna = aba.col_values(15)
            proxima_linha = len(coluna) + 1
            
            # Inserir dados
            aba.update(f'O{proxima_linha}:AK{proxima_linha}', [valores[:23]])
            aba.update(f'AZ{proxima_linha}:BA{proxima_linha}', [[valores[23], 0]])
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "row": proxima_linha}).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
