from flask import Flask, request,send_file
import pandas as pd
import datetime
import os
from haversine import haversine

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Welcome to the API'


def report(x,y):
    start = datetime.datetime.fromtimestamp(int(x))
    end = datetime.datetime.fromtimestamp(int(y))
    start = start.strftime("%Y%m%d%H%M%S")
    end = end.strftime("%Y%m%d%H%M%S")

    trip = pd.read_csv('Trip-info.csv')
    trip['date_time'] = pd.to_datetime(trip['date_time'], format='%Y%m%d%H%M%S')
    mask = (trip['date_time'] > start) & (trip['date_time'] <= end)
    trip = trip.loc[mask]
    if len(trip)==0:
        return ('Sorry there is no data avaliable in this time frame')
    vno = trip['vehicle_number'].unique()
    st = []
    fi = os.listdir('EOL-dump/')
    for i in vno:
        if i + '.csv' in fi:
            st.append(i)
    Numberplate = []
    Transport_name = []
    Speed_violation = []
    Avg_spd = []
    Distance = []
    Tripcount = []
    Harsh_Acc = []
    Harsh_Break = []
    for j in range(len(st)):
        z = st[j]
        truck = pd.read_csv(f'EOL-dump/{z}.csv')
        truck['tis'] = pd.to_datetime(truck['tis'], unit='s')
        truck['tis'] = pd.to_datetime(truck['tis'], format='%Y%m%d%H%M%S')
        mask = (truck['tis'] >= start) & (truck['tis'] <= end)
        truck = truck.loc[mask]
        truck.sort_values(by='tis', inplace=True)
        truck = truck.dropna()
        try:
            mask.value_counts()[True]
        except:
            continue
        if len(truck) == 0:
            continue
        print(z)
        try:
            Speed_violation.append(truck['osf'].value_counts()[True])
        except:
            Speed_violation.append(0)
        try:
            Harsh_Acc.append(truck['harsh_acceleration'].value_counts()[True])
        except:
            Harsh_Acc.append(0)
        try:
            Harsh_Break.append(truck['harsh_acceleration'].value_counts()[True])
        except:
            Harsh_Break.append(0)
        Numberplate.append(z)
        m = list(trip.query(f"vehicle_number=='{z}'")["transporter_name"])
        Transport_name.append(m[0])
        Tripcount.append(trip['vehicle_number'].value_counts()[z])
        Avg_spd.append(truck["spd"].mean())
        distance = 0.0
        lat = truck['lat'].tolist()
        lon = truck['lon'].tolist()
        lat1 = lat[1:]
        lon1 = lon[1:]
        lat1.append(lat[-1])
        lon1.append(lon[-1])
        dist = 0.0
        for i in range(len(lat)):
            dist = dist + (haversine((lat1[i], lon1[i]), (lat[i], lon[i]), unit='km'))
        Distance.append(dist)
    dict = {
        'License plate number': Numberplate,
        'Distance': Distance,
        'Number of Trips Completed': Tripcount,
        'Average Speed': Avg_spd,
        'Transporter Name': Transport_name,
        'Number of Speed Violations': Speed_violation,
        'Number of Harsh Accelaration':Harsh_Acc,
        'Number of Harsh Breaking': Harsh_Break
    }
    df = pd.DataFrame(dict)
    df.to_excel("output.xlsx", sheet_name='Report')
    return df

@app.route('/search', methods=['GET'])
def search():
    args = request.args
    x = args.get('startdate')
    y = args.get('enddate')
    start = datetime.datetime.fromtimestamp(int(x))
    end = datetime.datetime.fromtimestamp(int(y))
    start = start.strftime("%Y%m%d%H%M%S")
    end = end.strftime("%Y%m%d%H%M%S")

    trip = pd.read_csv('Trip-info.csv')
    trip['date_time'] = pd.to_datetime(trip['date_time'], format='%Y%m%d%H%M%S')

    mask = (trip['date_time'] > start) & (trip['date_time'] <= end)
    trip = trip.loc[mask]

    if len(trip) == 0:
        return ('Sorry there is no data avaliable in this time frame')

    print(len(trip['vehicle_number'].unique()))

    vno = trip['vehicle_number'].unique()
    print(vno)

    st = []
    fi = os.listdir('EOL-dump/')
    for i in vno:
        if i + '.csv' in fi:
            st.append(i)
    print(st)

    Numberplate = []
    Transport_name = []
    Speed_violation = []
    Avg_spd = []
    Distance = []
    Tripcount = []
    Harsh_Acc = []
    Harsh_Break = []
    for j in range(len(st)):
        z = st[j]
        col = ['tis', 'osf', 'lon', 'lat', 'spd']
        truck = pd.read_csv(f'EOL-dump/{z}.csv')
        truck['tis'] = pd.to_datetime(truck['tis'], unit='s')
        truck['tis'] = pd.to_datetime(truck['tis'], format='%Y%m%d%H%M%S')
        mask = (truck['tis'] >= start) & (truck['tis'] <= end)
        truck = truck.loc[mask]
        truck.sort_values(by='tis', inplace=True)
        truck = truck.dropna()
        try:
            mask.value_counts()[True]
        except:
            continue
        if len(truck) == 0:
            continue
        print(z)
        try:
            Speed_violation.append(truck['osf'].value_counts()[True])
        except:
            Speed_violation.append(0)
        try:
            Harsh_Acc.append(truck['harsh_acceleration'].value_counts()[True])
        except:
            Harsh_Acc.append(0)
        try:
            Harsh_Break.append(truck['harsh_acceleration'].value_counts()[True])
        except:
            Harsh_Break.append(0)
        Numberplate.append(z)
        m = list(trip.query(f"vehicle_number=='{z}'")["transporter_name"])
        Transport_name.append(m[0])
        Tripcount.append(trip['vehicle_number'].value_counts()[z])
        Avg_spd.append(truck["spd"].mean())
        distance = 0.0
        lat = truck['lat'].tolist()
        lon = truck['lon'].tolist()
        lat1 = lat[1:]
        lon1 = lon[1:]
        lat1.append(lat[-1])
        lon1.append(lon[-1])
        dist = 0.0
        for i in range(len(lat)):
            dist = dist + (haversine((lat1[i], lon1[i]), (lat[i], lon[i]), unit='km'))
        Distance.append(dist)

    dict = {
        'License plate number': Numberplate,
        'Distance': Distance,
        'Number of Trips Completed': Tripcount,
        'Average Speed': Avg_spd,
        'Transporter Name': Transport_name,
        'Number of Speed Violations': Speed_violation,
        'Number of Harsh Accelaration': Harsh_Acc,
        'Number of Harsh Breaking': Harsh_Break
    }

    df = pd.DataFrame(dict)
    df.to_excel("output.xlsx", sheet_name='Report')
    return send_file('output.xlsx', download_name='report.xlsx')


