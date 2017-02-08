from django.contrib import admin

# Register your models here.

from .models import Case,Consenus,Fact,StatementOfFacts,Verdict,View

admin.site.register(Case)
admin.site.register(Consenus)
admin.site.register(Fact)
admin.site.register(StatementOfFacts)
admin.site.register(Verdict)
admin.site.register(View)
