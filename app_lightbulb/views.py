from django.shortcuts import render
from  rest_framework.generics import ListAPIView
from .serializers import Type_of_premises_Serializers, RoomTypeCategorySerializer, RoomTypeSerializer, LEDPanelSerializer
from .models import Type_of_premises, Room_Type_Category, Room_Type, LEDPanel

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




import math


# class LampCalculationAPIView(APIView):
#     parser_classes = [JSONParser]

#     LAMPS_LIST = [
#                 ############################## O'zim ####################################################  
#                 {"name": "LM-LBL 7W", "watt": 7, "lumen": 630, "diameter": 110, "weight": 0.21},
#                 {"name": "AK-LBL 12W", "watt": 12, "lumen": 1080, "diameter": 110, "weight": 0.21},

#                 ########################### CHET ########################################################
#             #     {"name": "ACQUA C 06 WH 4000K", "watt": 8, "lumen": 600, "diameter": 110, "weight": 0.21},
#             #     {"name": "ACQUA C 12 WH 4000K", "watt": 14, "lumen": 1200, "diameter": 150, "weight": 0.34},
#             #     {"name": "ACQUA C 18 WH 4000K", "watt": 22, "lumen": 2100, "diameter": 180, "weight": 0.36},
#             #     {"name": "ASM/S LED 1500 SCHOOL 4000K CRI90", "watt": 24, "lumen": 2200, "diameter": 1610, "weight": 0.36},
#             #     {"name": "BACK LED 595 STANDARD 4000K", "watt": 40, "lumen": 4000, "diameter": 575, "weight": 0.36},
#             #     {"name": "ALD UNI LED 600 4000K", "watt": 24, "lumen": 2000, "diameter": 630, "weight": 0.36},
#             #     {"name": "ALD UNI LED 1200 4000K", "watt": 30, "lumen": 2600, "diameter": 1240, "weight": 0.36},
#             #     {"name": "ALD UNI LED 1200 4000K CRI90", "watt": 30, "lumen": 2400, "diameter": 1240, "weight": 0.36},
#             #     {"name": "ALS.OPL UNI LED 1200 TH 4000K", "watt": 18, "lumen": 2000, "diameter": 12700, "weight": 0.36},
#             #     {"name": "ALS.OPL UNI LED 600x200 4000K CRI90", "watt": 18, "lumen": 1800, "diameter": 180, "weight": 0.36},
#             #     {"name": "ALS.OPL UNI LED 1200 4000K", "watt": 32, "lumen": 3600, "diameter": 1270, "weight": 0.36},
#             #     {"name": "ALS.OPL UNI LED 600x600 (36) 4000K", "watt": 32, "lumen": 4000, "diameter": 1270, "weight": 0.36},
#             #     {"name": "ALS.OPL UNI LED 1200 EM 4000K CRI90", "watt": 32, "lumen": 3200, "diameter": 1270, "weight": 0.36},
#             #     {"name": "ARCTIC STANDARD 1500 TH 4000K", "watt": 44, "lumen": 4500, "diameter": 1582, "weight": 0.36},
#             #     {"name": "ARCTIC.OPL ECO LED 1200 TH EM 5000K", "watt": 36, "lumen": 3400, "diameter": 1280, "weight": 0.36},
#             #     {"name": "ARS/R UNI LED 300 4000K", "watt": 16, "lumen": 1500, "diameter": 575, "weight": 0.36},
#             # 
#             ]

#     def post(self, request, *args, **kwargs):
#         try:
#             data = request.data
#             room_length = float(data.get('room_length', 0))
#             room_width = float(data.get('room_width', 0))
#             room_height = float(data.get('room_height', 0))
#             illumination = float(data.get('illumination', 300))
#             reserve_factor = float(data.get('reserve_factor', 1.5))
#             reflection_factors = data.get('reflection_factors', [80, 80, 30])

#             total_area = room_length * room_width
#             effective_illumination = illumination * (sum(reflection_factors) / 300)
#             required_lumen = effective_illumination * total_area * reserve_factor

#             best_choice = None
#             best_lamps_count = 0
#             min_total_watt = float('inf')

#             for lamp in self.LAMPS_LIST:
#                 lamp_count = max(1, math.ceil(required_lumen / lamp['lumen']))
#                 total_watt = lamp['watt'] * lamp_count
#                 efficiency = lamp['lumen'] / lamp['watt']

#                 if total_area < 10 and lamp['diameter'] < 600:
#                     is_suitable = True
#                 elif room_height > 3.5 and lamp['lumen'] > 3000:
#                     is_suitable = True
#                 else:
#                     is_suitable = True

#                 if is_suitable and (total_watt < min_total_watt or efficiency > best_choice.get('efficiency', 0)):
#                     best_choice = lamp.copy()
#                     best_choice['efficiency'] = efficiency
#                     best_lamps_count = lamp_count
#                     min_total_watt = total_watt

#             if best_choice:
#                 response_data = {
#                     "room_length": room_length,
#                     "room_width": room_width,
#                     "room_height": room_height,
#                     "illumination": illumination,
#                     "reserve_factor": reserve_factor,
#                     "tavsiya_qilinadi": {
#                         "lamp": best_choice["name"],
#                         "watt": best_choice["watt"],
#                         "lumen": best_choice["lumen"],
#                         "diameter": best_choice["diameter"],
#                         "weight": best_choice["weight"],
#                         "samaradorlik": round(best_choice['efficiency'], 2),
#                         "yoruglik": best_choice["lumen"] * best_lamps_count,
#                         "number_of_lamps": best_lamps_count,
#                     }
#                 }
#                 return Response(response_data, status=status.HTTP_200_OK)
#             else:
#                 return Response({"status": "error", "message": "Mos lampa topilmadi."}, status=status.HTTP_400_BAD_REQUEST)

#         except Exception as e:
#             return Response({"status": "error", "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LampCalculationAPIView(APIView):
    parser_classes = [JSONParser]

    LAMPS_LIST = [
        {"name": "LM-LBL 5W E27", "watt": 5, "lumen": 450, "diameter": 110, "weight": 0.21},
        {"name": "LM-LBL E27", "watt": 7, "lumen": 630, "diameter": 110, "weight": 0.21},
        {"name": "LM-LBL 10W E27", "watt": 10, "lumen": 900, "diameter": 110, "weight": 0.21},
        {"name": "LM-LBL 12W E27", "watt": 12, "lumen": 1080, "diameter": 110, "weight": 0.21},
        {"name": "LM-SLPS 18W", "watt": 18, "lumen": 630, "diameter": 110, "weight": 0.21},
        {"name": "LM-SLPS 24W", "watt": 24, "lumen": 1860, "diameter": 110, "weight": 0.21},
        {"name": "LM - LPSS 18W", "watt": 18, "lumen": 2070, "diameter": 110, "weight": 0.21},
        {"name": "LM - LPSS 12W", "watt": 12, "lumen": 870, "diameter": 110, "weight": 0.21},

    ]

    def post(self, request, *args, **kwargs):
        data = request.data
        room_length = float(data.get('room_length', 0))
        room_width = float(data.get('room_width', 0))
        room_height = float(data.get('room_height', 0))
        illumination = float(data.get('illumination', 300))
        table_height = float(data.get('table_height', 0))
        lamp_height = float(data.get('lamp_height', 0))
        
        # 1. Xona yuzasi
        S = room_length * room_width
        room_height_1 = room_height
        # 2. Yorug'lik oqimi
        light_flux = illumination * S
        room_height  = room_height - table_height  - lamp_height/100
        # 3. Xona balandligi koeffitsiyenti
        if 0 <= room_height < 4:
            height_coef = 1.2
        elif 4 <= room_height < 6:
            height_coef = 1.6
        else:
            height_coef = 1.8
        
        # 4. To'liq kerakli yorug'lik oqimi
        total_lx = light_flux * height_coef
        
        # 5. Xonaga kerak bo'ladigan lampochka sonini aniqlash
        i = (room_length * room_width) / (room_height * (room_length + room_width))
        
        if i < 1:
            lamp_count = 4
        elif 1 <= i < 2:
            lamp_count = 8
        elif 2 <= i < 3:
            lamp_count = 16
        else:
            lamp_count = 25
        
        # 6. Eng mos keladigan lampochkani tanlash
        best_choice = min(self.LAMPS_LIST, key=lambda lamp: abs((lamp['lumen'] * lamp_count) - total_lx))
        
        response_data = {
            "room_length": room_length,
            "room_width": room_width,
            "room_height": room_height_1,
            "illumination": illumination,
            "table_height": table_height,
            "tavsiya_qilinadi": {
                "lamp": best_choice["name"],
                "watt": best_choice["watt"],
                "lumen": best_choice["lumen"],
                "diameter": best_choice["diameter"],
                "weight": best_choice["weight"],
                "number_of_lamps": lamp_count,
            }
        }
        return Response(response_data)




class RoomCalculationAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            width = float(request.data.get('width'))  # xona eni
            length = float(request.data.get('length'))  # xona bo'yi
            height = float(request.data.get('height'))  # xona bo'yi
            lk_id = int(request.data.get('lk_id'))     # Room_Type ID
            luks = int(request.data.get('luks'))   

            # Xona yuzasi
            area = width * length

            # Room_Type ni topamiz
            room = get_object_or_404(Room_Type, id=lk_id)

            # Umumiy LK va quvvat hisoblash
            energy = 90  # doimiy qiymat
            umumiy_lk = area * luks
            quvvat = umumiy_lk / energy

            return Response({
                "quvvat": round(quvvat, 2),
                "umumiy_lk" : umumiy_lk,
                "Xona_nomi": room.name,
                "Luks": luks,
                "rang_uzatish_index": room.ra,
                "pulsatsiya": room.k,
                "UGR": room.ugr,
                "Tavsiya etilgan lampalar": room.recommended_lamps,
                "eni":width,
                "boyi":length,
                "balandlik":height,
            })

        except (TypeError, ValueError):
            return Response({"error": "Ma'lumotlar noto‘g‘ri formatda berilgan."}, status=status.HTTP_400_BAD_REQUEST)
        except Room_Type.DoesNotExist:
            return Response({"error": "Room_Type topilmadi."}, status=status.HTTP_404_NOT_FOUND)
        

class LEDPanelListAPIView(ListAPIView):
    serializer_class = LEDPanelSerializer

    def get_queryset(self):
        return LEDPanel.objects.all().order_by('-power')  
    


from openai import OpenAI
import os
from .serializers import LightingAskSerializer

class LightingChatAPIView(APIView):


    def post(self, request):
        s = LightingAskSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        d = s.validated_data

        width = d["width"]
        length = d["length"]
        height = d["height"]
        reflectance = d["reflectance"]
        required_lux = d["required_lux"]
        room_type = d.get("room_type", "turar joy xonasi")

        area = width * length  # m^2

        # Siz xohlasangiz, shu joyda o'zingiz UF/MF ni statik yoki dinamik berasiz
        # (GPT dan ham so'rab tavsiya oldirsa bo'ladi)
        base_lumens = required_lux * area

        prompt = f"""
Sen yoritish muhandisi kabi javob ber.
Kiritilgan parametrlar:
- Xona: {width}m x {length}m x {height}m (maydon: {area:.2f} m²)
- Xona turi: {room_type}
- Minimal yoritish: {required_lux} Lk
- Rang qaytish koeffitsiyentlari (ship/devor/pol): {reflectance}


Vazifa:
1) Qanday LED lampochka (Watt va lumen) va nechta dona kerakligini tavsiya qil.
2) 2-3 ta variant ber (masalan: 4x15W, 5x12W va h.k.).
3) Har variant uchun taxminiy umumiy lumenni yoz.
4) Qisqa, aniq, o‘zbekcha yoz.
"""

        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        resp = client.responses.create(
            model="gpt-4o-mini",
            input=prompt,
        )

        return Response({
            "inputs": {
                "width": width,
                "length": length,
                "height": height,
                "area_m2": round(area, 2),
                "reflectance": reflectance,
                "required_lux": required_lux,
                "base_lumens_lux_x_area": round(base_lumens, 0),
            },
            "answer_text": resp.output_text,
        })