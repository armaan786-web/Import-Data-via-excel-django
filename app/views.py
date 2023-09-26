from django.shortcuts import render
from .models import Employee,ExcelFile
import pandas as pd
from django.http import JsonResponse
from django.conf import settings
# Create your views here.

def export_Data_to_excel(request):
    objs = Employee.objects.all()
    data = []
    for obj in objs:
        data.append({
            'employee_name':obj.employee_name,
            'employee_contact':obj.employee_contact,
            'employee_address':obj.employee_address
        })
    pd.DataFrame(data).to_excel('output.xlsx')
    return JsonResponse({
        'status':200
    })




# def import_to_db(request):
#     if request.method == "POST":
#         file = request.FILES['files']
#         print("fileee",file)
#         obj = ExcelFile.objects.create(
#             file = file

#         )
        
#         path = str(obj.file)
#         print(f'{settings.BASE_DIR}/{path}')
#         df = pd.read_excel(path)
#         for  d in df.values:
#             print("ddddddd",d)


#         print(df)

#     return render(request,'excel.html')



def import_to_db(request):
    if request.method == "POST":
        file = request.FILES['files']
        path = str(file)
        print(f'File path: {settings.BASE_DIR}/{path}')

        try:
            df = pd.read_excel(file)
            for row in df.itertuples(index=False):
                # Assuming your Excel columns are in the order: employee_name, employee_contact, employee_address
                employee = Employee(
                    employee_name=row[0],
                    employee_contact=row[1],
                    employee_address=row[2]
                )
                employee.save()

            print("Data imported successfully.")
        except Exception as e:
            print(f"Error importing data: {e}")

    return render(request, 'excel.html')