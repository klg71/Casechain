from django.contrib import admin

# Register your models here.

from .models import Case,Consenus,Facts,StatementOfFacts,Verdict,Views

admin.site.register(Case)
admin.site.register(Consenus)
admin.site.register(Facts)
admin.site.register(StatementOfFacts)
admin.site.register(Verdict)
admin.site.register(Views)
