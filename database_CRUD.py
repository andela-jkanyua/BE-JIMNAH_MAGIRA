from sqlalchemy import create_engine, func, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound
 
from database_declarative import StockQuote, Base
import datetime
import requests
from suds.client import Client
from prettytable import PrettyTable
import database_declarative

engine = create_engine('sqlite:///sqlalchemy_backend.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance

Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()
 


# Insert a record in the StockQuote table

def add(ind, l_value, lo_value, m_date):
	new_record = StockQuote(indice=ind, latest_value=l_value,\
		local_value=lo_value, date_modified=m_date)
	session.add(new_record)
	session.commit()

	return 'A Record has been added'

# SOAP function that acquires values from which to call our add function

def add_new_record():
	indices = ['CPA', 'CHRW', 'PHMD', 'WMLP',\
				'MDGS']
	url_service_1 = 'http://www.restfulwebservices.net/wcf/StockQuoteService.svc?wsdl'
	url_service_2 = 'http://www.restfulwebservices.net/wcf/CurrencyService.svc?wsdl'
	client_1 = Client(url_service_1)
	client_2 = Client(url_service_2)

	conversion_rate = float(client_2.service.GetConversionRate('USD','KES').Rate)
	
	for item in indices:
		lvalue = float(client_1.service.GetStockQuote(item).Last) 
		lo_value = float((client_1.service.GetStockQuote(item).Low)) * conversion_rate
		time_updated = datetime.datetime.now()

		print(add(item, round(lvalue,2), round(lo_value,2), time_updated))

#Prints a well formatted table to display values on console
def show_all():

	records = session.query(StockQuote).order_by(desc(StockQuote.id))
	x = PrettyTable()
	x.field_names = ["Id","Indice", "Latest Value - USD", "Local Value - KES", "Date Modified"]
	for item in records:
		x.add_row([item.id, item.indice, item.latest_value, item.local_value, item.date_modified])

	print (x)
	with open('file.csv', 'w') as w:
		w.write(str(x))




#Call to new record function
add_new_record()

#Call to print Table function after insert
show_all()