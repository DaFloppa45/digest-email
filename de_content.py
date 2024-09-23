from datetime import datetime, timedelta
# --- Weather Forecast Config ---
from pyowm.owm import OWM
from pyowm.utils import formatting, measurables

owm = OWM('c92d7336677e626ce0c6d9eca0be3777') # OWM API Key
mgr = owm.weather_manager()
# -------------------------------

# --- ICloud Config ---
# app-specific password: reim-wvbd-kynv-dsqj
import caldav
from caldav.elements import dav, cdav

num = 52
dsid = 21409152914
guid = 'E6E94AC8-9F66-40EC-A96B-CD9618604AB4'

icloud_client = caldav.DAVClient(
    url='https://caldav.icloud.com/',
    username='m.latinomain@icloud.com',
    password='reim-wvbd-kynv-dsqj'
)
# ---------------------

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
    principal = icloud_client.principal()
    calendars = principal.calendars()
    output = []
    for calendar in calendars:
        events = calendar.date_search(
            start=datetime.now(),
            end=datetime.now() + timedelta(days=1)
        )
        for event in events:
            name = event.vobject_instance.vevent.summary.value
            start_time = event.vobject_instance.vevent.dtstart.value
            end_time = event.vobject_instance.vevent.dtend.value
            output.append({
                'name': name,
                'start_time': start_time.strftime("%H:%M:%S"),
                'end_time': end_time.strftime("%H:%M:%S")
                })
        
    return output


def get_finance():
    pass

if __name__ == "__main__":
    print(get_events())

    
        