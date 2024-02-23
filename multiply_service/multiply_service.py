from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/multiply', methods=['POST'])
def multiply():
    data = request.json
    num1 = data['num1']
    num2 = data['num2']
    result = num1 * num2
    print(result)
    print(f"{jsonify(result=result)} hello")
    return jsonify(result=result)

if __name__ == '__main__':
    app.run(port=5002,host='0.0.0.0')
