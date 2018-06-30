from django.shortcuts import render
import requests

def home(request):
    data = {}
    test = False
    if 'image' in request.GET:
        label = request.GET['label']
        exposedport = request.GET['exposedport']
        image = request.GET['image']
        port = '8052'
        
        payload = {
            'Image':image,
            'HostConfig': {
                "PortBindings": {
                "4200/tcp": [{
                    "HostIp": "",
                    "HostPort": port
                    }
                ]}
            }
        }
        print(payload)
                   # 'Label':'{"question2" : label}'}
        url = 'http://192.168.52.130:3125/containers/create'
        response = requests.post(url, json=payload)
        if response.status_code == 201:
            test = True
            data = response.json()
        elif response.status_code == 400:
            data['message'] = payload
        elif response.status_code == 409:
            data['message'] = 'conflict'
        else:
            data['message'] = 'server error'
    return render(request, 'create.html', {'data': data, 'test': test})