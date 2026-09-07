## Unity MCP Server

Proyecto gestionado con [uv](https://docs.astral.sh/uv/) y el SDK oficial de Python para MCP.

### Requisitos

- Python 3.11 (la versión se fija en `.python-version`).
- `uv` instalado.

### Preparación

```bash
cp .env.example .env
uv sync
```

Esto crea o actualiza `.venv` a partir de `pyproject.toml` y `uv.lock`; no hace falta activar el entorno manualmente.

Edita `.env` si Unity escucha en otro host o puerto. El fichero real se ignora por Git.

### Ejecución

Con Unity escuchando en `127.0.0.1:8765`, inicia el servidor MCP HTTP en `127.0.0.1:3001` con:

```bash
uv run tfg-sergio-v2-mcp-server
```

Para ejecutar herramientas dentro del entorno, antepone `uv run`, por ejemplo `uv run python -m pytest`.
