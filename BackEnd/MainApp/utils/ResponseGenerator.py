from django.http import HttpResponse
import json
class ResponseFactory:
	def __init__(self) -> None:
		pass

	@staticmethod
	def getSucessful(msg, data) -> HttpResponse:
		jason = dict()
		jason["code"] = 200
		jason["msg"] = msg
		jason["data"] = data
		return HttpResponse(json.dumps(jason))
	
	@staticmethod
	def getError(msg, data) -> HttpResponse:
		jason = dict()
		jason["code"] = 404
		jason["msg"] = msg
		jason["data"] = data
		return HttpResponse(json.dumps(jason))
	
	@staticmethod
	def getInternalServerError(msg, data) -> HttpResponse:
		jason = dict()
		jason["code"] = 404
		jason["msg"] = msg
		jason["data"] = data
		return HttpResponse(json.dumps(jason))