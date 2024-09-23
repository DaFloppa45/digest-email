# --- Weather Forecast Config ---
from pyowm.owm import OWM
from pyowm.utils import formatting, measurables

owm = OWM('c92d7336677e626ce0c6d9eca0be3777') # OWM API Key
mgr = owm.weather_manager()
# -------------------------------

def get_forecast():
    # Initial Setup
    forecast = {'city': 'Reading',
                'country': 'GB',
                'periods': []}
    
    # Collect forecast data from OWM API
    obs = mgr.forecast_at_place(f"{forecast['city']},{forecast['country']}",'3h',9).forecast

    # Pick wanted details to output for each period
    for per in obs.to_dict()['weathers']:
        entry = {}
        entry['time'] = formatting.timeformat(per['reference_time'],'iso')
        entry['status'] = per['detailed_status']
        entry['temp'] = measurables.kelvin_dict_to(per['temperature'],'celsius')['temp']
        entry['weather_icon'] = per['weather_icon_name']
        forecast['periods'].append(entry)
        
    return forecast
        
        
    

def get_events():
    pass

def get_finance():
    pass

if __name__ == "__main__":
    print(get_forecast())
    