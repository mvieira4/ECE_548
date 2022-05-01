import WSN
from dash import Dash, html
import dash_cytoscape as cyto

# Initialize network
net = WSN.wsn()


net.add_nodes(200)    

net._set_neighbors()

net.run()

elements = net.gen_elements()

my_stylesheet = [
    # Group selectors
    {
        'selector': 'node', 
        'style': { 
            'content': 'data(l)' 
        }
    },
    
    {
        'selector': 'edge',
        'style': {
            'curve-style': 'bezier',
            'target-arrow-shape': 'vee'
        }
    },

    # Class selectors
    {
        'selector': '[network = 0]', 
        'style': {
            'background-color': 'cyan'
        }
    },
    {
        'selector': '[network = 1]',
        'style': {
            'background-color': 'orange'
        }
    },
    {
        'selector': '[role = 0]', 
        'style': {
            'shape': 'triangle',
            'background-color': 'blue'
        }
    },
    {
        'selector': '[role = 1]',
        'style': {
            'shape': 'triangle',
            'background-color': 'red'
        }
    }
    
]

app = Dash(__name__)
app.layout = html.Div([
    html.P("Dash Cytoscape:"),
    cyto.Cytoscape(
        id='cytoscape',
        elements=elements,
        layout={'name': 'preset'},
        style={'width': '100%', 'height': '700px'},
        stylesheet=my_stylesheet
    )
])


app.run_server(debug=True)