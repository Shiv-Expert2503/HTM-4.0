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
#     "q": "abbusiveword",
#     "target": "en",
#     "source": "hi"
# }
# headers = {
#     "content-type": "application/x-www-form-urlencoded",
#     "Accept-Encoding": "application/gzip",
#     "X-RapidAPI-Key": "appikey",
#     "X-RapidAPI-Host": "host"
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
# # payload = { "q": "abusiveword" }
# # headers = {
# #     "content-type": "application/x-www-form-urlencoded",
# #     "Accept-Encoding": "application/gzip",
# #     "X-RapidAPI-Key": "apikey",
# #     "X-RapidAPI-Host": "host"
# # }
# #
# # response = requests.post(url, data=payload, headers=headers)
# #
# # print(((response.json())['data']['detections'][0][0]))
