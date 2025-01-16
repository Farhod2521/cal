from django.shortcuts import render
from  rest_framework.generics import ListAPIView
from .serializers import Type_of_premises_Serializers
from .models import Type_of_premises
from .serializers import CalculateLampsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser

class Type_of_premises_ListApiview(ListAPIView):
    serializer_class =  Type_of_premises_Serializers
    queryset = Type_of_premises.objects.all()
    




















class LampCalculationAPIView(APIView):
    parser_classes = [JSONParser]

    def post(self, request, *args, **kwargs):
        try:
            # Kutilgan ma'lumotlarni olish (foydalanuvchidan kelgan malumotlar)
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
            ]

            # Lampaning fluxini hisoblash (lumen)
            lamp_flux = lamp_lumen  # Lumenni kiritgan bo'lsangiz, uni ishlatamiz

            # Kerakli lampalar sonini hisoblash
            utilization_factor = 0.6  # Ishlatish koeffitsienti (taxminiy)
            maintenance_factor = reserve_factor  # Zaxira koeffitsienti

            # Lampalar sonini hisoblash
            required_lamps_count = (effective_illumination * total_area) / (lamp_flux * utilization_factor * maintenance_factor)
            required_lamps_count = max(1, round(required_lamps_count))  # Kamida 1 lampochka kerak
            print(required_lamps_count)

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

            return Response({
                "status": "success",
                "jami_lampochka": required_lamps_count,
                "bir_kunda_tok_ishlatadi": total_watt_user_lamp * working_hours_per_day,  # Kuni davomida ishlatilgan tok
                "bir_kunda_som": total_cost,  # Kuni davomida to'lanadigan qiymat
                "tavsiya_qilinadi": {
                    "lamp": best_choice["name"],
                    "watt": best_choice["watt"],
                    "lumen": best_choice["lumen"],
                    "diameter": best_choice["diameter"],
                    "weight": best_choice["weight"],
                    "tok_teyadi": energy_saved,  # Tejash mumkin bo'lgan energiya
                    "foyda_som": energy_saved_cost,  # Tejash mumkin bo'lgan pul miqdori
                    "yoruglik": best_choice["lumen"] * best_lamps_count,  # Yangi lampochkalar bilan olingan yorug'lik
                    "number_of_lamps": best_lamps_count  # Nechta lampa kerak
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
