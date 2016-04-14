from factual import Factual
from django.utils.encoding import smart_str
import pandas as pd
import string
import json

# set up api
factual = Factual('HShWyOdPbw6OdXNEvR1ZR4px2RbGC95xvKbpgUTV', 'xN2HcgnG6nueorqRw584jHUSf3SIg5BJriFoNyc5')


# UK postalcodes
postalcodes = pd.read_csv('/Users/artsy/Desktop/factual/UK/UK_codes.csv')
postalcodes = postalcodes['Postalcode'][0:]

# country codes
countries = {'United States': 'places-us',
'China': 'places-cn',
'Japan': 'places-jp',
'Germany': 'places-de',
'Italy': 'places-it',
'France': 'places-fr',
'Spain': 'places-es',
'United Kingdom': 'places-gb',
'Brazil': 'places-br',
'Canada': 'places-ca',
'Australia': 'places-au',
'South Korea': 'places-kr',
'Portugal': 'places-pt',
'Taiwan': 'places-tw',
'Switzerland': 'places-ch',
'Norway': 'places-no',
'Russia': 'places-ru',
'Sweden': 'places-se',
'Austria': 'places-at',
'Mexico': 'places-mx',
'Denmark': 'places-dk',
'South Africa': 'places-za',
'India': 'places-in',
'Indonesia': 'places-id',
'Finland': 'places-fi',
'Netherlands': 'places-nl',
'Belgium': 'places-be',
'Thailand': 'places-th',
'Philippines': 'places-ph',
'Singapore': 'places-sg',
'Argentina': 'places-ar',
'Hong Kong': 'places-hk',
'Ireland': 'places-ie',
'Poland': 'places-pl',
'Turkey': 'places-tr',
'New Zealand': 'places-nz',
'Malaysia': 'places-my',
'Israel': 'places-il',
'Chile': 'places-cl',
'Colombia': 'places-co',
'Hungary': 'places-hu',
'Vietnam': 'places-vn',
'Croatia': 'places-hr',
'Czech Republic': 'places-cz',
'Puerto Rico': 'places-pr',
'Luxembourg': 'places-lu',
'Venezuela': 'places-ve',
'Peru': 'places-pe',
'Greece': 'places-gr',
'Egypt': 'places-eg'}

# columns
cols = ['Name', 'Locality', 'Postalcode', 'Address', 'Region', 'Country', 'Neighborhood', 'Phone', 'Email', 'Website', 'Category Labels']

# alphabet
upper = list(string.ascii_uppercase)
lower = list(string.ascii_lowercase)


def format_data(response, code):

	df = pd.DataFrame(columns=cols, index=[0])

	for x in response:

		bump = pd.DataFrame(columns=cols, index=[0])

		try:
			bump['Name'] = smart_str(x['name'])
		except Exception:
			bump['Name'] = ''
		try:	
			bump['Locality'] = smart_str(x['locality'])
		except Exception:
			bump['Locality'] = ''
		try:
			bump['Postalcode'] = smart_str(x['postcode'])
		except Exception:
			bump['Postalcode'] = ''
		try:
			bump['Address'] = smart_str(x['address'])
		except Exception:
			bump['Address'] = ''
		try:
			bump['Region'] = smart_str(x['region'])
		except Exception:
			bump['Region'] = ''
		try:
			bump['Country'] = smart_str(x['country'])
		except Exception:
			bump['Country'] = ''
		try:
			bump['Neighborhood'] = smart_str(x['neighborhood'])
		except Exception:
			bump['Neighborhood'] = ''
		try:
			bump['Phone'] = smart_str(x['tel'])
		except Exception:
			bump['Phone'] = ''
		try:
			bump['Email'] = smart_str(x['email'])
		except Exception:
			bump['Email'] = ''
		try:
			bump['Website'] = smart_str(x['website'])
		except Exception:
			bump['Website'] = ''
		try:
			bump['Category Labels'] = smart_str(x['category_labels'])
		except Exception:
			bump['Category Labels'] = ''

		df = df.append(bump)

	return df


def api_calls(location, codes, search_term):

	places = factual.table(countries[location])

	# results dataframe
	all_results = pd.DataFrame(columns=cols)

	# iterate through postal codes
	for y in codes:

		# search with filters
		data = places.search(search_term).limit(50).filters( { "$and": [ {"postcode": {"$bw": str(y)}}, {"category_labels": { "$includes_any": ['Art Dealers and Galleries']}} ] } ).data()
		results = format_data(data, y)
		all_results = all_results.append(results)
		print 'Page 1 of code ' + str(y) + ' returned ' + str(len(results) - 1) + ' rows.'

		counter = 50

		while (len(data) >= 50) and (counter < 500):

			next_page = places.search(search_term).offset(counter).limit(50).filters( { "$and": [ {"postcode": {"$bw": str(y)}}, {"category_labels": { "$includes_any": ['Art Dealers and Galleries']}} ] } ).data()
			results = format_data(next_page, y)
			all_results = all_results.append(results)
			print 'Page ' + str((counter/50 + 1)) + ' of code ' + str(y) + ' returned ' + str(len(results) - 1) + ' rows.'

			counter += 50
			data = next_page

		if counter == 500:
			print 'Refactor: Code ' + str(y) + '. (More than 500 results.)'
		
	# output csv
	all_results = all_results.drop_duplicates()
	all_results.to_csv('/Users/artsy/Desktop/factual/UK/CRAWL1/all_' + search_term.replace(' ','_') + '.csv')


# call United States, NYC postalcodes
api_calls('United Kingdom', postalcodes, 'Gallery')
