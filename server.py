import http.server
import socketserver
import urllib.request
import json
import ssl

PORT = 8000

class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # 當前端請求 /api/cctv 時，由 Python 後端代為抓取，完美解決瀏覽器 CORS 阻擋
        if self.path == '/api/cctv':
            url = "https://thbapp.thb.gov.tw/services/cctv/thb"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            
            # 忽略 Mac 的 SSL 憑證驗證，確保 100% 能通訊
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            
            try:
                with urllib.request.urlopen(req, context=ctx) as response:
                    data = response.read()
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(data)
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        else:
            # 其它請求則回傳靜態網頁（如 index.html）
            super().do_GET()

# 避免本機 Port 被佔用鎖死
socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), ProxyHandler) as httpd:
    print(f"✅ 專屬中繼伺服器已啟動！")
    print(f"👉 請在 Chrome 瀏覽器開啟： http://localhost:{PORT}")
    httpd.serve_forever()