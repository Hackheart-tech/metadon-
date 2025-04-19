from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os

def get_exif_data(image):
    exif_data = {}
    img = Image.open(image)
    info = img._getexif()
    if info is None:
        return exif_data
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        if decoded == "GPSInfo":
            gps_data = {}
            for t in value:
                sub_decoded = GPSTAGS.get(t, t)
                gps_data[sub_decoded] = value[t]
            exif_data[decoded] = gps_data
        else:
            exif_data[decoded] = value
    return exif_data

def convert_to_degrees(value):
    d = float(value[0][0]) / float(value[0][1])
    m = float(value[1][0]) / float(value[1][1])
    s = float(value[2][0]) / float(value[2][1])
    return d + (m / 60.0) + (s / 3600.0)

def get_gps_coordinates(gps_info):
    lat = convert_to_degrees(gps_info["GPSLatitude"])
    lon = convert_to_degrees(gps_info["GPSLongitude"])
    if gps_info["GPSLatitudeRef"] != "N":
        lat = -lat
    if gps_info["GPSLongitudeRef"] != "E":
        lon = -lon
    return (lat, lon)

def extract_geo(image_path):
    exif_data = get_exif_data(image_path)
    gps_info = exif_data.get("GPSInfo")
    if gps_info:
        lat, lon = get_gps_coordinates(gps_info)
        print(f"[+] {image_path} :")
        print(f"    📍 Latitude: {lat}")
        print(f"    📍 Longitude: {lon}")
        print(f"    🌍 Google Maps: https://www.google.com/maps?q={lat},{lon}\n")
    else:
        print(f"[-] {image_path} : pas de géolocalisation trouvée.\n")

# 🔁 Dossier d'images
path = "./photos/"
for file in os.listdir(path):
    if file.lower().endswith((".jpg", ".jpeg")):
        extract_geo(os.path.join(path, file))

