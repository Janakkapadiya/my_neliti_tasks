import json
import certifi
from django.http import HttpResponse
from django.shortcuts import render
import urllib3

from wether.forms import SearchForm

# Create your views here.


def index(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)

        http = urllib3.PoolManager(
            cert_reqs='CERT_REQUIRED',
            ca_certs=certifi.where()
        )

        if form.is_valid():
            latitude = form.cleaned_data['latitude']
            longitude = form.cleaned_data['longitude']
            url = http.request('POST', 'https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=' +
                               str(latitude) + '&lon=' + str(longitude))

            list_of_data = json.loads(url.data.decode('utf-8'))

            wether_list = []

            data = {
                'air_temperature': str(list_of_data['properties']['meta']['units']['air_temperature']),
                'relative_humidity': str(list_of_data['properties']['meta']['units']['relative_humidity']),
                'wind_speed': str(list_of_data['properties']['meta']['units']['wind_speed']),
                'wind_from_direction': str(list_of_data['properties']['meta']['units']['wind_from_direction']),
                'air_pressure_at_sea_level': str(list_of_data['properties']['meta']['units']['air_pressure_at_sea_level']),
                'cloud_area_fraction': str(list_of_data['properties']['meta']['units']['cloud_area_fraction'])
            }

            time_series = list_of_data['properties']['timeseries']

            for itr in time_series:

                wether = {
                    'time': str(itr['time']),
                    'air_temperature_': str(itr['data']['instant']['details']['air_temperature']),
                    'relative_humidity_': str(itr['data']['instant']['details']['relative_humidity']),
                    'wind_speed_': str(itr['data']['instant']['details']['wind_speed']),
                    'wind_from_direction_': str(itr['data']['instant']['details']['wind_from_direction']),
                    'air_pressure_at_sea_level_': str(itr['data']['instant']['details']['air_pressure_at_sea_level']),
                    'cloud_area_fraction_': str(itr['data']['instant']['details']['cloud_area_fraction'])
                }

                print(wether)

                wether_list.append(wether)

    else:
        form = SearchForm()
        data = None
        list_of_data = None
        wether_list = None

    return render(request, 'index.html', {'form': form,
                                          "data": data,
                                          "list_of_data": list_of_data,
                                          "wether_list": wether_list
                                          })
