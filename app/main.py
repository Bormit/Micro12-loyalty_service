from fastapi import FastAPI, HTTPException
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from pydantic import BaseModel

class CreateLoyaltyModel(BaseModel):
    status: str
    nameLoyalty: str

class Loyalty:
    def __init__(self, id: int, status: str, nameLoyalty: str):
        self.id = id
        self.status = status
        self.nameLoyalty = nameLoyalty

loyaltyList: list[Loyalty] = [
    # Loyalty(0, 'Активно', 'Скидка %30 на бытовую технику'),
    # Loyalty(1, 'Использовано', 'Скидка %15 на электронику'),
    # Loyalty(2, 'Срок действия истек', 'Скидка %10 на продуктовые товары')
]

def add_loyalties(content: CreateLoyaltyModel):
    id = len(loyaltyList)
    loyaltyList.append(Loyalty(id, content.status, content.nameLoyalty))
    return id

app = FastAPI()

#######
# Jaeger

from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

resource = Resource(attributes={
    SERVICE_NAME: "loyalty_service"
})

jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger",
    agent_port=6831,
)

provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(jaeger_exporter)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

FastAPIInstrumentor.instrument_app(app)

#
#######

#######
#Prometheus

from prometheus_fastapi_instrumentator import Instrumentator

@app.on_event("startup")
async def startup():
    Instrumentator().instrument(app).expose(app)

#
#######


@app.get("/v1/loyalties")
async def get_loyalties():
    return loyaltyList

@app.post("/v1/loyalties")
async def add_loyalty(content: CreateLoyaltyModel):
    add_loyalties(content)
    return loyaltyList[-1]

@app.get("/v1/loyalties/{id}")
async def get_loyalties_by_id(id: int):
    result = [item for item in loyaltyList if item.id == id]
    if len(result) > 0:
        return result[0]
    else:
        raise HTTPException(status_code=404, detail="Loyalties not found")

@app.get("/__health")
async def check_service():
    return