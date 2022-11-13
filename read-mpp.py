import jpype
import mpxj
import json

jpype.startJVM()
# Note: this mpxj package must be imported after jpype.startJVM()
# net.sf.mpxj.reader is running java code
from net.sf.mpxj.reader import UniversalProjectReader

def build_json_data(task):
    childTasks = task.getChildTasks()
    temp_obj = {}
    
    # str is used to convert java string into json serializable string
    temp_obj['taskName'] = str(task.getName().toString())
    temp_obj['duration'] = str(task.getDuration().toString())
    temp_obj['startDate'] = str(task.getStart().toString())
    if len(childTasks) <= 0:
        return temp_obj
    else:
        temp_obj['children'] = [build_json_data(task) for task in childTasks]
        return temp_obj


project = UniversalProjectReader().read('example.mpp')
data = [build_json_data(task) for task in project.getChildTasks()]

json_string = json.dumps(data, indent=2)

with open("./output.json", "w") as outfile:
    outfile.write(json_string)

jpype.shutdownJVM()
