from flask import Flask, request, render_template, session
import requests
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Define the URLs for the other services
addition_url = "http://10.35.64.88:5001/add"
multiplication_url = "http://10.35.64.88:5002/multiply"

# Initialize tracer provider
trace.set_tracer_provider(
    TracerProvider(resource=Resource.create({SERVICE_NAME: "my-service"}))
)
tracer = trace.get_tracer(__name__)

# Create a JaegerExporter
jaeger_exporter = JaegerExporter(
    agent_host_name="10.35.64.88",
    agent_port=6831,
)
span_processor = BatchSpanProcessor(jaeger_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

@app.route('/', methods=['GET', 'POST'])
def index():
    add_result = session.get('add_result')
    multiply_result = session.get('multiply_result')

    if request.method == 'POST':
        num1 = int(request.form['num1'])
        num2 = int(request.form['num2'])

        with tracer.start_as_current_span("getting results"):
            with tracer.start_as_current_span("sending to services"):
                # Request addition result
                add_result = requests.post(addition_url, json={"num1": num1, "num2": num2}).json()

                # Request multiplication result
                multiply_result = requests.post(multiplication_url, json={"num1": num1, "num2": num2}).json()

        # Store results in session
        session['add_result'] = add_result['result']
        session['multiply_result'] = multiply_result['result']
        print(add_result)

        return render_template('index.html', add_result=add_result['result'], multiply_result=multiply_result['result'])

    return render_template('index.html', add_result=add_result, multiply_result=multiply_result)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
