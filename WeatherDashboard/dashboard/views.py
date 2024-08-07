from django.shortcuts import render
from django.http import HttpResponse
from dashboard.forms import CityForm
from dashboard.models import City
from django.conf import settings
import requests

# Create your views here.
def get_weather_data(city_name):
    url = f'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': city_name,
        'appid': settings.OWM_API_KEY,
        'units': 'metric'
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return None
    json_response = response.json()

    weather_data = {
        'temp': json_response['main']['temp'],
        'temp_min': json_response['main']['temp_min'],
        'temp_max': json_response['main']['temp_max'],
        'city_name': json_response['name'],
        'country': json_response['sys']['country'],
        'lat': json_response['coord']['lat'],
        'lon': json_response['coord']['lon'],
        'weather': json_response['weather'][0]['main'],
        'weather_desc': json_response['weather'][0]['description'],
        'pressure': json_response['main']['pressure'],
        'humidity': json_response['main']['humidity'],
        'wind_speed': json_response['wind']['speed'],
    }
    return weather_data

def home(request):
    form = CityForm()

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
            city_name = form.cleaned_data.get('city_name')
            weather_data = get_weather_data(city_name)
            

    elif request.method == 'GET':
        try:
            city_name = City.objects.latest('date_added').city_name
            weather_data = get_weather_data(city_name)
        except Exception as e:
            weather_data = None
            
    template_name = 'home.html'
    context = {'form': form, 'weather_data': weather_data}
    return render(request, template_name, context=context)

def history(request):
    template_name = 'history.html'
    cities = City.objects.all().order_by('-date_added')[:5]

    weather_data_list = []
    for city in cities:
        city_name = city.city_name
        weather_data_list.append(get_weather_data(city_name))

    context = {'weather_data_list': weather_data_list}
    return render(request, template_name, context)
