from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from .models import Region, District
import json

class RegionDistrictAPIView(APIView):
    def post(self, request):
        try:
            data = request.data.get('regions', [])
            
            for region_data in data:
                region_name = region_data.get('name')
                districts_data = region_data.get('districts', [])
                
                region, _ = Region.objects.get_or_create(name=region_name)
                
                for district_data in districts_data:
                    District.objects.create(
                        region=region,
                        name=district_data.get('name'),
                        average_temperature=district_data.get('average_temperature'),
                        time=district_data.get('time')
                    )
            
            return Response({
                'message': 'Maʼlumotlar muvaffaqiyatli saqlandi',
                'saved_regions': len(data)
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        """Get all regions with their districts"""
        regions = Region.objects.all()
        data = []
        
        for region in regions:
            region_data = {
                'name': region.name,
                'districts': []
            }
            
            districts = District.objects.filter(region=region)
            for district in districts:
                region_data['districts'].append({
                    'name': district.name,
                    'average_temperature': district.average_temperature,
                    'time': district.time
                })
            
            data.append(region_data)
        
        return Response({
            'regions': data
        }, status=status.HTTP_200_OK)
    

