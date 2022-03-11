from datetime import datetime
from django.shortcuts import render, redirect, render_to_response
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
import random
from jedzonko.models import Recipe, Plan, RecipePlan, Dayname, Page
from django.db.models import Count
from django.core.paginator import Paginator
from urllib.error import HTTPError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import LogForms, AddUser, ResetPass
from django.contrib.auth.mixins import PermissionRequiredMixin


class IndexView(View):
    def get(self, request):
        recpies = list(Recipe.objects.all())
        plan = list(Plan.objects.all())
        random.shuffle(recpies)
        random.shuffle(plan)
        ctx = {"actual_date": datetime.now(), "recipe": recpies, "plan": plan}
        return render(request, "index.html", ctx)

    def post(self, request):
        recpies = list(Recipe.objects.all())
        plan = list(Plan.objects.all())
        random.shuffle(recpies)
        random.shuffle(plan)
        try:
            if request.POST.get("name") != "":
                recipename = request.POST.get("name")
                recipe = Recipe.objects.get(name=recipename)
                return redirect(f'/recipe/{recipe.id}')
            elif request.POST.get("weight") != "" and request.POST.get("height") != "":
                wei = int(request.POST.get("weight"))
                hei = float(request.POST.get("height").replace(",", "."))
                bmi = wei / (hei ** 2)
                bmi = round(bmi, 2)
                if bmi < 19:
                    text = f"Twoje BMI to {bmi}, zbyt niski (niedowaga), jeśli otrzymaliśmy wynik poniżej 19"
                elif 19 < bmi < 25:
                    text = f"Twoje BMI to {bmi}, prawidłowy (normalna waga), jeżeli nasz wynik mieści się w przedziale 19 – 24,9"
                elif 25 < bmi < 30:
                    text = f"Twoje BMI to {bmi}, zbyt wysoki (nadwaga), kiedy otrzymaliśmy BMI z przedziału 25 – 29,9"
                ctx = {"actual_date": datetime.now(), "recipe": recpies, "plan": plan, "bmi": text}
                return render(request, "index.html", ctx)
            else:
                ctx = {"actual_date": datetime.now(), "recipe": recpies, "plan": plan}
                return render(request, "index.html", ctx)
        except:
            ctx = {"actual_date": datetime.now(), "recipe": recpies, "plan": plan}
            return render(request, "index.html", ctx)


class Dashboard(View):
    def get(self, request):
        recipes = Recipe.objects.all()
        plans = Plan.objects.all().order_by('-created')
        plan = plans[0]
        recipeplan = RecipePlan.objects.filter(plan_id=plan.id).order_by('order')
        daynames = Dayname.objects.filter(id__in=recipeplan.values('dayname_id')).order_by('order')
        return render(request, "dashboard.html",
                      {'recipes': recipes, 'plans': plans, 'plan': plan, 'recipeplan': recipeplan,
                       'daynames': daynames})


class RecipeID(View):
    def get(self, request, id):
        recipe = Recipe.objects.get(id=id)
        return render(request, "app-recipe-details.html", {"recipe": recipe})

    def post(self, request, id):
        if request.POST.get("vote") == "1":
            vp = Recipe.objects.get(id=id)
            vp.votes = vp.votes + 1
            vp.save()
            return redirect(f'/recipe/{vp.id}/')
        elif request.POST.get("voteminus") == "2":
            vm = Recipe.objects.get(id=id)
            vm.votes = vm.votes - 1
            vm.save()
            return redirect(f'/recipe/{vm.id}/')


class RecipeList(View):
    def get(self, request):
        recipe_list = Recipe.objects.all().order_by('-votes', '-created')
        paginator = Paginator(recipe_list, 5)
        page = request.GET.get('page')
        recipes = paginator.get_page(page)
        return render(request, "app-recipes.html", {'recipes': recipes})

    def post(self, request):
        recipid = request.POST.get("id")
        recip = Recipe.objects.get(id=recipid)
        recip.delete()
        return redirect('/recipe/list/')


class RecipeAdd(PermissionRequiredMixin, View):
    permission_required = 'jedzonko.add_recipe'

    def get(self, request):
        return render(request, "app-add-recipe.html")

    def post(self, request):
        name = request.POST.get('name')
        description = request.POST.get("description")
        preparation = request.POST.get("preparation")
        method_of_preparation = request.POST.get("method_of_preparation")
        ingredients = request.POST.get("ingredients")
        if name != "" and description != "" and preparation != "" and method_of_preparation != "" and ingredients != "":
            Recipe.objects.create(
                name=name,
                description=description,
                preparation=preparation,
                method_of_preparation=method_of_preparation,
                ingredients=ingredients
            )
            return redirect('/recipe/list/')
        else:
            return render(request, 'app-add-recipe.html', {'alert_flag': True})


class RecipeModify(PermissionRequiredMixin, View):
    permission_required = 'jedzonko.change_recipe'

    def get(self, request, id):
        try:
            Recipe.objects.get(id=id)
        except HTTPError:
            HTTPError.msg = 'Nie ma takiego przepisu'
            return HttpResponse(HTTPError.msg)
        recipe = Recipe.objects.get(id=id)
        return render(request, "app-edit-recipe.html", {'recipe': recipe})

    def post(self, request, id):
        recipe = Recipe.objects.get(id=id)
        name = request.POST.get('name')
        description = request.POST.get('description')
        preparation = request.POST.get('preparation')
        method_of_preparation = request.POST.get('method_of_preparation')
        ingredients = request.POST.get('ingredients')
        if name != "" and description != "" and preparation != "" and method_of_preparation != "" and ingredients != "":
            recipe.name = name
            recipe.description = description
            recipe.preparation = preparation
            recipe.method_of_preparation = method_of_preparation
            recipe.ingredients = ingredients
            recipe.save()
            return redirect(f'/recipe/list/')
        else:
            return render(request, "app-edit-recipe.html", {'recipe': recipe, 'alert_flag': True})


class PlanModify(PermissionRequiredMixin, View):
    permission_required = 'jedzonko.add_plan'

    def get(self, request, id):
        try:
            Plan.objects.get(id=id)
        except HTTPError:
            HTTPError.msg = 'Nie ma takiego przepisu'
            return HttpResponse(HTTPError.msg)
        plan = Plan.objects.get(id=id)
        return render(request, "app-edit-plan.html", {'plan': plan})

    def post(self, request, id):
        plan = Plan.objects.get(id=id)
        name = request.POST.get('name')
        description = request.POST.get('description')
        if name != "" and description != "":
            plan.name = name
            plan.description = description
            plan.save()
            return redirect(f'/plan/list/')
        else:
            return render(request, "app-edit-plan.html", {'plan': plan, 'alert_flag': True})


class PlanID(View):
    def get(self, request, id):
        plan = Plan.objects.get(id=id)
        recipeplan = RecipePlan.objects.filter(plan_id=plan.id).order_by('order')
        daynames = Dayname.objects.filter(id__in=recipeplan.values('dayname_id')).order_by('order')
        return render(request, "app-details-schedules.html",
                      {'plan': plan, 'recipeplan': recipeplan, 'daynames': daynames})

    def post(self, request, id):
        recipeplanid = request.POST.get("id")
        recipeplan = RecipePlan.objects.get(id=recipeplanid)
        recipeplan.delete()
        return redirect(f'/plan/{id}')


class PlanAdd(PermissionRequiredMixin, View):
    permission_required = 'jedzonko.add_plan'

    def get(self, request):
        return render(request, "app-add-schedules.html")

    def post(self, request):
        name = request.POST.get("name")
        description = request.POST.get("description")
        if name != "" and description != "":
            plan = Plan.objects.create(name=name, description=description)
            return redirect(f'/plan/{plan.id}')
        else:
            return render(request, 'app-add-schedules.html', {'alert_flag': True})


class PlanAddRecipe(PermissionRequiredMixin, View):
    permission_required = 'jedzonko.add_recipe'

    def get(self, request):
        plan = Plan.objects.all()
        dayname = Dayname.objects.all()
        recipe = Recipe.objects.all()
        return render(request, "app-schedules-meal-recipe.html", {"plan": plan, "dayname": dayname, "recipe": recipe})

    def post(self, request):
        plan1 = Plan.objects.all()
        dayname1 = Dayname.objects.all()
        recipe1 = Recipe.objects.all()
        plan = request.POST.get("nameplan")
        plandb = Plan.objects.get(name=plan)
        plan_id = plandb.id
        namemeals = request.POST.get("namemeal")
        numbermeals = request.POST.get("numbermeal")
        if numbermeals != "" and namemeals != "":
            recipe = request.POST.get("recipe")
            recipedb = Recipe.objects.get(name=recipe)
            recipe_id = recipedb.id
            day = request.POST.get("nameday")
            daydb = Dayname.objects.get(name=day)
            day_id = daydb.id
            RecipePlan.objects.create(
                plan_id=plan_id,
                meal_name=namemeals,
                order=numbermeals,
                recipe_id=recipe_id,
                dayname_id=day_id
            )
            return redirect(f'/plan/{plan_id}/')
        else:
            return render(request, 'app-schedules-meal-recipe.html',
                          {"plan": plan1, "dayname": dayname1, "recipe": recipe1, 'alert_flag': True})


class PlanList(View):
    def get(self, request):
        plan_list = Plan.objects.all().order_by('name')
        paginator = Paginator(plan_list, 5)
        page = request.GET.get('page')
        plans = paginator.get_page(page)
        return render(request, "app-schedules.html", {'plans': plans})

    def post(self, request):
        planid = request.POST.get("id")
        plan = Plan.objects.get(id=planid)
        plan.delete()
        return redirect('/plan/list/')


class ContactView(View):
    def get(self, request):
        if Page.objects.filter(slug="contact").exists():
            slug = Page.objects.get(slug="contact")
            ctx = {"actual_date": datetime.now(), "slug": slug}
            return render(request, "contact.html", ctx)
        else:
            return redirect('/')


class AboutView(View):
    def get(self, request):
        if Page.objects.filter(slug="about").exists():
            slug = Page.objects.get(slug="about")
            ctx = {"actual_date": datetime.now(), "slug": slug}
            return render(request, "about.html", ctx)
        else:
            return redirect('/')


class UserLogin(View):
    def get(self, request):
        form = LogForms()
        return render(request, 'logowaniehome.html', {'form': form})

    def post(self, request):
        form = LogForms(request.POST)
        if form.is_valid():
            user_login = form.cleaned_data['login']
            user_password = form.cleaned_data['password']
            user = authenticate(username=user_login, password=user_password)
            if user is None:
                return render(request, 'logowaniehome.html', {'form': form, 'alert_flag': True})
            else:
                login(request, user)
                return redirect('/')
        else:
            return render(request, 'logowaniehome.html', {'form': form})


class UserLogout(View):
    def get(self, request):
        logout(request)
        return redirect('/')


class FullLoginView(PermissionRequiredMixin, View):
    permission_required = 'jedzonko.view_user'

    def get(self, request):
        form = AddUser()
        return render(request, 'fulllogin.html', {'form': form})

    def post(self, request):
        form = AddUser(request.POST)
        if form.is_valid():
            loginname = form.cleaned_data['login']
            password = form.cleaned_data['password']
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            email = form.cleaned_data['email']
            u = User.objects.create_user(loginname, password=password, first_name=name, last_name=surname, email=email)
            login(request, u)
            return redirect('/')
        else:
            return render(request, 'fulllogin.html', {'form': form, 'alert_flag': True})


class AccountModify(PermissionRequiredMixin, View):
    permission_required = 'jedzonko.change_user'

    def get(self, request, id):
        u = User.objects.get(id=id)
        return render(request, 'modify.html', {'user3': u})


class ChangeDateAccount(PermissionRequiredMixin, View):
    # permission_required = 'jedzonko.change_user'

    def get(self, request, id):
        u = User.objects.get(id=id)
        return render(request, 'changedateuser.html', {'user2': u})

    def post(self, request, id):
        u = User.objects.get(id=id)
        username = request.POST.get("username")
        name = request.POST.get("name")
        surname = request.POST.get("surname")
        email = request.POST.get("email")
        superuser = request.POST.get("super")

        u.username = username
        u.name = name
        u.surname = surname
        u.email = email
        u.is_superuser = superuser
        u.save()
        return redirect(f'/userall/')



class ResetPasswordView(PermissionRequiredMixin, View):
    permission_required = 'jedzonko.change_user'

    def get(self, request, id):
        form = ResetPass()
        return render(request, 'reset_pass.html', {'form': form})

    def post(self, request, id):
        form = ResetPass(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            u = User.objects.get(id=id)
            u.set_password(password)
            u.save()
            return redirect(f'/login/')
        else:
            return render(request, 'reset_pass.html', {'form': form})


class DeleteUser(PermissionRequiredMixin, View):
    permission_required = 'jedzonko.delete_user'

    def get(self, request, id):
        u = User.objects.get(id=id)
        return render(request, "deleteuser.html", {"user": u})

    def post(self, request, id):
        if request.POST.get("id") == "1":
            logout(request)
            u = User.objects.get(id=id)
            u.delete()
            return redirect("/")
        elif request.POST.get("prev") == "2":
            u = User.objects.get(id=id)
            return redirect(f'/modify/{u.id}/')


class UserAllView(PermissionRequiredMixin, View):
    permission_required = 'jedzonko.view_user'

    def get(self, request):
        alluser = User.objects.all()
        return render(request, "userall.html", {"user1": alluser})

