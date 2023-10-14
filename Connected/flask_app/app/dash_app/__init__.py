import dash
from dash import dcc,html
from datetime import datetime,date
from dash.dependencies import Output, Input
import pandas as pd
import plotly.express as px
import os


external_stylesheets = [
    "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css",
    {
        'href': "https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css",
        'rel': 'stylesheet',
        'integrity': "sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC",
        'crossorigin': 'anonymous',
    },
]



def create_dash_application(flask_app):
    # sales = pd.read_csv('/Users/tranvo1233/VSCode/MyShecodes/Connected/flask_app/app/dash_app/data/brand.csv')

    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    path_sales = os.path.join(SITE_ROOT, "data", "brand.csv")
    sales = pd.read_csv(path_sales)

    sales["InvoiceDate"] = pd.to_datetime(sales["InvoiceDate"])
    sales["InvoiceDate"] = sales["InvoiceDate"].apply(lambda x: x.date())

    dash_app = dash.Dash(__name__, external_stylesheets=external_stylesheets,title='[SheCode]', server = flask_app, url_base_pathname='/dash/')
    # dash_app.layout = html.Div([
    #     html.H1('Dash App'),
    # ])
    dash_app.index_string = '''
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <!-- BOOTSTRAP -->
                    {%css%}
                    <title>{%title%}</title>
                </head>

                <body>
                    <div class="d-flex flex-column">
                            <nav class="navbar sticky-top bg-body-tertiary d-flex align-items-center justify-content-between p-4 " style="background-color: #e3f2fd;">
                                <div class="header_logo container-fluid">
                                    <a class="navbar-brand" href="http://127.0.0.1:5000"  style="color: black;">
                                        <img width="80" height="40" src="../static/img/logo1.png" alt="logo">
                                        SheCodes
                                    </a>
                                    <div class="">
                                        <ul class=" m-0 d-flex flex-row align-items-center " style="list-style:none;">
                                            <li class="p-2"><a href="http://127.0.0.1:5000" style='text-decoration: none; color:inherit'>Home</a></li>
                                            <li class="p-2"><a href="http://127.0.0.1:5000/about" style='text-decoration: none; color:inherit'>About Us</a></li>
                                            <li class="p-2"><a href="http://127.0.0.1:5000/products" style='text-decoration: none; color:inherit'>Products</a></li>
                                            <li class="p-2 me-3"><a href="http://127.0.0.1:5000/company" style='text-decoration: none; color:inherit'>Company</a></li>

                                            <li class="">
                                                <a class="text-light" href="http://127.0.0.1:5000/auth/login">
                                                    <button type="button" class="btn btn-primary">Login</button>
                                                </a>
                                            </li>
                                        
                                        </ul>
                                    </div>
                                    
                                </div>
                            
                            </nav>
                        <div class="m-3">                                                               
                            {%app_entry%}         
                           
                        </div>
                        <footer>
                                {%config%}
                                {%scripts%}
                                {%renderer%}
                        </footer>
                    </div>
                    <!-- <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script> -->
                    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
                </body>
                </html> 
 
        '''


    dash_app.layout = html.Div( 
        className='d-flex flex-row justify-content-center',   
        children =[
            html.Div(
                className = 'container',
                children = [
                    html.Div(
                        className= 'row mb-3',
                        children=[
                            # html.Div('Plotly Dash',className="m-4"),
                            # html.Button("nice",className='btn btn-primary'),
                            html.Div(
                                className='col-6', 
                                children= [
                                    dcc.Dropdown(
                                        id = "input", 
                                        options = [{"label": "USA", "value" :"USA"}, {"label": "Austria", "value":'Austria'},{"label": "Greece", "value" :"Greece"}],
                                        placeholder="Select a country",
                                        style={'width': '50%'}
                                        # style={"width": "50%";},
                                    ),
                                    dcc.Graph(id='graph', className='w-80'),
                                ]
                            ),
                            html.Div(
                                className='col-6',
                                children = [
                                    dcc.DatePickerSingle(id='sale_date',
                                        min_date_allowed=sales['InvoiceDate'].min(),
                                        max_date_allowed=sales['InvoiceDate'].max(),
                                        initial_visible_month= date(2010,1,26),
                                        date=date(2010,1,26),
                                        style={'width':'200px', 'margin':'0 auto'}),
                                    dcc.Graph(id='sale-date-graph'),
                                ]
                            ),
                        ]     
                    )
                ]
            )
        ]
    )
    @dash_app.callback(
        Output(component_id = 'graph',component_property='figure'),
        Input(component_id='input',component_property='value')
    )
    def update_plot(input_country):
        country = "USA"
        sales_country = sales.copy(deep=True)
        if input_country:
            country = input_country
            sales_country= sales_country[sales_country["Country"] ==  country].groupby("StockCode")["Quantity"].sum().reset_index(name='Total Quantity')
            sales_country = sales_country.sort_values(by="Total Quantity",ascending=False).reset_index(drop=True)
            bar = px.bar(data_frame = sales_country, x="StockCode",y="Total Quantity",title=f'Total Quantity in {country}')
        else:
    #         sales_country= sales_country[sales_country["Country"] ==  "USA"].groupby("StockCode")["Quantity"].sum().reset_index(name='Total Quantity')
    #         sales_country = sales_country.sort_values(by="Total Quantity",ascending=False).reset_index(drop=True)
            total = sales_country.groupby("Country")["Quantity"].sum().reset_index(name="Total Quantity").sort_values(by="Total Quantity",ascending=False).reset_index(drop=True)
            bar = px.bar(data_frame = total, x="Country",y="Total Quantity",title='Total Quantity by Country')
        return bar

    @dash_app.callback(
        Output(component_id='sale-date-graph', component_property='figure'),
        Input(component_id='sale_date', component_property='date')
    )
    def hi(input_date):
        sales_country = sales.copy(deep=True)
        if input_date:
            input_date = datetime.strptime(input_date, "%Y-%m-%d").date()
            sales_country = sales_country[sales_country['InvoiceDate'] == input_date]
        sales_country = sales_country.groupby("StockCode")["Quantity"].sum().reset_index(name="Total quantity")
        sales_country = sales_country.sort_values(by='Total quantity', ascending=False).reset_index(drop=True)
        bar =  px.bar(data_frame = sales_country[:20], x="StockCode",y="Total quantity",title=f'Total Quantity in {input_date}')
        return bar
    if __name__ == "__main__":
        dash_app.run_server(debug = True)
    return dash_app





