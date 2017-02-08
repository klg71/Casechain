from django.shortcuts import render
from models import Case
import hashlib

# Create your views here.

class CaseViews:

    def viewCase(self,request):
        """
        View Specific case
        """
        pass

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

