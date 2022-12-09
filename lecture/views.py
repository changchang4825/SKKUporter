from django.http import JsonResponse
from django.utils import timezone
from django.utils.dateparse import parse_datetime
import requests, json
from authentification.models import Token


def lecture(request):
    url = "https://canvas.skku.edu/api/v1/users/self/favorites/courses"
    token = Token.objects.first()
    # header = {'xn_api_token': "Bearer " + xn_api_token}
    header = token.header
    # cookie = {'_normandy_session': _normandy_session}
    cookie = token.cookie
    user_id = token.user_id
    student_id = token.student_id

    course_list = json.loads(requests.get(url=url, cookies=cookie).text.lstrip('while(1);'))
    now = timezone.now()
    lectures = []

    for course in course_list:
        id = str(course.get("id"))
        name = course.get("name")
        classNum = None
        prof = None

        if '_' in name:
            name = name.split('_', 1)
            classNum, prof = name[1].split('(')
            prof = prof[:-1]
            name = name[0]

        url = "https://canvas.skku.edu/learningx/api/v1/courses/" + id + "/allcomponents_db?user_id=" + user_id + "&user_login=" + student_id + "&role=1" #user_num & student_id
        content_list = json.loads(requests.get(url=url, headers=header, cookies=cookie).text.lstrip('while(1);'))
        
        lecture_list = []
        assignment_list = []

        for content in content_list:
            due_at = content.get("due_at")
            if due_at == None or parse_datetime(content.get("due_at")) < now: continue
            title = content.get("title")
            type_ = content.get("type")

            if type_ == "commons":
                lecture_list.append({"title": title, "dueDate": due_at})
            
            elif type_ == "assignment":
                assignment_list.append({"title": title, "dueDate": due_at})

        lectures.append({"id": id, "name": name, "classNum": classNum, "prof": prof, "thingsToDo": {"lecture": lecture_list, "assignment": assignment_list}})

    return JsonResponse({"Lectures": lectures}, safe=False, json_dumps_params={'ensure_ascii': False})