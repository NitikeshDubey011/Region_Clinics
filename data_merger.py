import petl as pt
import re


# Convenience function to convert values under the given field using a regular expression substitution."""
def substitute(table, field, pattern, repl, count=0, flags=0):
    program = re.compile(pattern, flags)
    convert = lambda tempData: program.sub(repl, tempData, count=count)
    return pt.convert(table, field, convert)

# use to read the csv file using the petl framework
# the below code is use to read services csv file
fileData = pt.fromcsv('services.csv')
# the below code is use to read clinicservices csv file
servicesData = pt.fromcsv('clinicservices.csv')
# join the csv file using the inbuilt function join using ServiceID as main key
fileJoin = pt.join(servicesData, fileData, key="ServiceID")
# the below code is use to read clinic csv file
readCsv = pt.fromcsv('clinics.csv')
# join the csv file using the inbuilt function join using ClinicID as main key
doubleJoin = pt.join(fileJoin, readCsv, key='ClinicID')
# reading the xml file cliniclocations.xml
locationXML = pt.fromxml('cliniclocations.xml', 'clinic', {"ClinicID": "ClinicID", "Lat": "Lat", "Lon": "Lon"})
# join the csv file using the inbuilt function join using ClinicID as main key
doubleJoin2 = pt.join(doubleJoin, locationXML, key="ClinicID")
# removing the spaces from the email field
cleanOne = substitute(doubleJoin2, 'Email', '\s', '')
# adding @myclinic.com.au behind every email id
cleanTwo = substitute(cleanOne, 'Email', '(^[\w]+$)', '\\1@myclinic.com.au')
# acquire the required columns
result = pt.cut(cleanTwo, 'ClinicServiceID', 'ClinicID', 'ServiceID', 'Service', 'Name', 'Suburb', 'State', 'Email',
                'Lat', 'Lon')
# creating the final csv file which is clinicservicelocations.csv
pt.tocsv(result, "clinicservicelocations.csv")
print('Csv file generated.!!!')
