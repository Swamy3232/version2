from dash import dcc, html, dash_table

  
CARD_STYLE = {
    'backgroundColor': 'white',
    'padding': '10px',
    'borderRadius': '5px',
    'boxShadow': '0px 4px 10px rgba(202, 22, 22, 0.1)',
    'marginBottom': '0px',
    'textAlign': 'center',
}

BUTTON_STYLE = {
    'margin': '10px',
    'padding': '8px 20px',
    'borderRadius': '5px',
    'border': 'none',
    'color': 'white',
    'cursor': 'pointer',
    'fontSize': '16px',
}

INPUT_STYLE = {
    'width': '80%',
    'padding': '12px 16px',
    'border': '1px solid #ccc',
    'borderRadius': '8px',
    'fontSize': '14px',
    'boxSizing': 'border-box',
    'marginBottom': '10px',
}
# Layout definition
from dash import dcc, html, dash_table

# ... (your existing styles and layout code)

# Layout definition
layout = html.Div(
    style={'textAlign': 'center', 'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#ECF0F1', 'padding': '20px'},
    children=[
        html.H1("🔧 Vibration Analyzer 📊", style={'color': '#2C3E50', 'marginBottom': '20px'}),

        # Page load trigger
        dcc.Interval(id="page-load-trigger", interval=500, n_intervals=0, max_intervals=1),

        # Machine details input
        html.Div(
            style={**CARD_STYLE, 'display': 'flex', 'flexWrap': 'wrap', 'gap': '20px', 'justifyContent': 'center'},
            children=[
                html.Div([ 
                    html.Label("Machine Name:", style={'fontSize': '16px', 'fontWeight': 'bold'}),
                    dcc.Dropdown(id='machine-id-dropdown', options=[], placeholder='Select Machine ID')
                ], style={'width': '22%'}),

                html.Div([ 
                    html.Label("Measurement Location:", style={'fontSize': '16px', 'fontWeight': 'bold'}),
                    dcc.Dropdown(id='meas-point-dropdown', options=[], placeholder='Select Measurement Point')
                ], style={'width': '22%'}),

                html.Div([ 
                    html.Label("Add the Remarks:", style={'fontSize': '16px', 'fontWeight': 'bold'}),
                    dcc.Input(id='remarks-point', type='text', placeholder='', style=INPUT_STYLE),
                ], style={'width': '22%'}),

                html.Div([ 
                    html.Label("Enter the RPM:", style={'fontSize': '16px', 'fontWeight': 'bold'}),
                   dcc.Input(id='rpm-input', type='text', placeholder='', style={'width': '150px', 'marginRight': '10px'}),
    html.Button('Submit', id='submit-btn', n_clicks=0),
    html.Div(id='output-rpm', style={'marginTop': '10px', 'fontSize': '16px'}),
   
dcc.Store(id='stored-rpm', data={}),

                ], style={'width': '22%'}),
            ]
        ),

        # Additional dropdowns for sensitivity, coupling, averages, and number of lines
        html.Div(
            style={**CARD_STYLE, 'display': 'flex', 'flexWrap': 'wrap', 'gap': '20px', 'justifyContent': 'center'},
            children=[
                # Sensitivity input text
                html.Div([
                    html.Label("Sensitivity:", style={'fontSize': '16px', 'fontWeight': 'bold'}),
                    dcc.Input(
                        id='sensitivity-input',
                        type='text',  # Restrict input to numbers
                        min=1,  # Minimum value
                        max=10,  # Maximum value
                        step=0.1,  # Allow decimal values
                        placeholder='Enter Sensitivity (v)/(m/s^2)',
                        style={'width': '100%'}
                    ),
                ], style={'width': '22%'}),

                html.Div([
                    html.Label("Sampling Rate:", style={'fontSize': '16px', 'fontWeight': 'bold'}),
                    dcc.Dropdown(
                        id='sampling-rate-dropdown',
                        options=[
                            {'label': '102.4 kS/s', 'value': 102400},
                            {'label': '65.536 kS/s', 'value': 65536},
                            {'label': '51.2 kS/s', 'value': 51200},
                            {'label': '32.768 kS/s', 'value': 32768},
                            {'label': '25.6 kS/s', 'value': 25600},
                            {'label': '16.384 kS/s', 'value': 16384},
                            {'label': '12.8 kS/s', 'value': 12800},
                            {'label': '8.192 kS/s', 'value': 8192},
                            {'label': '6.4 kS/s', 'value': 6400},
                            {'label': '5.12 kS/s', 'value': 5120},
                            {'label': '4.096 kS/s', 'value': 4096},
                            {'label': '3.2768 kS/s', 'value': 3276.8},
                            {'label': '3.2 kS/s', 'value': 3200},
                            {'label': '2.048 kS/s', 'value': 2048},
                        ],
                        placeholder='Select Sampling Rate',
                        style={'width': '100%'}
                    ),
                ], style={'width': '22%'}),

                # Coupling dropdown
                html.Div([
                    html.Label("Coupling:", style={'fontSize': '16px', 'fontWeight': 'bold'}),
                    dcc.Dropdown(
                        id='coupling-dropdown',
                        options=[
                            {'label': 'AC', 'value': 0},
                            {'label': 'DC', 'value': 1},
                            {'label': 'ICP', 'value': 2},
                            {'label': 'AC Floating', 'value': 3},
                            {'label': 'DC Floating', 'value': 4},
                            {'label': 'ICP TEDS', 'value': 7},
                        ],
                        placeholder='Select Coupling',
                        style={'width': '100%'}
                    ),
                ], style={'width': '22%'}),

                # Averages dropdown
                html.Div([
                    html.Label("Averages:", style={'fontSize': '16px', 'fontWeight': 'bold'}),
                    dcc.Dropdown(
                        id='averages-dropdown',
                        options=[{'label': str(i), 'value': i} for i in range(5, 26, 5)],  # 5, 10, 15, 20, 25
                        placeholder='Select Averages',
                        style={'width': '100%'}
                    ),
                ], style={'width': '22%'}),

                # Number of Lines dropdown
                html.Div([
                    html.Label("Number of Lines:", style={'fontSize': '16px', 'fontWeight': 'bold'}),
                    dcc.Dropdown(
                        id='lines-dropdown',
                        options=[{'label': str(i), 'value': i} for i in [101, 201, 401, 801, 1601, 3201, 6401, 12801, 25601]],
                        style={'width': '100%'}
                    ),
                ], style={'width': '22%'}),
            ]
        ),

        # Control Buttons
        html.Div(style=CARD_STYLE, children=[
            html.Button('▶ Start Measurement', id='run-button', n_clicks=0, style={**BUTTON_STYLE, 'backgroundColor': '#27AE60'}),
            html.Button('⏹ Stop Measurement', id='stop-button', n_clicks=0, style={**BUTTON_STYLE, 'backgroundColor': '#E74C3C'}),
            html.Button('📥 Fetch Base Data', id='fetch-base-button', n_clicks=0, style={**BUTTON_STYLE, 'backgroundColor': '#8E44AD'}),
            html.Button('❌ Clear Data', id='clear-button', n_clicks=0, style={**BUTTON_STYLE, 'backgroundColor': '#F39C12'}),
            html.Button('🔄 Refresh', id='refresh-button', n_clicks=0, style={**BUTTON_STYLE, 'backgroundColor': '#2980B9'}),
            html.Button('💾 Save Data', id='save-button', n_clicks=0, style={**BUTTON_STYLE, 'backgroundColor': '#3498DB'}),
            html.Button('📌 Set as Base', id='base-button', n_clicks=0, style={**BUTTON_STYLE, 'backgroundColor': '#9B59B6'}),
            html.Button('🔍 Show Defect', id='show-defect-button', n_clicks=0, style={**BUTTON_STYLE, 'backgroundColor': '#C0392B'}),

            html.Div(id='status-indicator', style={'marginTop': '10px', 'fontSize': '18px', 'color': '#555'}),
        ]),

        # Dropdown and Log Axis Checkboxes
        html.Div(
            style={**CARD_STYLE, 'display': 'flex', 'justifyContent': 'center', 'gap': '20px', 'flexWrap': 'wrap'},
            children=[
                html.Div([ 
                    html.Label("Select Type:", style={'fontSize': '16px', 'fontWeight': 'bold'}),
                    dcc.Dropdown(
                        id='plot-type',
                        options=[ 
                            {'label': 'RMS', 'value': 'rms'},
                            {'label': 'Peak', 'value': 'peak'},
                            {'label': 'Peak-to-Peak', 'value': 'ptp'}
                        ],
                        value='rms',
                        style={'width': '100%'}
                    ),
                ], style={'width': '30%'}),
                html.Div([ 
                    html.Label("Select Type:", style={'fontSize': '16px', 'fontWeight': 'bold'}),
                    dcc.Dropdown(
                        id='type',
                        options=[ 
                            {'label': 'ACCELERATION', 'value': 'acceleration'},
                            {'label': 'Velocity', 'value': 'velocity'}, 
                            {'label': 'DISPLACEMENT', 'value': 'displacement'}
                        ],
                        value='acceleration',
                        style={'width': '100%'}
                    ),
                ], style={'width': '30%'}),

                html.Div([ 
                    dcc.Checklist(
                        id='log-x',
                        options=[{'label': 'Log X Axis', 'value': 'log_x'}],
                        value=[],
                        style={'fontSize': '16px'}
                    ),
                ], style={'width': '30%'}),

                html.Div([ 
                    dcc.Checklist(
                        id='log-y',
                        options=[{'label': 'Log Y Axis', 'value': 'log_y'}],
                        value=[],
                        style={'fontSize': '16px'}
                    ),
                ], style={'width': '10%'}),
            ]
        ),

        # Vibration Graphs (Side by Side)
        html.Div(style={**CARD_STYLE, 'display': 'flex', 'gap': '20px'}, children=[
            html.Div(style={'flex': '1'}, children=[
                dcc.Graph(id='vibration-graph', style={'marginTop': '20px'}),
            ]),
            html.Div(style={'flex': '1'}, children=[
                dcc.Graph(id='vibration-graph-2', style={'marginTop': '20px'}),
            ]),
        ]),

        html.Div(id='sampling-rate-display', style={'marginTop': '10px', 'fontSize': '18px', 'color': '#555'}),

        # Save to Excel Section
        html.Div(style={**CARD_STYLE, 'textAlign': 'center'}, children=[
            html.Button('📊 Save to Excel', id='save-excel-button', n_clicks=0, style={**BUTTON_STYLE, 'backgroundColor': '#2ECC71'}),
            html.Div(
                children=[
                    dcc.Input(id='filename-input', type='text', placeholder='Enter filename', style=INPUT_STYLE),
                ],
                id='filename-input-container',
                style={'display': 'none'}
            ),
            dcc.Download(id="download-excel")
        ]),

        # Measurement Data Table with Save to DB button
        html.Div(style=CARD_STYLE, children=[
            html.H3("📋 Measurement Data Table", style={'color': '#2C3E50', 'marginBottom': '10px'}),
            html.Button('💾 Save to DB', id='save-db-button', n_clicks=0, style={**BUTTON_STYLE, 'backgroundColor': '#F39C12'}),
            dash_table.DataTable(
                id='measurement-table',
                columns=[ 
                    {'name': 'Machine ID', 'id': 'machine_id', 'editable': False},
                    {'name': 'Measurement Location', 'id': 'meas_point', 'editable': False},
                    {'name': 'Date', 'id': 'date', 'editable': False},
                    {'name': 'Band 1', 'id': 'band1', 'editable': False},
                    {'name': 'Band 2', 'id': 'band2', 'editable': False},
                    {'name': 'Band 3', 'id': 'band3', 'editable': False},
                    {'name': 'Band 4', 'id': 'band4', 'editable': False},
                    {'name': 'Overall RMS', 'id': 'overall_rms', 'editable': False},
                    {'name': 'Remarks', 'id': 'remarks', 'editable': True},
                ],
                data=[],
                editable=True,
                row_deletable=True,
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'center', 'padding': '5px'},
            ),
        ]),

        # Interval component for live updates
        dcc.Interval(id='interval-component', interval=1000, n_intervals=0, disabled=True),
        
        # Add the dcc.Location component to handle the refresh functionality
        dcc.Location(id='url', refresh=True)
    ]
)