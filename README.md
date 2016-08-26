# dj-export

Testes para exportar dados do Django.

Inicialmente estou usando o [django-import-export](https://github.com/django-import-export/django-import-export) para exportar dados do Django e fazer alguns testes. O [django-import-export](https://github.com/django-import-export/django-import-export) trabalha no Admin.

Meu objetivo é implementar para que seja possível exportar a partir de um template.

## Como desenvolver?

1. Clone o repositório
2. Crie um virtualenv com Python 3.5
3. Ative o virtualenv.
4. Instale as dependências.
5. Configure a instância com o .env
6. Execute os testes.
7. Rode a aplicação.

```bash
git clone https://github.com/rg3915/dj-export.git
cd dj-export
python -m venv .venv
source .venv/bin/activate # Linux
pip install -r requirements.txt
cp contrib/env-sample .env
python manage.py test
python manage.py runserver
```

