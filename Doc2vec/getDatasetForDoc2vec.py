from androguard.misc import AnalyzeAPK
import os
from androguard.core.analysis.analysis import ExternalMethod

def getDataUserAndAPI(FCG):
    for node in FCG.nodes:
        if isinstance(node, ExternalMethod):
            name = str(node.class_name)[1:-1]
            with open("api.txt", "a") as file:
                file.write(name + "\n")
        else:
            opcode_groups = set()
            for instr in node.get_instructions():
                opcode_groups.add(instr.get_name())
            with open("user.txt", "a") as file:
                file.write(str(list(opcode_groups)) + "\n")

begin_cnt, malware_cnt = 0, 0
for root, dirs, files in os.walk("Dataset/Malware"):
    for file in files:
        if file.endswith(".apk"):
            begin_cnt += 1
            if begin_cnt == 100: break
            file_path = os.path.join(root, file)
            a, d, dx = AnalyzeAPK(file_path)
            FCG = dx.get_call_graph()
            getDataUserAndAPI(FCG)

for root, dirs, files in os.walk("Dataset/Begin"):
    for file in files:
        if file.endswith(".apk"):
            malware_cnt += 1
            if malware_cnt == 10: break
            file_path = os.path.join(root, file)
            a, d, dx = AnalyzeAPK(file_path)
            FCG = dx.get_call_graph()
            getDataUserAndAPI(FCG)