# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import bcrypt
from django.db import models

# Create your models here.
class UserManager(models.Manager):
    def registervalidate(self, postdata):
        results = {'status':True, 'errors':[], 'user':None}
        if not postdata['first_name'] or len(postdata['first_name']) < 3:
            results['errors'].append("First name must be at least 3 characters")
            results['status'] = False
        if not postdata['last_name'] or len(postdata['last_name']) < 3:
            results['errors'].append("Last name must be at least 3 characters")
            results['status'] = False
        if not postdata['email'] or \
            not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", postdata['email']):
            results['errors'].append("Email must be a valid email address")
            results['status'] = False
        if not postdata['userpassword'] or len(postdata['userpassword']) < 8:
            results['errors'].append("Password must be at least 8 characters")
            results['status'] = False
        if postdata['cpassword'] != postdata['cpassword']:
            results['errors'].append("Passwords do not match")
            results['status'] = False
        user = User.objects.filter(email=postdata['email'])
        if user:
            results['status'] = False
            results['errors'].append("User already exists. Please login...")
        if results['status']:
            userpassword = bcrypt.hashpw(postdata['userpassword'].encode(), bcrypt.gensalt())
            user = User.objects.create(
                first_name=postdata['first_name'],
                last_name=postdata['last_name'],
                email=postdata['email'],
                userpassword=userpassword)
            results['user'] = user
        return results

    def loginvalidate(self, postdata):
        results = {'status':True, 'errors':[], 'user':None}
        user = User.objects.filter(email=postdata['email'])
        try:                #need this try loop if the db is empty.
            user[0]
        except IndexError:
            results['status'] = False
            return results
        if user[0]:
            if user[0].userpassword != bcrypt.hashpw(postdata['userpassword'].encode(),
                                                     user[0].userpassword.encode()):
                results['status'] = False
            else:
                results['user'] = user[0].id
        else:
            results['status'] = False
        return results

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    userpassword = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.email + "," + self.userpassword
    objects = UserManager()
    #ReviewUsers
