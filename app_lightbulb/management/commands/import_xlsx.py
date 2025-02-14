import pandas as pd
from django.core.management.base import BaseCommand
from app_lightbulb.models import Room_Type_Category, Room_Type

class Command(BaseCommand):
    help = 'Import room types and categories from an Excel file'

    def handle(self, *args, **kwargs):
        # File path
        file_path = "/home/user/backend/cal/app_lightbulb/management/commands/x.xlsx"
        
        # Read the Excel file
        data = pd.read_excel(file_path)

        # Strip all column names to remove any extra spaces
        data.columns = data.columns.str.strip()
        
        # Iterate through each row in the Excel file
        for index, row in data.iterrows():
            # Handle Room_Type_Category (parent)
            root_category_name = str(row['Room_Type_Category  name']).strip()  
            root_category, _ = Room_Type_Category.objects.get_or_create(name=root_category_name, parent=None)
            
            # Handle category (child of the root category)
            category_name = str(row['category']).strip() if pd.notna(row['category']) else None
            if category_name:
                category, _ = Room_Type_Category.objects.get_or_create(name=category_name, parent=root_category)
            else:
                category = root_category

            # Ensure all fields are handled safely
            def safe_str(value):
                return str(value).strip() if pd.notna(value) else ""

            table_height = (
                float(row["table_height"]) 
                if pd.notna(row["table_height"]) and str(row["table_height"]).strip() != "-" 
                else 0
            )
            color_tem = safe_str(row["color_tem"])
            light_type = safe_str(row["light_type"])
            recommended_lamps = safe_str(row["recommended_lamps"])

            # Create Room_Type instance
            try:
                Room_Type.objects.create(
                    category=category,
                    lk=int(row['lk']),
                    ra=int(row['ra']),
                    k=int(row['k']) if pd.notna(row['k']) else None,
                    table_height=table_height,
                    color_tem=color_tem,
                    light_type=light_type,
                    recommended_lamps=recommended_lamps
                )
            except Exception as e:
                print(f"Error processing row {index + 1}: {e}")
        
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
