import mod.server.extraServerApi as serverApi
levelId = serverApi.GetLevelId()


class Model:

	@staticmethod
	def GetEntityScale(entityId):
		comp = serverApi.GetEngineCompFactory().CreateScale(entityId)
		return comp.GetEntityScale()

	@staticmethod
	def GetModelName(entityId):
		comp = serverApi.GetEngineCompFactory().CreateModel(entityId)
		return comp.GetModelName()

	@staticmethod
	def SetEntityScale(entityId, scale):
		comp = serverApi.GetEngineCompFactory().CreateScale(entityId)
		return comp.SetEntityScale(entityId, scale)

	@staticmethod
	def SetModel(entityId, modelName):
		comp = clientApi.GetEngineCompFactory().CreateModel(entityId)
		return comp.SetModelPerspectiveEffect(modelName)