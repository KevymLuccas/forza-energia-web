from http.server import BaseHTTPRequestHandler
import json
import os
import base64
import tempfile
from google import genai
from google.genai import types

# Prompt para extração
PROMPT_EXTRACAO = """Gostaria que você lesse pdf retirasse algumas informação que direi logo abaixo, mas antes gostaria de lhe dizer como gostaria que você entregasse as informações:
vou lhe passar itens de informações a serem colhidas documento e as respostas devem ser entregues em formato JSON, as chaves são a numeração dos itens e os valores são as informações encontradas.
Lembrando também que a resposta que forem números separe os decimais com uma virgula.
items a serem buscados:
1. próximo ao cabeçalho, busque o valor do vencimento da fatura
2. na aba DATAS DE LEITURA, busque a informação Nº DE DIAS
3. na aba MENSAGENS IMPORTANTES, busque os kwh medidos sobre ˜Energia Injetada HFP no mês˜
4. na aba MENSAGENS IMPORTANTES, busque os kwh medidos sobre ˜Saldo utilizado no mês˜
5. na aba MENSAGENS IMPORTANTES, busque os kwh medidos sobre ˜Saldo atualizado˜
6. ao lado do vencimento busque o valor ˜total a pagar˜
7. na aba DATAS DA LEITURA busque a data da LEITURA ANTERIOR
8. na aba DATAS DA LEITURA busque a data da LEITURA ATUAL
9. na aba DATAS DA LEITURA busque a data da PRÓXIMA LEITURA
10. na aba DADOS DE MEDIÇÃO busque o valor CONSUMO KWH
11. na aba DADOS DE MEDIÇÃO busque o valor LEITURA ATUAL
12. na aba DADOS DE MEDIÇÃO busque o valor LEITURA ANTERIOR
13. na aba DESCRIÇÃO DO FATURAMENTO busque o VALOR (R$) do item Energia Ativa Fornecida TE
14. na aba DESCRIÇÃO DO FATURAMENTO busque o VALOR (R$) do item Energia Ativa Fornecida TUSD
15. na aba DESCRIÇÃO DO FATURAMENTO busque os VALORES (R$) dos itens Energia Atv Inj TE oUC mPT
16. na aba DESCRIÇÃO DO FATURAMENTO busque os VALORES (R$) dos itens Energia Atv Inj TUSD oUC mPT
17. na aba DESCRIÇÃO DO FATURAMENTO busque o VALOR (R$) do item "Adicional Bandeira Amarela Comp."
18. na aba DESCRIÇÃO DO FATURAMENTO busque o VALOR (R$) do item Adicional Bandeira Vermelha Comp.
19. na aba DESCRIÇÃO DO FATURAMENTO busque o VALOR (R$) do item Adicional Bandeira Amarela
20. na aba DESCRIÇÃO DO FATURAMENTO busque o VALOR (R$) do item Adicional Bandeira Vermelha
21. na aba DESCRIÇÃO DO FATURAMENTO busque o VALOR (R$) do item CIP ILUM PUB PREF MUNICIPAL
22. na aba DESCRIÇÃO DO FATURAMENTO busque o somatório dos VALORES (R$) que são negativos e que não foram citados aqui.
23. na aba DESCRIÇÃO DO FATURAMENTO busque o somatório dos VALORES (R$) que são positivos e que não foram citados aqui.
24. na aba INSTALAÇÃO / UNIDADE CONSUMIDORA busque o valor
25. na aba N DO CLIENTE busque o valor de 8 digitos.

nos campos onde nao encontrar nenhum valor retorne 0.
ao final confira se realmente você está entregando os 25 itens que perguntei
revise e entregue todas as determinações exatamente da forma que pedi."""


def converter_para_fatura(dados_json):
    """Converte o JSON do Gemini para o formato da fatura"""
    return {
        "id": f"fat_{dados_json.get('25', 'unknown')}_{dados_json.get('1', 'unknown').replace('/', '-')}",
        "vencimento": dados_json.get("1", ""),
        "diasLeitura": int(dados_json.get("2", 0) or 0),
        "energiaInjetada": float(str(dados_json.get("3", 0)).replace(",", ".") or 0),
        "saldoUtilizado": float(str(dados_json.get("4", 0)).replace(",", ".") or 0),
        "saldoAtualizado": float(str(dados_json.get("5", 0)).replace(",", ".") or 0),
        "totalPagar": float(str(dados_json.get("6", 0)).replace(",", ".").replace("R$", "").strip() or 0),
        "leituraAnteriorData": dados_json.get("7", ""),
        "leituraAtualData": dados_json.get("8", ""),
        "proximaLeituraData": dados_json.get("9", ""),
        "consumoKwh": float(str(dados_json.get("10", 0)).replace(",", ".") or 0),
        "leituraAtual": float(str(dados_json.get("11", 0)).replace(",", ".") or 0),
        "leituraAnterior": float(str(dados_json.get("12", 0)).replace(",", ".") or 0),
        "energiaAtivaTE": float(str(dados_json.get("13", 0)).replace(",", ".") or 0),
        "energiaAtivaTUSD": float(str(dados_json.get("14", 0)).replace(",", ".") or 0),
        "energiaInjetadaTE": float(str(dados_json.get("15", 0)).replace(",", ".") or 0),
        "energiaInjetadaTUSD": float(str(dados_json.get("16", 0)).replace(",", ".") or 0),
        "bandeiraAmarelaComp": float(str(dados_json.get("17", 0)).replace(",", ".") or 0),
        "bandeiraVermelhaComp": float(str(dados_json.get("18", 0)).replace(",", ".") or 0),
        "bandeiraAmarela": float(str(dados_json.get("19", 0)).replace(",", ".") or 0),
        "bandeiraVermelha": float(str(dados_json.get("20", 0)).replace(",", ".") or 0),
        "iluminacaoPublica": float(str(dados_json.get("21", 0)).replace(",", ".") or 0),
        "valoresNegativos": float(str(dados_json.get("22", 0)).replace(",", ".") or 0),
        "valoresPositivos": float(str(dados_json.get("23", 0)).replace(",", ".") or 0),
        "unidadeConsumidora": dados_json.get("24", ""),
        "numeroCliente": dados_json.get("25", ""),
        "status": "concluido",
        "createdAt": ""
    }


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Ler o conteúdo do request
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Parse multipart form data (simplificado para base64)
            data = json.loads(post_data)
            pdf_base64 = data.get('file')
            
            if not pdf_base64:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Arquivo PDF não fornecido"}).encode())
                return
            
            # Decodificar PDF
            pdf_bytes = base64.b64decode(pdf_base64)
            
            # Salvar temporariamente
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
                tmp_file.write(pdf_bytes)
                tmp_path = tmp_file.name
            
            # Inicializar Gemini
            api_key = os.environ.get('GEMINI_API_KEY')
            if not api_key:
                raise Exception("GEMINI_API_KEY não configurada")
            
            client = genai.Client(api_key=api_key)
            
            # Upload do arquivo para Gemini
            pdf_file = client.files.upload(file=tmp_path)
            
            # Gerar resposta
            response = client.models.generate_content(
                model="gemini-2.5-pro",
                contents=[pdf_file, PROMPT_EXTRACAO],
                config={
                    "response_mime_type": "application/json",
                    "seed": 42
                }
            )
            
            # Parse da resposta
            dados_extraidos = json.loads(response.text)
            fatura = converter_para_fatura(dados_extraidos)
            
            # Limpar arquivo temporário
            os.unlink(tmp_path)
            
            # Retornar sucesso
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(fatura).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
