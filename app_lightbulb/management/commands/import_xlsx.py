import pandas as pd
from django.core.management.base import BaseCommand
from app_lightbulb.models import Room_Type_Category, Room_Type

class Command(BaseCommand):
    help = 'Import room types and categories from an Excel file'

    def handle(self, *args, **kwargs):
        file_path = "/home/user/backend/cal/app_lightbulb/management/commands/x.xlsx"
        
        try:
            data = pd.read_excel(file_path)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error reading Excel file: {e}"))
            return
        
        # Ustun nomlarini tozalash
        data.columns = data.columns.str.strip()

        def safe_int(value):
            if pd.isna(value) or value in ["-", "", None]:
                return 0
            try:
                return int(float(str(value).replace("*", "").strip()))
            except ValueError:
                return 0
        
        def safe_str(value):
            return str(value).strip() if pd.notna(value) else ""
        
        def safe_float(value):
            try:
                return float(value) if pd.notna(value) else 0.0
            except ValueError:
                return 0.0

        for index, row in data.iterrows():
            category_name = safe_str(row.get('category'))
            sub_category_name = safe_str(row.get('sub_category'))
            
            # Qatorlarni chop etish (debugging)
            print(f"Row {index + 1} - Category: '{category_name}', Sub_category: '{sub_category_name}'")

            if not category_name or not sub_category_name:
                self.stderr.write(self.style.WARNING(f"Skipping row {index + 1}: Missing category or sub_category"))
                continue
            
            # Kategoriyalarni yaratish
            root_category, _ = Room_Type_Category.objects.get_or_create(name=category_name, parent=None)
            sub_category, _ = Room_Type_Category.objects.get_or_create(name=sub_category_name, parent=root_category)
            
            try:
                Room_Type.objects.create(
                    category=sub_category,
                    name=sub_category_name,
                    table_height=safe_float(row.get('table_height')),
                    lk=safe_int(row.get('lk')),
                    ra=safe_int(row.get('ra')),
                    k=safe_int(row.get('k')),    
                    ugr=safe_str(row.get('ugr')),
                    recommended_lamps=safe_str(row.get('recommended_lamps'))
                )
                self.stdout.write(self.style.SUCCESS(f"Row {index + 1} imported successfully"))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error processing row {index + 1}: {e}"))
        
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
