import uvicorn
from fastapi import FastAPI
from .api import router, init_cors
from .db import Base, engine


def create_app():
    app = FastAPI(title='Agentic Support RAG')
    Base.metadata.create_all(bind=engine)
    init_cors(app)
    app.include_router(router, prefix='/api')

    @app.get('/health')
    def health_check():
        return {'status': 'ok'}

    return app


app = create_app()


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000, reload=True)
