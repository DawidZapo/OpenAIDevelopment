import json

import requests

from prompts import create_photo_enhance_prompt, create_person_description
from utils import get_centrala_url, create_payload, get_poligon_key, create_query_payload, create_process_image_request, \
    create_process_image_request_from_urls

image_url = '/dane/barbara/'
start_images = ['IMG_559.PNG', 'IMG_1410.PNG', 'IMG_1443.PNG', 'IMG_1444.PNG']

images_fix_array = []
for image in start_images:
    answer = create_process_image_request_from_urls([get_centrala_url() + image_url + image], create_photo_enhance_prompt())
    print(answer)
    images_fix_array.append({image: answer})


for image_dict in images_fix_array:
    for filename, action in image_dict.items():
        if action != 'NONE':

            automat_response = requests.post(
                get_centrala_url() + '/report',
                json=create_payload("photos", get_poligon_key(), action + " " + filename)
            )
            print(json.loads(automat_response.text)['message'])

ready_images = ['IMG_1410_FXER.PNG', 'IMG_1443_FT12.PNG', 'IMG_559_NRR7.PNG']
ready_images_url= [get_centrala_url() + image_url + img for img in ready_images]


person_description = create_process_image_request_from_urls(ready_images_url, create_person_description())

centrala_answer = requests.post(get_centrala_url() + '/verify', json=create_payload("photos", get_poligon_key(), person_description))
print(centrala_answer.text)