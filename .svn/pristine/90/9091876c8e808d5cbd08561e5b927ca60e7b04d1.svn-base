

import osa

#https://bitbucket.org/sboz/osa/wiki/Home

try:
	client = osa.Client("http://www.thomas-bayer.com/axis2/services/BLZService?wsdl")
	result = client.service.getBank("76251020")
	print result
except Exception,e:
	pass

try:
	client = osa.Client("http://wsf.cdyne.com/WeatherWS/Weather.asmx?WSDL")
	result = client.service.GetCityForecastByZIP("48103")
	print result
	result = client.service.GetCityWeatherByZIP("48103")
	print result

except Exception,e:
	pass


try:
	client = osa.Client("http://www.webservicex.net/globalweather.asmx?WSDL")
	result = client.service.GetCitiesByCountry("United States")
	print result
	result = client.service.GetWeather("Ann Arbor","United States")
	print result

except Exception,e:
	pass

try:
	client = osa.Client("http://graphical.weather.gov/xml/SOAP_server/ndfdXMLserver.php?wsdl")
	result = client.service.GetWeatherByZipCode("48103")
	print result
	print result

except Exception,e:
	pass


# try:
# 	client = osa.Client("https://onlineapplication.credentialcheck.com/careeropportunities/services/ccc/service.asmx?WSDL")
# 	result = client.service.GetAvailableServices("UMHS_Profile","#*@@)M45**2012@@(##$#",1)
# 	print result
# except Exception,e:
# 	pass
