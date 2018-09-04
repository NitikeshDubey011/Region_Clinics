from bottle import route, request, response, run, error
import petl as pt
import json


# this link will give the list of services
@route('/getservices')
def anyServices():
    # reading the csv file
    csv = pt.fromcsv('services.csv')
    # json content type declaration
    response.headers['Content-type'] = 'application/json'
    response.headers['Access-Control-Allow-Origin'] = '*'
    # cutting out the required column names
    jsonData = pt.cut(csv, 'ServiceID', 'Service')
    # convert the dictionary data into json data
    jsonData = json.JSONEncoder().encode(list(pt.dicts(jsonData)))
    # returning the json data
    return jsonData


# this link will provide the clinics names who provide the particular services
@route('/getclinics')
# start of module
def main_loop():
    # requested query
    inputServiceID = request.query.serviceid
    csv = pt.fromcsv('clinicservicelocations.csv')
    response.headers['Content-type'] = 'application/json'
    response.headers['Access-Control-Allow-Origin'] = '*'
    for i in csv:
        if inputServiceID == i[0]:
            # select the data according to the given requested query
            dataSelect = pt.select(csv, "{ServiceID} == '" + str(inputServiceID) + "'")
            # cutting out the required column names
            jsonData = pt.cut(dataSelect, 'Name', 'Service', 'Suburb', 'State', 'Email', 'Lat', 'Lon')
            # convert the dictionary data into json data
            jsonData = json.JSONEncoder().encode(list(pt.dicts(jsonData)))
            # return the json data
            return jsonData

        # this is requested link of getting all the distinct list of
        # clinics offering any service.
        if inputServiceID == "0":
            anyServices = pt.unique(csv, key='Name')
            jsonData = pt.cut(anyServices, 'Name', 'Service', 'Suburb', 'State', 'Email', 'Lat', 'Lon')
            jsonData = json.JSONEncoder().encode(list(pt.dicts(jsonData)))
            return jsonData
    else:
        jsonData = json.JSONEncoder().encode('Unable to find this id.')
        return jsonData


# error handling or exception handling
@error(404)
def linkerror(error):
    return "<h1>Please fill proper link!!"


run(host='localhost', port='8080', debug=True)
