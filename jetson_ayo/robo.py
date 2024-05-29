from roboflow import Roboflow

rf = Roboflow(api_key="yxsWU7bMscq8Jcsv4qG0")
project = rf.workspace().project("primeberrry")
model = project.version("3").model

