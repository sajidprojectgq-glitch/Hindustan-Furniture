from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import FurnitureForm
from .models import CategorizePost


# ---------------------------
# PUBLIC VIEWS
# ---------------------------

def home(request):
    """Home page: show latest products."""
    products = CategorizePost.objects.all().order_by('-date')
    return render(request, "index.html", {"products": products})


# def products(request):
#     """Products page with optional category filter."""
#     category = request.GET.get("category")
#     if category:
#         products_list = CategorizePost.objects.filter(type=category)
#     else:
#         products_list = CategorizePost.objects.all()

#     context = {
#         "products": products_list,
#         "selected_category": category,
#     }
#     return render(request, "product.html", context)

# views.py (suggested implementation; adjust as needed if you have an existing view)
from django.shortcuts import render
from django.db.models import F, ExpressionWrapper, FloatField
from .models import CategorizePost

def products(request):
    category = request.GET.get('category')
    sort_by = request.GET.get('sort_by')
    show_discounted = request.GET.get('discounted') == 'on'  # Checkbox value

    products = CategorizePost.objects.all()

    if category:
        products = products.filter(type=category)

    if show_discounted:
        products = products.filter(discount_price__isnull=False)

    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'new':
        products = products.order_by('-date')
    elif sort_by == 'discount':
        # Sort by discount percentage descending (higher discount first)
        products = products.filter(discount_price__isnull=False).annotate(
            discount_perc=ExpressionWrapper(
                (F('price') - F('discount_price')) / F('price') * 100,
                output_field=FloatField()
            )
        ).order_by('-discount_perc')
    # Else: default ordering (e.g., by ID or relevance if search is added later)

    # Get display name for selected category
    selected_category = next((display for value, display in CategorizePost.FURNITURE_TYPES if value == category), category.title() if category else None)

    context = {
        'products': products,
        'selected_category': selected_category,
        'category': category,  # For hidden input in form
        'sort_by': sort_by,
        'show_discounted': show_discounted,
    }
    return render(request, 'product.html', context)  # Replace with your template name

def about(request):
    """About page."""
    return render(request, "about.html")


def contact(request):
    """Contact page."""
    return render(request, "about.html")


# ---------------------------
# ADMIN AUTHENTICATION
# ---------------------------

def admin_login(request):
    """Admin login view."""
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('admin_log')  # Already logged in admin

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin_log')
        else:
            messages.error(request, "Invalid credentials or not an admin.")

    return render(request, "admin_login.html")


@login_required
def admin_logout(request):
    """Logout admin and redirect to login page."""
    logout(request)
    return redirect('admin_login')


# ---------------------------
# ADMIN DASHBOARD & CRUD
# ---------------------------

@user_passes_test(lambda u: u.is_superuser)
def admin_log(request):
    """Admin dashboard: list all furniture posts."""
    products = CategorizePost.objects.all().order_by('-date')
    return render(request, "admin_log.html", {"products": products})


@user_passes_test(lambda u: u.is_superuser)
@login_required
def upload_furniture(request):
    """Upload/Add new furniture — superuser only."""
    if request.method == "POST":
        form = FurnitureForm(request.POST, request.FILES)
        if form.is_valid():
            furniture = form.save(commit=False)
            furniture.owner = request.user  # assign owner
            furniture.save()
            return redirect("admin_log")
    else:
        form = FurnitureForm()

    return render(request, "upload.html", {"form": form})


@user_passes_test(lambda u: u.is_superuser)
@login_required
def edit_furniture(request, pk):
    """Edit furniture — superuser only."""
    furniture = get_object_or_404(CategorizePost, pk=pk)

    if request.method == "POST":
        form = FurnitureForm(request.POST, request.FILES, instance=furniture)
        if form.is_valid():
            form.save()
            return redirect('admin_log')
    else:
        form = FurnitureForm(instance=furniture)

    return render(request, "upload.html", {"form": form, "edit": True})


@user_passes_test(lambda u: u.is_superuser)
@login_required
def delete_furniture(request, pk):
    """Delete furniture — superuser only."""
    furniture = get_object_or_404(CategorizePost, pk=pk)

    if request.method == "POST":
        furniture.delete()
        return redirect('admin_log')

    return render(request, "confirm_delete.html", {"furniture": furniture})


# details


def details(request, pk):
    products = CategorizePost.objects.all()
    product = get_object_or_404(products, pk=pk)
    return render(request, 'details.html', {'product': product})