from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from api import admin, chat, feedback

app = FastAPI(
    title="CosmosLine Barry Chatbot DS API",
    description="API for the Barry chatbot, an e-commerce petroleum product knowledgebase.",
    version="1.0.0"
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        openapi_version=app.openapi_version,
        description=app.description,
        routes=app.routes,
    )
    # Fix Swagger UI bug with file arrays in OpenAPI 3.1.0
    for schemas in openapi_schema.get("components", {}).get("schemas", {}).values():
        for prop in schemas.get("properties", {}).values():
            if prop.get("type") == "array" and prop.get("items", {}).get("contentMediaType") == "application/octet-stream":
                prop["items"].pop("contentMediaType", None)
                prop["items"]["format"] = "binary"
                
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(feedback.router, prefix="/feedback", tags=["Feedback"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the CosmosLine Barry Chatbot DS API"}
