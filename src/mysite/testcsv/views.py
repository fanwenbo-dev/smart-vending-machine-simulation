from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse, Http404
import csv
from datetime import datetime
import os
from django.utils.http import urlencode

def update_csv(request):
    if request.method == "POST":
        # Get the drink value from POST + make it global
        global drink
        drink = int(request.POST.get('drink'))
        
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')) # csv file path
        csv_file_path = os.path.join(project_root, 'updt.csv')
        
        with open(csv_file_path, mode='r', newline='') as file: # csv number read
            reader = csv.DictReader(file)
            rows = list(reader)
            if rows:
                last_number = int(rows[-1]['number'])
            else:
                last_number = 0
        
        next_number = last_number + 1
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.now().strftime("%H:%M:%S")
        
        with open(csv_file_path, mode='a', newline='') as file: # update csv 
            writer = csv.writer(file)
            writer.writerow([next_number, current_date, current_time, drink])
        
        return redirect('payproc') #redirect payment processing
    
    return render(request, 'testcsv/webpage1.html') # else show default page

def csv_updated(request):
    template_mapping = {
        1: 'testcsv/webpage2_1.html',
        2: 'testcsv/webpage2_2.html',
        3: 'testcsv/webpage2_3.html',
        4: 'testcsv/webpage2_4.html',
        5: 'testcsv/webpage2_5.html',
        6: 'testcsv/webpage2_6.html',
        7: 'testcsv/webpage2_7.html',
        8: 'testcsv/webpage2_8.html',
        9: 'testcsv/webpage2_9.html',
        10: 'testcsv/webpage2_10.html'
    }
    template = template_mapping.get(drink)
    return render(request, template)


def rawcsv(request):
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))     # path to updt.csv
    csv_file_path = os.path.join(project_root, 'updt.csv')
    with open(csv_file_path, mode='r', newline='') as file:     # read current number
        reader = csv.DictReader(file)
        rows = list(reader)
    return HttpResponse(rows)

def payproc(request):
    return render(request, 'testcsv/webpage3.html')

def serve_image(request):
    image_path = os.path.join(os.path.dirname(__file__), 'templates', 'testcsv', 'images', 'full.jpg')
    if os.path.exists(image_path):
        return FileResponse(open(image_path, 'rb'), content_type='image/jpeg')
    else:
        raise Http404("Image not found")
    
def serve_qr_image(request, image_name):
    image_path = os.path.join(os.path.dirname(__file__), 'templates', 'testcsv', 'qrs', f'{image_name}.png')
    if os.path.exists(image_path):
        return FileResponse(open(image_path, 'rb'), content_type='image/png')
    else:
        raise Http404("Image not found")