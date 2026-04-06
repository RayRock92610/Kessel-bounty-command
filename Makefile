setup:
	@echo "🛰️ Kessel Setup..."
	pkg install postgresql clang make libcrypt pkg-config libffi openssl-tool -y
	@if [ ! -d $$PREFIX/var/lib/postgresql ]; then initdb $$PREFIX/var/lib/postgresql; fi
	@pg_ctl -D $$PREFIX/var/lib/postgresql start || true
	export LDFLAGS="-L${PREFIX}/lib" && export CPPFLAGS="-I${PREFIX}/include" && pip install psycopg2 && pip install -r backend/requirements.txt
	PYTHONPATH=./backend python scripts/seed.py

start:
	@echo "🧹 Clearing the new line (8081)..."
	@fuser -k 8081/tcp || true
	@pg_ctl -D $$PREFIX/var/lib/postgresql start || true
	cd backend && PYTHONPATH=. python -m uvicorn app.main:app --host 127.0.0.1 --port 8081
