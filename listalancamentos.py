import requests
from prettytable import PrettyTable
from datetime import datetime, timezone, timedelta

def listar_novas_criptos():
    url_recent = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 250,
        "page": 1,
        "sparkline": False
    }
    response_recent = requests.get(url_recent, params=params)
    
    if response_recent.status_code == 200:
        dados = response_recent.json()
        criptos_ordenadas = sorted(dados, key=lambda x: x.get("atl_date", ""), reverse=True)
        
        tabela = PrettyTable()
        tabela.field_names = ["Nome", "Símbolo", "Data", "Hora"]
        
        fuso_brasilia = timezone(timedelta(hours=-3))
        
        for cripto in criptos_ordenadas[:20]:  # Mostra as 10 mais recentes
            atl_date = cripto.get('atl_date', None)
            if atl_date:
                dt_obj = datetime.fromisoformat(atl_date.replace('Z', '')).replace(tzinfo=timezone.utc).astimezone(fuso_brasilia)
                data_formatada = dt_obj.strftime('%d-%m-%Y')
                hora_formatada = dt_obj.strftime('%H:%M:%S')
            else:
                data_formatada, hora_formatada = 'Desconhecida', 'Desconhecida'
            
            tabela.add_row([cripto['name'], cripto['symbol'], data_formatada, hora_formatada])
        
        print(tabela)
    else:
        print("Erro ao buscar criptomoedas recentes.")

def main():

    try:

        listar_novas_criptos()

        return True

    except Exception as error:
        print(f'\nError: {error}')

        return False


if __name__ == "__main__":
    main()
