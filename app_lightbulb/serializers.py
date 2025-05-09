from rest_framework import serializers

from .models import Type_of_premises, Room_Type_Category, Room_Type, LEDPanel


class Type_of_premises_Serializers(serializers.ModelSerializer):
    class Meta:
        model =  Type_of_premises
        fields = "__all__"




class RoomTypeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Room_Type_Category
        fields = '__all__'

class RoomTypeSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Room_Type
        fields = '__all__'


class CalculateLampsSerializer(serializers.Serializer):
    room_length = serializers.FloatField()
    room_width = serializers.FloatField()
    room_height = serializers.FloatField()
    reflection_factors = serializers.ListField(
        child=serializers.IntegerField(), required=False, default=[80, 80, 30]
    )
    illumination = serializers.FloatField()
    working_surface_height = serializers.FloatField(required=False, default=0)
    reserve_factor = serializers.FloatField(default=1.4)
    lamp_flux = serializers.FloatField(default=4000)


class LEDPanelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LEDPanel
        fields = '__all__'