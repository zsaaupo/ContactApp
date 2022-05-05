from django.shortcuts import render
from registration.models import AppUser
from .serializers import PersonSerializer, PersonDetailsSerializer, AppUserSerializers
from .models import Person, DeletedContacts
from .serializers import PersonSerializer, PersonDetailsSerializer
import json
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from django.db.models import Q

def contactList(request):
    return render(request, 'index.html')

def details(request, slug):
    return render(request, 'contact_details.html')

def addcontact(request):
    return render(request,'add_contact.html')

def my_account(request):
    return render(request,'my_account.html')

def qr_code(requset, slug):
    return render(requset, 'qr_code.html')

def trashcontact(request):
    return render(request, 'trash_contacts.html')


#All api


class contact_list_api(ListAPIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        data = Person.objects.filter(user=request.user, is_archived=False).all()
        data = PersonSerializer(data, many=True).data
        return Response(data)

class DetailsApi(ListAPIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, slug):
        data_val = Person.objects.filter(slug=slug).first()
        data_val = PersonDetailsSerializer(data_val).data
        return Response(data_val)

class contact_edit_api(CreateAPIView):
    permission_classes = []
    def put(self, request, slug):
        try:
            data = json.loads(request.body)

            person = Person.objects.filter(slug=slug).first()

            if not person:
                feedback = {}
                feedback['status'] = HTTP_400_BAD_REQUEST
                feedback['message'] = "Person was not found !"
                return Response(feedback)
            else:
                person.email = data['email']
                person.name = data['name']
                person.phone = data['phone']
                person.save()

                feedback = {}
                feedback['status'] = HTTP_200_OK
                feedback['message'] = "All details updated !"
                return Response(feedback)
        except Exception as ex:
            feedback = {}
            feedback['status'] = HTTP_400_BAD_REQUEST
            feedback['message'] = str(ex)
            return Response(feedback)


class Add_contact_api(CreateAPIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        try:
            #data= request.data
            data= json.loads(request.body)
            user= request.user
            print("user")
            print(user)
            person = Person()
            if 'name' not  in data or data['name']=='':
                return Response('Please Enter Your Name',status=400)
            if 'phone' not  in data or data['phone']=='':
                return Response('Please Enter Phone Number',status=400)

            person.user= user
            person.name=data['name']
            person.phone=data['phone']
            person.email=data['email']
            person.save()
            result = {}
            result['status'] = HTTP_200_OK
            result['message'] = "success"
            return Response(result)

        except Exception as ex:
            result = {}
            result['status'] = HTTP_400_BAD_REQUEST
            result['message'] = str(ex)
            return Response(result)


class My_account_api(ListAPIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            data_val = AppUser.objects.filter(user=request.user).first()
            data_val = AppUserSerializers(data_val).data
            return Response(data_val)
        except Exception as ex:
            result = {}
            result['status'] = HTTP_400_BAD_REQUEST
            result['message'] = str(ex)
            return Response(result)


class Delete_contact_api(CreateAPIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, slug):
        try:
            #data = json.loads(request.body)
            person = Person.objects.filter(slug=slug, user=request.user).first()

            if not person:
                result = {}
                result['status'] = HTTP_400_BAD_REQUEST
                result['message'] = "Person Not Found !"
                return Response(result)
            else:
                #data['is_archived'] = True
                person.is_archived = True
                person.save()

                result = {}
                result['status'] = HTTP_200_OK
                result['message'] = "Delete Success"
                return Response(result)
        except Exception as ex:
            result = {}
            result['status'] = HTTP_400_BAD_REQUEST
            result['message'] = str(ex)
            return Response(result)


class My_account_edit_api(CreateAPIView):
    permission_classes = [IsAuthenticated]
    def put(self, request):
        try:
            data = json.loads(request.body)

            if 'name' not  in data or data['name']=='':
                feedback = {}
                feedback['status'] = HTTP_400_BAD_REQUEST
                feedback['message'] = "Name can't be Null !"
                return Response(feedback)
            if 'email' not  in data or data['email']=='':
                feedback = {}
                feedback['status'] = HTTP_400_BAD_REQUEST
                feedback['message'] = "email not found !"
                return Response(feedback)

            user = User.objects.filter(email=data['email']).first()

            if not user:
                feedback = {}
                feedback['status'] = HTTP_400_BAD_REQUEST
                feedback['message'] = "Invalid User !"
                return Response(feedback)

            app_user = AppUser.objects.filter(user=request.user).first()

            if not app_user:
                feedback = {}
                feedback['status'] = HTTP_400_BAD_REQUEST
                feedback['message'] = "Person was not found !"
                return Response(feedback)
            else:
                app_user.full_name = data['name']
                user.first_name = data['name']
                user.save()
                app_user.save()

                feedback = {}
                feedback['status'] = HTTP_200_OK
                feedback['message'] = "All details updated !"
                return Response(feedback)
        except Exception as ex:
            feedback = {}
            feedback['status'] = HTTP_400_BAD_REQUEST
            feedback['message'] = str(ex)
            return Response(feedback)

class Trash_contact_list_api(ListAPIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        data = Person.objects.filter(user=request.user, is_archived=True).all()
        data = PersonSerializer(data, many=True).data
        return Response(data)

class Trash_contact_api(ListAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, slug):
        try:
            data_archived = Person.objects.filter(user=request.user, slug=slug).first()
            if data_archived.is_archived:
                deleted_contacts = DeletedContacts()
                deleted_contacts.user = data_archived.user
                deleted_contacts.name = data_archived.name
                deleted_contacts.email = data_archived.email
                deleted_contacts.phone = data_archived.phone
                deleted_contacts.slug = data_archived.slug
                deleted_contacts.is_archived = True
                deleted_contacts.save()
                data_trashed = data_archived.delete()
                feedback = {}
                feedback['status'] = HTTP_200_OK
                feedback['message'] = "Trashed"
                return Response(feedback)
        except Exception as e:
            feedback = {}
            feedback['status'] = HTTP_400_BAD_REQUEST
            feedback['message'] = str(e)
            return Response(feedback)

class Trash_restore(ListAPIView):
    permission_classes = []

    def put(self, request, slug):
        try:
            person = Person.objects.filter(user=request.user, slug=slug, is_archived=True).first()
            if not person.is_archived:
                feedback = {}
                feedback['status'] = HTTP_200_OK
                feedback['message'] = "ALready is list"
                return Response(feedback)
            else:
                person.is_archived = False
                person.save()
                feedback = {}
                feedback['status'] = HTTP_200_OK
                feedback['message'] = "Restored"
                return Response(feedback)

        except Exception as e:
            feedback = {}
            feedback['status'] = HTTP_400_BAD_REQUEST
            feedback['message'] = str(e)
            return Response(feedback)

class Search_contact_api(ListAPIView):
    permission_classes = [IsAuthenticated]
    def put(self, request):
        try:
            data = json.loads(request.body)
            if 'search_keywords' not in data or data['search_keywords'] == '':
                feedback = {}
                feedback['status'] = HTTP_400_BAD_REQUEST
                feedback['message'] = "Search Keyword Not Found !"
                return Response(feedback)

            search_result = Person.objects.filter(user=request.user,is_archived=False).all()
            search_result = search_result.filter(Q(name__icontains=data['search_keywords']) | Q(phone__icontains=data['search_keywords']) | Q(email__icontains=data['search_keywords'])).all()
            search_result = PersonSerializer(search_result, many=True).data
            return Response(search_result)
        except Exception as ex:
            result = {}
            result['status'] = HTTP_400_BAD_REQUEST
            result['message'] = str(ex)
            return Response(result)
