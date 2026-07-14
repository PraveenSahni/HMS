curl -s -w "\nHTTP:%{http_code}\n" -X POST http://127.0.0.1/api/tryton/ -H "Content-Type: application/json" -d "{\"id\":1,\"method\":\"common.db.list\",\"params\":[]}"
echo "===="
curl -s -w "\nHTTP:%{http_code}\n" -X POST http://127.0.0.1:8000/ -H "Content-Type: application/json" -d "{\"id\":1,\"method\":\"common.db.list\",\"params\":[]}" 2>/dev/null || true
echo "===="
curl -s -w "\nHTTP:%{http_code}\n" -X POST http://127.0.0.1:8000/gnuhealth/ -H "Content-Type: application/json" -d "{\"id\":2,\"method\":\"common.db.login\",\"params\":[\"admin\",\"IstHealth@2026!Admin\"]}" 2>/dev/null || true
ss -tlnp | head -30
