from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    pay = request.args.get('payload','')
    return render_template_string('%s'% (pay))

app.run()
