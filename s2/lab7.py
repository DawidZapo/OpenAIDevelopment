from prompts import create_recognize_city_prompt
from utils import create_multi_image_request

images = ['./image_files/city1.png', './image_files/city2.png', './image_files/city3.png', './image_files/city4.png']

response = create_multi_image_request(images, create_recognize_city_prompt())
print(response)