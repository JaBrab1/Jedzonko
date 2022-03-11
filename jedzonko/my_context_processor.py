from django.http import HttpResponse
import datetime
from django.shortcuts import render, redirect


def my_cp(request):
  ctx = {
    "now": datetime.date.today(),
  }
  return ctx
