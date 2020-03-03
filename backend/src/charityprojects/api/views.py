import json

from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from ..models import CharityProjects, ProjectUser, ProjectUserDetails, Prize
from django.http import JsonResponse
from accounts.models import User
from .serializers import ProjectUserSerializer
from rest_framework import status
from rest_framework.response import Response


def charity_project_details(request, project_id):
    response = {'status': "Invalid Request"}
    project = CharityProjects.objects.get(pk=project_id)
    print(request.build_absolute_uri(project.Video.url))
    if request.method == "GET":
        try:
            if project:
                response['status'] = "Success"
                response["project_name"] = project.Name
                response["project_goal"] = project.Goal
                response["project_mission"] = project.Mission
                if project.Video_Name:
                    response["project_video_name"] = project.Video_Name
                    response["project_video"] = request.build_absolute_uri(project.Video.url)
                else:
                    response["project_video_name"] = ""
                    response["project_video"] = ""

                response["project_category"] = project.Category
                response["project_tags"] = project.Tags
                response["project_badge"] = request.build_absolute_uri(project.Badge.url)
                response["project_banner"] = ""
                if project.Banner:
                    response["project_banner"] = request.build_absolute_uri(project.Banner.url)
            else:
                response['status'] = "Wrong project id"
        except ValueError:
            response['status'] = "Invalid Request"
    return JsonResponse(response)


def all_project_list(request):
    response = {'status': "Success"}
    project_list = []
    projects = CharityProjects.objects.all()
    for project in projects:
        project_list.append(project.Name)
        response['project_list'] = project_list
    return JsonResponse(response)


def all_project_info_list(request):
    response = {'status': "Success"}
    projects = CharityProjects.objects.all()
    project_list = []
    for project in projects:
        each_project = {"project_id": project.id, "project_name": project.Name, "project_goal": project.Goal,
                        "project_mission": project.Mission,
                        "project_video": request.build_absolute_uri(project.Video_Name),
                        "project_category": project.Category,
                        "project_badge": request.build_absolute_uri(project.Badge.url),
                        "project_tags": project.Tags, "project_banner": request.build_absolute_uri(project.Banner.url)}
        project_list.append(each_project)
    print(project_list)
    response['project_list'] = project_list
    return JsonResponse(response)


def project_category(request):
    response = {'status': "Success"}
    category_list = []
    projects = CharityProjects.objects.all()
    for project in projects:
        category_list.append(project.Category)
        response['category_list'] = category_list
    return JsonResponse(response)


def start_project(request):
    response = {'status': "Invalid Request"}
    invited_by = ""
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body)
            project_id = json_data["project_id"]
            user = User.objects.get(email=json_data["user_emailid"])
            if 'invited_by' not in json_data:
                invited_by = ""
            project = CharityProjects.objects.get(pk=project_id)
            user_id = User.objects.get(email=json_data["user_emailid"]).id
            project_user_records = ProjectUser.objects.filter(project_id_id=project_id, user_id_id=user_id)
            if project_user_records.count() > 0:
                for record in project_user_records:
                    purecord_id = record.id
                    print(record.project_status)
                    response['status'] = "Entry already exists."
                    response['project_status'] = record.project_status
                    project_user_details_records = ProjectUserDetails.objects.filter(pu_id=purecord_id)
                    for precord in project_user_details_records:
                        if precord.video == "":
                            response['status'] = "No video uploaded. Complete step2 "
                        elif precord.prize_given_id is None:
                            response['status'] = "Select prize for project. Complete step3"
            else:
                project_user = ProjectUser.objects.create(project_id=project, user_id=user,
                                                                  invited_by=invited_by, project_status="PlanningPhase1")
                project_user.save()
                print("Created new record")
                pu_id = project_user.id
                project_user_details = ProjectUserDetails.objects.create(pu_id=project_user)
                project_user_details.save()
                response["pu_id"] = pu_id
                response['status'] = "Success"
        except ValueError:
            response['status'] = "Invalid Request"
    print(response)
    return JsonResponse(response)


@api_view(['PUT'])
@parser_classes([MultiPartParser, FormParser])
def update_project_invitation_video_details(request):
    if request.method == 'PUT':
        user_emailid = request.data["Email"]
        project_id = request.data["ProjectId"]

        user_id = User.objects.get(email=user_emailid).id #get user id from email id
        project_user_record = ProjectUser.objects.filter(user_id_id=user_id, project_id_id=project_id)[0]# from project user table get id
        pu_id = project_user_record.id
        project_user_details = ProjectUserDetails.objects.filter(pu_id=pu_id)[0]
        project_user_update_data = {"video": request.data["ProjectVideo"]}
        # Create new dictionary containing data to update

        if project_user_details:
            project_user_serializer = ProjectUserSerializer(project_user_details, data=project_user_update_data)
            if project_user_serializer.is_valid():
                project_user_serializer.save()
                project_user_record.project_status = "PlanningPhase2"
                project_user_record.save()
                return Response(project_user_serializer.data, status=status.HTTP_201_CREATED)
            else:
                print('error', project_user_serializer.errors)
                return Response(project_user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# @api_view(['PUT'])
# @parser_classes([MultiPartParser, FormParser])
def update_project_prize(request):
    response = {'status': "Invalid Request"}
    if request.method == 'PUT':
        json_data = json.loads(request.body)
        user_email_id = json_data["user_email"]
        user_id = User.objects.get(email=user_email_id).id  # get user id from email id
        project_id = json_data["project_id"]
        prize_id = json_data["prize_id"]
        project_user_record = ProjectUser.objects.filter(user_id=user_id,
                                        project_id_id=project_id)[0]
        pu_id = project_user_record.id
        project_user_details = ProjectUserDetails.objects.filter(pu_id=pu_id)[0]

        if project_user_details:
            project_user_details.prize_given_id = Prize.objects.get(pk=prize_id)
            project_user_details.save()
            project_user_record.project_status = "PlanningPhase3"
            project_user_record.save()
            response['status'] = "Success"
        else:
            response['status'] = 'Wrong project user reference'
    return JsonResponse(response)


def update_project_challenge_status_explore(request):
    response = {'status': "Invalid Request"}
    if request.method == 'PUT':
        json_data = json.loads(request.body)
        user_email_id = json_data["user_email"]
        user_id = User.objects.get(email=user_email_id).id
        project_id = json_data["project_id"]
        project_join_date = json_data["joining_date"]
        project_user_record = ProjectUser.objects.filter(user_id=user_id, project_id_id=project_id)[0] #ideally only one entry should be there
        if project_user_record:
            project_user_record.date_joined = project_join_date
            project_user_record.challenge_status = "Challenge1Complete"
            project_user_record.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


