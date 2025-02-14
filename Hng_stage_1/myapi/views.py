

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import logging
import requests

logger = logging.getLogger(__name__)

def is_prime(number):
    """Check if a number is prime."""
    if number <= 1:
        return False
    if number == 2:
        return True
    if number % 2 == 0:
        return False
    for d in range(3, int(abs(number) ** 0.5) + 1, 2):
        if number % d == 0:
            return False
    return True

def is_perfect(number):
    """Check if a number is perfect."""
    return sum(i for i in range(1, abs(number)) if number % i == 0) == abs(number)

def is_armstrong(number):
    """Check if a number is an Armstrong number."""
    digits = str(abs(number))
    power = len(digits)
    return sum(int(digit) ** power for digit in digits) == abs(number)

def get_fun_fact(number):
    """Fetch a fun fact about the number from the Numbers API."""
    url = f"http://numbersapi.com/{abs(number)}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            fact = response.text.strip()
            if number < 0:
                fact = f"-{number} is an unremarkable number."
            return fact
        return f"No fun fact available for {number}"
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching fun fact: {e}")
        return "Fun fact service is unavailable."

def number_properties(n):
    """Determine number properties (armstrong, even, odd)."""
    properties = []
    if is_armstrong(n):
        properties.append("armstrong")
    if n % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")
    return properties

@api_view(["GET"])
def classify_number(request):
    """API endpoint to classify a number."""
    number_param = request.GET.get("number", "").strip()
    
    try:
        number = int(number_param)
    except ValueError:
        return Response({"number": "alphabet", "error": True}, status=status.HTTP_400_BAD_REQUEST)

    properties = number_properties(number)
    response_data = {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": sum(int(d) for d in str(abs(number))),
        "fun_fact": get_fun_fact(number),
    }
    return Response(response_data, status=status.HTTP_200_OK)