from django.db import models
from datetime import *


class Recipe(models.Model):
    name = models.CharField(max_length=255)
    ingredients = models.TextField()
    description = models.TextField()
    created = models.DateField(auto_now_add=timezone)
    updated = models.DateField(auto_now=timezone)
    preparation = models.IntegerField(null=False)
    votes = models.IntegerField(default=0)
    method_of_preparation = models.TextField()

    def __str__(self):
        return self.name


class Plan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateField(auto_now_add=timezone)
    recipes = models.ManyToManyField(Recipe, through="RecipePlan")

    def __str__(self):
        return self.name


class Dayname(models.Model):
    name = models.CharField(max_length=16)
    order = models.IntegerField(unique=True)

    def __str__(self):
        return self.name


class RecipePlan(models.Model):
    meal_name = models.CharField(max_length=255)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    order = models.IntegerField()
    dayname = models.ForeignKey(Dayname, on_delete=models.CASCADE)

    def __str__(self):
        return self.meal_name


class Page(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(max_length=255)

    def __str__(self):
        return self.title + " " + self.description + " " + self.slug
