from dash import Dash, html, dcc, Input, Output, callback, dash_table
import plotly.express as px
import plotly.graph_objects as go
from dataloader import prepare_data

def create_weight_slider(id):
    return dcc.Slider(
        id=id,
        min=0,
        max=10,
        step=1,
        value=5,
        marks={i: str(i) for i in range(11)}
    )


cluster_stat_averages, player_stats, normalized_player_stats, features, grouped_player_names = prepare_data()

app = Dash(__name__)


app.layout = html.Div(
    children=[

        # Global styling
        html.Div(
            style={
                "backgroundColor": "#F3F4F6",  # Light gray
                "font-family": "Arial, sans-serif",
                "color": "#333",
                "padding": "20px",
                "margin": "0 auto",  # Center dashboard
                "maxWidth": "1200px",  # Limit dashboard width for readability
                "borderRadius": "10px",
                "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)"
            },

            children=[

                html.Div([
                    # Clustering Analysis Overview
                    html.H2("Clustering Analysis Findings", style={"textAlign": "center", "color": "#1F77B4"}),

                    # Cluster overview heatmap
                    dcc.Graph(
                        figure=px.imshow(
                            cluster_stat_averages.values,
                            x=cluster_stat_averages.columns,
                            y=cluster_stat_averages.index,
                            color_continuous_scale="GnBu", 
                            title="Midfielder Cluster Attribute Overview (Z score normalized)"
                        ), 
                        style={"border": "2px solid #ccc", "borderRadius": "10px"}
                    ),

                    html.P(
                        "Note: Z scores indicate how much an attribute from the average across all clusters. Lighter colors indicate below average performance in each attribute, while darker colors indicate the opposite."
                    ),

                    html.Div([
                        html.Div([
                            html.Label("X"),
                            dcc.Dropdown(
                                features,
                                value=features[0],
                                placeholder="Select X axis attribute...",
                                style={'width': '150px'},
                                id='x-axis-dropdown'
                            ),
                        ]),

                        html.Div([
                            html.Label("Y"),
                            dcc.Dropdown(
                                features,
                                value=features[1],
                                placeholder="Select Y axis attribute...",
                                style={'width': '150px'},
                                id='y-axis-dropdown'
                            ),
                        ])
                    ], style={"display":"flex", "padding": "20px"}),

                    dcc.Graph(id='player-scatter', style={"border": "2px solid #ccc", "borderRadius": "10px"}),
                ]),

                # Midfielder recommendation
                html.Div(
                    [
                        html.Div([
                            html.H2("Prioritize Attributes for Your Ideal Defensive Midfielder", style={"textAlign": "center", "color": "#1F77B4", "padding":"20px"}),

                            html.Label("Market Value (M Euro)"),
                            dcc.Slider(
                                min=0, 
                                max=int(player_stats['Market Value (M Euro)'].max()),
                                step=1,
                                value=35,
                                marks={i: f"{i}M" for i in range(0, int(player_stats['Market Value (M Euro)'].max()) + 1, 10)},
                                id="market-value-slider",
                                tooltip={"placement": "bottom"}
                            ),

                            html.Label("Tackles"),
                            create_weight_slider("tackles-weight"),

                            html.Label("Interceptions"),
                            create_weight_slider("interceptions-weight"),

                            html.Label("Recoveries"),
                            create_weight_slider("recoveries-weight"),

                            html.Label("Passing"),
                            create_weight_slider("passes-weight"),

                            html.Label("Assists"),
                            create_weight_slider("assists-weight"),

                            html.Label("Chances Created"),
                            create_weight_slider("chances-created-weight"),

                            html.Label("Shots"),
                            create_weight_slider("shots-weight"),

                            html.Label("Goals"),
                            create_weight_slider("goals-weight"),

                            html.H4("Recommended Defensive Midfielders (best to worst):")
                        ]),


                        # table: players by cluster and price
                        dash_table.DataTable(
                            id="cluster-table",
                            columns=[
                                {"name": "Player Name", "id": "Player_Name"},
                                {"name": "Market Value (M Euro)", "id": "Market Value (M Euro)"},
                                {"name": "Score", "id": "Score"},
                                ], 
                            page_size=10,
                            page_current=0,
                            page_action='custom',
                            sort_action='custom',
                            sort_mode='single',
                            sort_by=[{"column_id": "Score", "direction": "desc"}],
                            style_table={'marginTop': '20px', 'width': '100%'},
                            style_cell={'textAlign': 'center', 'padding': '10px'},
                            style_header={
                                'backgroundColor': '#f7f7f7',
                                'fontWeight': 'bold'
                            }
                        )
                    ],
                    style={"margin-top": "30px"}
                ),


                # Player comparison section title
                html.H2("Head to Head - Player Comparison", style={"textAlign": "center", "color": "#1F77B4", "padding": "20px"}),

                # Dropdowns for player comparison
                html.Div([
                    dcc.Dropdown(
                        grouped_player_names,
                        value=grouped_player_names[0]['value'],
                        placeholder="Select player...",
                        style={'width': '300px'},
                        id='player1'
                    ),
                    dcc.Dropdown(
                        grouped_player_names,
                        value=grouped_player_names[1]['value'],
                        placeholder="Select player...",
                        style={'width': '300px'},
                        id='player2'
                    )
                ], style={"display": "flex", "justifyContent": "space-evenly", "padding": "20px"}),

                # Comparison section (radar chart and player comparison table)
                dcc.Graph(id='head-to-head', style={"border": "2px solid #ccc", "borderRadius": "10px"}),
                html.Div(id="comparison-summary", style={"margin-top": "30px"})
            ]
        )
    ]
)



##### call back functions
@callback(
    Output('head-to-head', 'figure'),
    [Input('player1', 'value'), Input('player2', 'value')]
)
def update_player_radar(player1, player2):
    '''
    Updates radar chart with selected player(s). Will create blank radar chart if no player selected
    '''

    fig = go.Figure()

    if not player1 and not player2:
        fig.add_trace(go.Scatterpolar(r=[None]*len(features), theta=features))

    if player1:
        player1_stats = normalized_player_stats[normalized_player_stats.Player_Name == player1]

        r=player1_stats[features].T.values.flatten().tolist()

        fig.add_trace(go.Scatterpolar(r=r, theta=features, fill='toself', name=player1))

    if player2:
        player2_stats = normalized_player_stats[normalized_player_stats.Player_Name == player2]

        r2=player2_stats[features].T.values.flatten().tolist()

        fig.add_trace(go.Scatterpolar(r=r2, theta=features, fill='toself', name=player2))

    fig.update_layout(
        showlegend=True,
        title_text="Player Stats"
        )

    return fig



@callback(
        Output('player-scatter', 'figure'),
        [Input('x-axis-dropdown', 'value'), Input('y-axis-dropdown', 'value')]
)
def update_scatter(x_axis, y_axis):

    if not x_axis or not y_axis:
        return go.Figure()
    
    fig = px.scatter(
        player_stats, 
        x=x_axis, y=y_axis, color="Cluster", hover_data=["Player_Name"],
        title=f"{x_axis} vs. {y_axis} (per game)")
    
    fig.update_layout(
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )
    
    return fig


@callback(
    Output('cluster-table', 'data'),
    Input('market-value-slider', "value"),
    Input('cluster-table', "page_current"),
    Input('cluster-table', "page_size"),
    Input('cluster-table', 'sort_by'),
    Input('tackles-weight', 'value'),
    Input('passes-weight', 'value'),
    Input('interceptions-weight', 'value'),
    Input('recoveries-weight', 'value'),
    Input('assists-weight', 'value'),
    Input('goals-weight', 'value'),
    Input('shots-weight', 'value'),
    Input('chances-created-weight', 'value')
    )
def update_table(market_value, page_current, page_size, sort_by, tackles_w, passes_w, interceptions_w, recoveries_w, assists_w, goals_w, shots_w, chances_created_w):
    '''
    Updates table with midfielders according to price and cluster
    '''

    filtered_df = normalized_player_stats[(normalized_player_stats['Market Value (M Euro)'] <= market_value) & (normalized_player_stats['Cluster'] == "Defensive")].copy()

    filtered_df['Score'] = (
        (filtered_df['Tackles'] * (tackles_w)) +
        (filtered_df['Passes'] * (passes_w)) +
        (filtered_df['Interceptions'] * (interceptions_w)) +
        (filtered_df['Recoveries'] * (recoveries_w)) +
        (filtered_df['Assists'] * (assists_w)) +
        (filtered_df['Goals'] * (goals_w)) +
        (filtered_df['Shots'] * shots_w) +
        (filtered_df['Big chances created'] * chances_created_w)
    ).astype(int)

    if len(sort_by):
        dff = filtered_df.sort_values(
            sort_by[0]['column_id'],
            ascending=sort_by[0]['direction'] == 'asc',
            inplace=False
        )
    else:
        # No sort is applied
        dff = filtered_df

    return dff.iloc[
        page_current*page_size:(page_current+ 1)*page_size
    ].to_dict('records')



@app.callback(
    Output('comparison-summary', 'children'),
    [Input('player1', 'value'), Input('player2', 'value')]
)
def update_comparison_summary(player1, player2):
    '''
    Updates head to head player comparison table
    '''
    if not player1 or not player2:
        return html.P("Select two players to compare.", style={'textAlign': 'center'})
    
    player1_stats = player_stats[player_stats['Player_Name'] == player1]
    player2_stats = player_stats[player_stats['Player_Name'] == player2]
    
    player1_cluster = player1_stats['Cluster'].values[0]
    player2_cluster = player2_stats['Cluster'].values[0]
    
    comparison_data = []
    for feature in features:
        player1_value = player1_stats[feature].values[0]
        player2_value = player2_stats[feature].values[0]

        comparison_data.append(
            {
                "Attribute": feature,
                f"{player1}": round(player1_value, 2),
                f"{player2}": round(player2_value, 2)
            }
        )

    # add cluster player belongs to
    comparison_data.append(
        {
            "Attribute": "Cluster",
            f"{player1}": player1_cluster,
            f"{player2}": player2_cluster
        }
    )

    # create comparison summary table
    return dash_table.DataTable(
        columns=[
            {"name": "Attribute (per game basis)", "id": "Attribute"},
            {"name": f"{player1}", "id": f"{player1}"},
            {"name": f"{player2}", "id": f"{player2}"}
        ],
        data=comparison_data,
        style_data_conditional=[
            {
                'if': {
                    'filter_query': f'{{{player1}}} > {{{player2}}}',
                    'column_id': f'{player1}'
                },
                'backgroundColor': '#D4EFDF',  # Light green
                'color': 'black'
            },
            {
                'if': {
                    'filter_query': f'{{{player2}}} > {{{player1}}}',
                    'column_id': f'{player2}'
                },
                'backgroundColor': '#D4EFDF',  # Light green
                'color': 'black'
            }
        ],
        style_table={'marginTop': '20px', 'width': '100%'},
        style_cell={'textAlign': 'center', 'padding': '10px'},
        style_header={
            'backgroundColor': '#f7f7f7',
            'fontWeight': 'bold'
        }
    )


if __name__ == '__main__':
    app.run(debug=True)
