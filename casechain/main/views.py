from django.shortcuts import render
from . import models
from . import hash
import hashlib
import json
from django.http.response import HttpResponse


# Create your views here.

class CaseViews:

    def viewCase(self,request,case_id=None):
        case = models.Case.objects.get(id=case_id)
        return render(request,'main/index.html',{'case': case})

    def addText(self,request):
        """
        Adds a Text to a case
        """
        pass


    def addCase(self,request):
        """
        Adds a new case to the chain
        """
        pass

    def receiveCase(self,request):
        """
        Method to receive a case from other nodes
        """
        if 'case' in request.POST:
            caseJson=json.loads(request.POST['case'])
            case=models.Case(date=caseJson['date'],
                             court=caseJson['court'],
                             plaintiff=caseJson['plaintiff'],
                             defendant=caseJson['defendant'],
                             hashValue=caseJson['hashValue'],
                             prevHashValue=caseJson['prevHashValue'],
                             nonce=caseJson['nonce']
                             )
            if string(hashLib.calculateHash(case)) != string(caseJson['hashValue']):
                error="sha256 hash incorrect"
                return HttpResponse(json.dumps({'error':error}))


    def __createHashValue(self,caseId):
        """
        Calculates Hash Value for given case
        """
        hashSha265=hashlib.sha256()
        case=Case.objects.get(id=caseId)
        hashSha265.update(bytes(case.nonce,"utf-8"))
        texts=Text.objects.filter(case=case.id)
        for text in texts:
            hashSha265.update(text.text)

