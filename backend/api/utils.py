from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status
from rest_framework.response import Response

User = get_user_model()

def download_shooping_card(x):
    """Функция для скачивания shopping_card."""
    pdfmetrics.registerFont(
        TTFont("Fonts", "Fonts.ttf", "UTF-8"))
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = ("attachment; "
                                       "filename='shopping_list.pdf'")
    page = canvas.Canvas(response)
    page.setFont("Fonts", size=24)
    page.drawString(200, 800, "Список ингредиентов")
    page.setFont("Fonts", size=16)
    height = 750
    for i, (name, data) in enumerate(x.items(), 1):
        page.drawString(75, height, (f"<{i}> {name} - {data['amount']}, "
                                     f"{data['measurement_unit']}"))
        height -= 25
    page.showPage()
    page.save()
    return response

def check_author_and_user(request):
    """Вынес проверку на автора для функций подписок."""
    author = get_object_or_404(User, id=id)

    if request.user == author:
        return status==status.HTTP_400_BAD_REQUEST
    
    return status
