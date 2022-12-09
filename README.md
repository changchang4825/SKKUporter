# SKKUporter
## Requirements
```
Django==4.1.3
pycparser==2.21
pyperclip==1.8.2
requests==2.28.1
selenium==4.6.0
```
## REST API
### 1. /authentification
- method: POST
- body: {"id": my_id, "pw": my_pw"}
- lecture api 이용에 필요한 token을 발급


### 2. /lecture
- method: ANY (상관없음)
- 마감 기한이 지나지 않은 강의와 과제 목록을 JSON 형태로 반환
#### Example
```
{
    "Lectures": [
        {
            "id": 32429,
            "name": "HCI개론",
            "classNum": "SWE3053_41",
            "prof": "조재민",
            "thingsToDo": {
                "lecture": [],
                "assignment": []
            }
        },
        {
            "id": 32225,
            "name": "Introduction to Software Engineering",
            "classNum": "SWE3002_42",
            "prof": "차수영",
            "thingsToDo": {
                "lecture": [
                    {
                        "title": "SWE3002_Lecture10_Automatic Program Repair (1)",
                        "dueDate": "2022-11-20T14:59:59Z"
                    },
                    {
                        "title": "SWE3002_Lecture10_Automatic Program Repair (2)",
                        "dueDate": "2022-11-20T14:59:59Z"
                    }
                ],
                "assignment": []
            }
        }
    ]
}
```
