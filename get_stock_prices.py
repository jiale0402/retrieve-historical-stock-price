from kucoin.client import Client
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account
import yfinance as yf

def get_spread_sheet_id():
	return "1v6fBeuhSD2x3LQXGtT0dY-AiMKvWV15icep6o6DDP2I"

def download_data(key):
	data = yf.download(key,'2010-01-01','2022-03-22').to_dict("split")
	return data
	# ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']

def convert_timestamp_to_data(data):
	response = []
	for date in data:
		response.append([date.strftime('%Y-%m-%d')])
	return response

def write_data(data, service, sheet_name):
	body = {"values":data}
	request = service.spreadsheets().values().update(
	spreadsheetId=get_spread_sheet_id(), 
	range = sheet_name+"!B2", 
	valueInputOption="USER_ENTERED", 
	body=body
	).execute()

def write_headings(data, service, sheet_name):
	body = {"values":data}
	request = service.spreadsheets().values().update(
	spreadsheetId=get_spread_sheet_id(), 
	range = sheet_name+"!B1", 
	valueInputOption="USER_ENTERED", 
	body=body
	).execute()

def write_timestamp(data, service, sheet_name):
	data = convert_timestamp_to_data(data)
	body = {"values":data}
	request = service.spreadsheets().values().update(
	spreadsheetId=get_spread_sheet_id(), 
	range = sheet_name+"!A2", 
	valueInputOption="USER_ENTERED", 
	body=body
	).execute()

def main(): 
	SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
	SERVICE_ACCOUNT_FILE = ('key.json')
	creds = None
	creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
	service = build('sheets', 'v4', credentials=creds)
	spreadsheet_id = get_spread_sheet_id()

	keys = ["SBUX","NVDA","MSI","TSLA","MSFT","GOOG","GM","PFE","LKNCY","BABA","FB","AAPL"]
	for key in keys:
		data = download_data(key)
		write_data(data["data"], service, key)
		write_headings([data["columns"]], service, key)
		write_timestamp(data["index"], service, key)
	"""
	spy_heading = download_heading("SPY")
	write_headings(spy_data, service, "SPY")
	"""
main()
