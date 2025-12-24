import plotly.express as px

def line_chart(df, x, y, title):
    fig = px.line(df, x=x, y=y, markers=True, title=title)
    return fig

def bar_chart(df, x, y, title):
    fig = px.bar(df, x=x, y=y, color=x, title=title)
    return fig
