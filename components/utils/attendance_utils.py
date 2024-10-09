import face_recognition
from geopy.distance import geodesic
from attendance.models import UserProfile


def check_geofence(lat, lon, geofence):
    distance = geodesic((lat, lon), (geofence.latitude, geofence.longitude)).meters
    return distance <= geofence.radius


def verify_image(user, uploaded_image):
    try:
        user_profile = UserProfile.objects.get(user=user)
        known_image_path = user_profile.known_image.path
        known_image = face_recognition.load_image_file(known_image_path)
        known_encoding = face_recognition.face_encodings(known_image)[0]
        unknown_image = face_recognition.load_image_file(uploaded_image)
        unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
        results = face_recognition.compare_faces([known_encoding], unknown_encoding)
        return results[0]
    except UserProfile.DoesNotExist:
        return False
    except IndexError:
        return False