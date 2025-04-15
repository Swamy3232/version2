import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pynvdrive
from pynvdrive.commands.settingsstates import GetSettingValue, GetSettingValues, SetSettingValue

app = dash.Dash(__name__)

# Setting ID for the sampling rate
SETTING_ID = '001.338.189'

# Available sampling rates
SAMPLING_RATES = [2048, 3200, 6400, 12800, 25600, 51200, 102400]

def get_current_sampling_rate():
    """Fetch the current sampling rate from pynvdrive."""
    with pynvdrive.Client() as client:
        try:
            cmd = GetSettingValue(idn=SETTING_ID)
            client.send_command(cmd)
            return cmd.value
        except:
            print(f"GetSettingValue error: {cmd.error}")
            return None

def set_sampling_rate(value):
    """Set the sampling rate in pynvdrive."""
    with pynvdrive.Client() as client:
        try:
            cmd = SetSettingValue(idn=SETTING_ID, value=value)
            client.send_command(cmd)
            print(f"Successfully set {SETTING_ID} to {value}")
        except:
            print(f"SetSettingValue error: {cmd.error}")

# Get the initial sampling rate
initial_sampling_rate = get_current_sampling_rate()

app.layout = html.Div([
    html.H2("Input Values Setting", style={'textAlign': 'center'}),
    
    html.Div([
        html.Label("Sampling Rate:", style={'fontSize': '16px', 'fontWeight': 'bold'}),
        dcc.Dropdown(
            id='sampling-rate-dropdown',
            options=[{'label': str(rate), 'value': rate} for rate in SAMPLING_RATES],
            value=initial_sampling_rate,  # Set default as the last selected value
            placeholder='Select Sampling Rate'
        )
    ], style={'width': '20%', 'margin': 'auto'}),
    
    html.Div(id='output-message', style={'marginTop': '20px', 'textAlign': 'center'})
])

@app.callback(
    Output('output-message', 'children'),
    Input('sampling-rate-dropdown', 'value')
)
def update_sampling_rate(selected_rate):
    if selected_rate:
        set_sampling_rate(selected_rate)
        return f"Sampling rate set to {selected_rate} Hz"
    return ""

if __name__ == '__main__':
    app.run_server(debug=True)