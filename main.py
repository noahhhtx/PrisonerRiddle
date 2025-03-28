import base64
from flask import Flask, request, render_template, Response
import puzzle_solver as ps
from matplotlib.figure import Figure
from io import BytesIO

app = Flask(__name__)

def result(x, y, prob):

    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)

    axis.axhline(y=prob, color='r')
    axis.plot(x, y)

    fig.supxlabel("Number of Simulations")
    fig.supylabel("Rate of Success")

    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)

    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img class='center' src='data:image/png;base64,{data}'/>"

@app.route("/")
def home():
    html = render_template("home.html")
    html += "</body> </html>"
    return html

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/sim", methods =["POST"])
def sim():
    html = render_template("home.html")

    prisoners = int(request.form.get("prisoners"))
    simulations = int(request.form.get("simulations"))

    suboptimal_probability = ps.computeSuboptimalProbability(prisoners)
    optimal_probability = ps.computeOptimalProbability(prisoners)

    x = [i for i in range(1, simulations + 1)]
    y = ps.simulation(prisoners, simulations)

    html += '''
    
    <br>
    
    <h2 class="center">Results</h2>
    
    '''

    html += f"<p class='center'>Suboptimal Probability of Success for {prisoners} Prisoners: {suboptimal_probability} percent</p>"
    html += f"<p class='center'>Optimal Probability of Success for {prisoners} Prisoners: {optimal_probability} percent</p>"
    html += f"<p class='center'>Rate of Success After {simulations} Simulations: {y[-1]} percent</p>"

    html += result(x, y, optimal_probability)

    html += '''
    
    <br>
    
    <h2 class="center">Detailed Results</h2>
    
    <table id="results">
    
    <tr>
        <th>Number of Simulations</th>
        <th>Rate of Success</th>
    </tr>
    
    '''

    for i in range(len(x)):
        html += "<tr>"
        html += f"<td>{x[i]}</td><td>{y[i]}</td>"
        html += "</tr>\n"

    html += "</table>"

    html += "</body> </html>"
    return html