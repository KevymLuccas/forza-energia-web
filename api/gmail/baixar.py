from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Baixa faturas do Gmail (placeholder - requer OAuth no frontend)"""
        try:
            # Esta função requer autenticação OAuth do usuário
            # No Vercel, é melhor implementar OAuth no frontend
            # e passar o token para o backend
            
            response_data = {
                "success": True,
                "message": "Para baixar faturas do Gmail, configure a autenticação OAuth no frontend",
                "total": 0,
                "novos": 0,
                "processados": 0
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
