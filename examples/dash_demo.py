import dash
import pandas as pd
import pygwalker as pyg

df = pd.read_csv("https://kanaries-app.s3.ap-northeast-1.amazonaws.com/public-datasets/bike_sharing_dc.csv")

app = dash.Dash()

pyg_html_code = pyg.to_html(df)

app.layout = dash.html.Div([
    dash.html.Iframe(srcDoc=pyg_html_code, style={"width": "100%", "height": "100vh", "border": "0"}),
])

if __name__ == '__main__':
    # After startup, open http://127.0.0.1:8050/ in your browser.
    # To stop the server: press Ctrl+C in this terminal.
    # If the terminal is gone, kill the process holding port 8050 (PowerShell):
    #   Get-NetTCPConnection -LocalPort 8050 | Select-Object -ExpandProperty OwningProcess | ForEach-Object { Stop-Process -Id $_ -Force }
    app.run(debug=True)
