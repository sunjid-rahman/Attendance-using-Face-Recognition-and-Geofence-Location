from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Attendance, Geofence
from .serializers import AttendanceSerializer
from django.shortcuts import get_object_or_404
from components.utils.attendance_utils import check_geofence, verify_image


class AttendanceView(APIView):
    def post(self, request):
        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            lat = serializer.validated_data['latitude']
            lon = serializer.validated_data['longitude']
            image = request.FILES['image']

            # Verify the uploaded image with the user's stored known image
            is_verified = verify_image(user, image)
            # Assuming user's geofence
            geofences = Geofence.objects.all()  # Get all geofences
            in_geofence = any(check_geofence(lat, lon, gf) for gf in geofences)

            if is_verified and in_geofence:
                serializer.save(user=user, is_verified=True)
                return Response({"message": "Attendance marked successfully.", "is_image_matched": is_verified, "is_location_matched": in_geofence}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "Failed to verify attendance." , "is_image_matched": is_verified, "is_location_matched": in_geofence}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
