# -*- coding: utf-8 -*-
from django.http import request
from django.shortcuts import render

from .views import opcostICE as ice_operate, opcostEV as ev_operate
from .views import capitalICE as capICE, opcostICE as opICE, maintainenceICE as maICE, insuranceICE as inICE, \
    resaleICE as reICE, ownershipICE as ownICE
from .views import capitalEV as capEV, opcostICE as opEV, maintainenceEV as maEV, insuranceEV as inEV, resaleEV as reEV, \
    ownershipEV as ownEV
from .views import drivingRange

costs_ice = [capICE, opICE, inICE, maICE, reICE]
costs_ev = [capEV, opEV, inEV, maEV, reEV]


def operating_line_plot(ice_operate, ev_operate):
    import plotly.graph_objects as go
    import numpy as np

    x = [2023, 2024, 2025, 2026, 2027, 2028]
    x_rev = x[::-1]

    # Line 1
    y1 = ice_operate
    range_y1 = (sum(y1) / len(y1)) / 15
    y1_upper = [x + range_y1 for x in y1]
    y1_lower = [x - range_y1 for x in y1]
    y1_lower = y1_lower[::-1]

    # Line 2
    y2 = ev_operate
    range_y2 = (sum(y2) / len(y2)) / 2
    y2_upper = [x + range_y2 for x in y2]
    y2_lower = [x - range_y2 for x in y2]
    y2_lower = y2_lower[::-1]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x + x_rev,
        y=y1_upper + y1_lower,
        fill='toself',
        fillcolor='rgba(0,100,80,0.2)',
        line_color='rgba(255,255,255,0)',
        showlegend=False,
        name='ICE',
    ))
    fig.add_trace(go.Scatter(
        x=x + x_rev,
        y=y2_upper + y2_lower,
        fill='toself',
        fillcolor='rgba(0,176,246,0.2)',
        line_color='rgba(255,255,255,0)',
        name='EV',
        showlegend=False,
    ))
    fig.add_trace(go.Scatter(
        x=x, y=y1,
        line_color='rgb(0,100,80)',
        name='ICE',
    ))
    fig.add_trace(go.Scatter(
        x=x, y=y2,
        line_color='rgb(0,176,246)',
        name='EV',
    ))
    fig.update_traces(mode='lines')
    fig.show()
    fig.write_html("ice_vs_ev_operating.html")


def cost_break_pie_ice(costs_ice):
    import plotly.express as px
    labels = ['Capital Cost', 'Operating Cost', 'Insurance Cost', 'Maintenance Cost', 'Resale Value']
    fig = px.pie(values=costs, names=labels, color_discrete_sequence=px.colors.sequential.RdBu)
    fig.show()
    fig.write_html("compareApp\cost_break_pie_ice.html")


def cost_break_pie_ev(costs_ev):
    import plotly.express as px
    labels = ['Capital Cost', 'Operating Cost', 'Insurance Cost', 'Maintenance Cost', 'Resale Value']
    fig = px.pie(values=costs_ev, names=labels, color_discrete_sequence=px.colors.sequential.RdBu)
    fig.show()
    fig.write_html("compareApp\cost_break_pie_ev.html")


def ownership_cost_compare(ownership_ice, ownership_ev):
    import plotly.express as px
    fig = px.bar(x=['ICE', 'EV'], y=[ownership_ice, ownership_ev],
                 labels={'x': 'Year', 'y': 'Ownership Cost'}, height=400, pattern_shape_sequence=['.'])
    fig.show()
    fig.write_html("compareApp\ownership_cost_compare.html")


def costs_compare_bar(costs_ice, costs_ev):
    import plotly.graph_objects as go

    costs_labels = ['Capital Cost', 'Operating Cost', 'Maintenance Cost', 'Insurance Cost', 'Resale Value']

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=costs_labels,
        y=costs_ice,
        name='ICE',
        marker_color='indianred'
    ))
    fig.add_trace(go.Bar(
        x=costs_labels,
        y=costs_ev,
        name='EV',
        marker_color='lightsalmon'
    ))

    # Here we modify the tickangle of the xaxis, resulting in rotated labels.
    fig.update_layout(barmode='group', xaxis_tickangle=-45)
    fig.show()
    fig.write_html("compareApp/costs_compare_bar.html")


def ev_efficiency_reduction(drive_range):
    import plotly.express as px
    li = [drive_range]
    for i in range(5):
        drive_range = drive_range - drive_range * .023
        li.append(drive_range)
    years = [2023, 2024, 2025, 2026, 2027, 2028]
    fig = px.bar(x=years, y=li, title='Ev Efficiency Reduction', labels={'x': 'Years', 'y': 'Drive Range'})
    fig.show()
    fig.write_html("compareApp/ev_efficiency_reduction.html")


def graphsPlot():
    # operating_line_plot(ice_operate, ev_operate)
    # cost_break_pie_ice(costs_ice)
    # cost_break_pie_ev(costs_ev)
    # ownership_cost_compare(ownICE, ownEV)
    # costs_compare_bar(costs_ice, costs_ev)
    # ev_efficiency_reduction(drivingRange)
    return render(request, 'compareApp/compare.html')
