# from transformers import pipeline
#
# translator = pipeline("translation", model="t5-base")
#
# translated_text = translator("teri esi tesi")
# import requests
#
# url = "https://google-translate1.p.rapidapi.com/language/translate/v2"
#
# payload = {
#     "q": "behenchod",
#     "target": "en",
#     "source": "hi"
# }
# headers = {
#     "content-type": "application/x-www-form-urlencoded",
#     "Accept-Encoding": "application/gzip",
#     "X-RapidAPI-Key": "fbf9842bd2mshce10357b7b39318p1b91b4jsndaf977b5923c",
#     "X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
# }
#
# response = requests.post(url, data=payload, headers=headers)
#
# print(response.json())
#
#
#
# # '''Detect'''
# # import requests
# #
# # url = "https://google-translate1.p.rapidapi.com/language/translate/v2/detect"
# #
# # payload = { "q": "randi ka choda" }
# # headers = {
# #     "content-type": "application/x-www-form-urlencoded",
# #     "Accept-Encoding": "application/gzip",
# #     "X-RapidAPI-Key": "fbf9842bd2mshce10357b7b39318p1b91b4jsndaf977b5923c",
# #     "X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
# # }
# #
# # response = requests.post(url, data=payload, headers=headers)
# #
# # print(((response.json())['data']['detections'][0][0]))