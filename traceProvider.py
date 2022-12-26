from opentelemetry import trace
# from opentelemetry.exporter.zipkin.proto.http import ZipkinExporter
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource


resource = Resource(attributes={
    SERVICE_NAME: "client/server App"
})

# zipkinExporter = ZipkinExporter(endpoint="http://localhost:9411/api/v2/spans")

jaegarExporter = JaegerExporter(agent_host_name="localhost", agent_port=6831)

provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(jaegarExporter)
provider.add_span_processor(processor)

# Sets the global default tracer provider
trace.set_tracer_provider(provider)

# Creates a tracer from the global tracer provider
tracer = trace.get_tracer(__name__)