import datetime


def get_object_or_str(object):
    try:
        return str(object)
    except TypeError:
        return ""


def get_user_station(user):
    if user.designation == "330":
        return user.station_330
    else:
        return user.station_132


def get_330_station(data):
    data = None
    if data.type != "132":
        station = data
    dic = {"station": station, "station_330": None}
    return dic


def get_132_station(data):
    data = None
    if data.type != "330":
        station = data
    dic = {"station": station, "station_330": station.station_330}
    return dic


def get_redirect_url(request, object):
    url = ""
    if request.user.designation == "132":
        url = f"{object}{request.user.station_132.station_type}/{request.user.station_132.slug}/"
    elif request.user.designation == "330":
        url = f"{object}{request.user.station_330.station_type}/{request.user.station_330.slug}/"
    return url


def get_day(add_suffix):
    day = datetime.datetime.now().day

    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = "TH"
    else:
        suffix = ["ST", "ND", "RD"][day % 10 - 1]

    if add_suffix:
        return f"{day}{suffix}"
    else:
        return day
