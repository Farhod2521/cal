from django.shortcuts import render
from  rest_framework.generics import ListAPIView
from .serializers import Type_of_premises_Serializers, RoomTypeCategorySerializer, RoomTypeSerializer
from .models import Type_of_premises, Room_Type_Category, Room_Type

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser

class Type_of_premises_ListApiview(ListAPIView):
    serializer_class =  Type_of_premises_Serializers
    queryset = Type_of_premises.objects.all()
    






class RoomTypeCategoryListView(ListAPIView):
    serializer_class = RoomTypeCategorySerializer

    def get_queryset(self):
        # Faqat parent=None bo'lganlar
        return Room_Type_Category.objects.filter(parent__isnull=True)

# View to list categories by parent ID
class RoomTypeCategoryByParentView(ListAPIView):
    serializer_class = RoomTypeCategorySerializer

    def get_queryset(self):
        # URL orqali uzatilgan parent_id ni olish
        tree_id = self.kwargs.get('tree_id')
        if tree_id is not None:
            return Room_Type_Category.objects.filter(tree_id=tree_id)
        return Room_Type_Category.objects.none()  # Agar parent_id bo'lmasa bo'sh queryset

# View to list Room Types by category ID
class RoomTypeListView(ListAPIView):
    serializer_class = RoomTypeSerializer

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return Room_Type.objects.filter(category_id=category_id)
    








from django.shortcuts import get_object_or_404

class RoomTypeCategoryAPIView(APIView):
    def get(self, request, category_id=None):
        """
        Kategoriyalarni daraxt ko'rinishida chiqarish.
        Agar category_id berilsa, shu kategoriya ichidagi subkategoriyalar, minikategoriyalar va mikrokategoriyalar ham qaytadi.
        """
        if category_id:
            category = get_object_or_404(Room_Type_Category, id=category_id)
            subcategories = category.children.all()

            subcategory_data = []
            for sub in subcategories:
                mini_categories = sub.children.all()

                mini_data = []
                for mini in mini_categories:
                    micro_categories = mini.children.all()
                    mini_data.append({
                        "id": mini.id,
                        "name": mini.name,
                        "microcategories": RoomTypeCategorySerializer(micro_categories, many=True).data
                    })

                subcategory_data.append({
                    "id": sub.id,
                    "name": sub.name,
                    "minicategories": mini_data
                })

            rooms = Room_Type.objects.filter(category=category)
            return Response({
                "subcategories": subcategory_data,
                "rooms": RoomTypeSerializer(rooms, many=True).data
            }, status=status.HTTP_200_OK)
        else:
            categories = Room_Type_Category.objects.filter(parent__isnull=True)
            return Response(RoomTypeCategorySerializer(categories, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = RoomTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)  # Xatolikni tekshirish uchun
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)










class LampCalculationAPIView(APIView):
    parser_classes = [JSONParser]

    def post(self, request, *args, **kwargs):
        try:
            # Kutilgan ma'lumotlarni olish (foydalanuvchidan kelgan ma'lumotlar)
            data = request.data
            room_length = float(data.get('room_length', 0))  # Xona uzunligi (metr)
            room_width = float(data.get('room_width', 0))    # Xona kengligi (metr)
            room_height = float(data.get('room_height', 0))  # Xona balandligi (metr)
            reflection_factors = data.get('reflection_factors', [80, 80, 30])  # Oqimlarning qaytish koeffitsienti
            illumination = float(data.get('illumination', 300))  # Kerakli yoritish (lux)
            reserve_factor = float(data.get('reserve_factor', 1.4))  # Zaxira koeffitsienti (odam tomonidan kiritilgan)
            lamp_watt = float(data.get('lamp_watt', 8))  # Lampaning quvvati (Watt)
            lamp_lumen = float(data.get('lamp_lumen', 600))  # Lampaning yorug'lik oqimi (lumen)

            # Agar lampaning quvvati yoki lumen kiritilmagan bo'lsa, xato
            if lamp_watt == 0 or lamp_lumen == 0:
                return Response({"status": "error", "message": "Lamp watt and lumen must be provided."}, status=status.HTTP_400_BAD_REQUEST)

            # Xonani umumiy maydoni
            total_area = room_length * room_width

            # Reflection factors orqali samarali yoritishni hisoblash
            effective_illumination = illumination * (sum(reflection_factors) / 300)

            # Lampalar ro'yxati
            lamps_list = [
                {"name": "ACQUA C 06 WH 4000K", "watt": 8, "lumen": 600, "diameter": 110, "weight": 0.21},
                {"name": "ACQUA C 12 WH 4000K", "watt": 14, "lumen": 1200, "diameter": 150, "weight": 0.34},
                {"name": "ACQUA C 18 WH 4000K", "watt": 22, "lumen": 2100, "diameter": 180, "weight": 0.36},
                {"name": "ASM/S LED 1500 SCHOOL 4000K CRI90", "watt": 24, "lumen": 2200, "diameter": 1610, "weight": 0.36},
                {"name": "BACK LED 595 STANDARD 4000K", "watt": 40, "lumen": 4000, "diameter": 575, "weight": 0.36},
                {"name": "ALD UNI LED 600 4000K", "watt": 24, "lumen": 2000, "diameter": 630, "weight": 0.36},
                {"name": "ALD UNI LED 1200 4000K", "watt": 30, "lumen": 2600, "diameter": 1240, "weight": 0.36},
                {"name": "ALD UNI LED 1200 4000K CRI90", "watt": 30, "lumen": 2400, "diameter": 1240, "weight": 0.36},
                {"name": "ALS.OPL UNI LED 1200 TH 4000K", "watt": 18, "lumen": 2000, "diameter": 12700, "weight": 0.36},
                {"name": "ALS.OPL UNI LED 600x200 4000K CRI90", "watt": 18, "lumen": 1800, "diameter": 180, "weight": 0.36},
                {"name": "ALS.OPL UNI LED 1200 4000K", "watt": 32, "lumen": 3600, "diameter": 1270, "weight": 0.36},
                {"name": "ALS.OPL UNI LED 600x600 (36) 4000K", "watt": 32, "lumen": 4000, "diameter": 1270, "weight": 0.36},
                {"name": "ALS.OPL UNI LED 1200 EM 4000K CRI90", "watt": 32, "lumen": 3200, "diameter": 1270, "weight": 0.36},
                {"name": "ARCTIC STANDARD 1500 TH 4000K", "watt": 44, "lumen": 4500, "diameter": 1582, "weight": 0.36},
                {"name": "ARCTIC.OPL ECO LED 1200 TH EM 5000K", "watt": 36, "lumen": 3400, "diameter": 1280, "weight": 0.36},
                {"name": "ARS/R UNI LED 300 4000K", "watt": 16, "lumen": 1500, "diameter": 575, "weight": 0.36},



            ]
            # Lampaning fluxini hisoblash (lumen)
            lamp_flux = lamp_lumen  # Lumenni kiritgan bo'lsangiz, uni ishlatamiz

            # Kerakli lampalar sonini hisoblash
            utilization_factor = 0.6  # Ishlatish koeffitsienti (taxminiy)
            maintenance_factor = reserve_factor  # Zaxira koeffitsienti

            # Lampalar sonini hisoblash
            required_lamps_count = (effective_illumination * total_area) / (lamp_flux * utilization_factor * maintenance_factor)
            required_lamps_count = max(1, round(required_lamps_count))  # Kamida 1 lampochka kerak

            # Asl lampaning umumiy quvvati va yorug'lik
            total_watt_user_lamp = lamp_watt * required_lamps_count
            total_lumen_user_lamp = lamp_lumen * required_lamps_count

            # Eng samarali energiya sarflaydigan lampochkani topish
            best_choice = None
            min_total_watt = float('inf')
            best_lamps_count = 0
            for lamp in lamps_list:
                # Har bir lampaning kerakli sonini hisoblash
                lamp_count = round((effective_illumination * total_area) / (lamp['lumen'] * utilization_factor * maintenance_factor))
                lamp_count = max(1, lamp_count)  # Kamida 1 lampochka kerak

                # Lampaning umumiy quvvati va yorug'lik
                total_watt = lamp['watt'] * lamp_count
                total_lumen = lamp['lumen'] * lamp_count

                # Eng kam energiya sarflaydigan lampochkani tanlash
                if total_watt < min_total_watt:
                    min_total_watt = total_watt
                    best_choice = lamp
                    best_lamps_count = lamp_count

            # Energiya tejashni hisoblash
            energy_saved = total_watt_user_lamp - min_total_watt

            # Kuni davomida tok sarfi va qiymatini hisoblash
            working_hours_per_day = 5  # Bitta lampochka kuniga necha soat ishlaydi
            cost_per_kwh = 450  # 1 kWh = 450 so'm
            total_cost = (total_watt_user_lamp * working_hours_per_day) / 1000 * cost_per_kwh
            energy_saved_cost = (energy_saved * working_hours_per_day) / 1000 * cost_per_kwh

            response_data = {
                "room_length": room_length,
                "room_width": room_width,
                "room_height": room_height,
                "reflection_factors": reflection_factors,
                "illumination": illumination,
                "working_surface_height": 0,
                "reserve_factor": reserve_factor,
                "tavsiya_qilinadi": {
                    "lamp": best_choice["name"],
                    "watt": best_choice["watt"],
                    "lumen": best_choice["lumen"],
                    "diameter": best_choice["diameter"],
                    "weight": best_choice["weight"],
                    "tok_teyadi": round(energy_saved, 2),
                    "foyda_som": round(energy_saved_cost, 2),
                    "yoruglik": best_choice["lumen"] * best_lamps_count,
                    "number_of_lamps": best_lamps_count
                }
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
