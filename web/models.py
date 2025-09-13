# from django.db import models
# from django.contrib.auth.models import User

# class CategorizePost(models.Model):
#     FURNITURE_TYPES = [
#         ("bed", "Bed"),
#         ("sofa", "Sofa"),
#         ("chair", "Chair"),
#         ("table", "Table"),
#         ("dresser", "Dresser"),
#         ("wardrobe", "Wardrobe"),
#         ("bookshelf", "Bookshelf"),
#         ("desk", "Desk"),
#         ("cabinet", "Cabinet"),
#         ("nightstand", "Nightstand"),
#         ("dining_set", "Dining Set"),
#         ("coffee_table", "Coffee Table"),
#         ("tv_stand", "TV Stand"),
#         ("ottoman", "Ottoman"),
#         ("recliner", "Recliner"),
#         ("shelving_unit", "Shelving Unit"),
#         ("bench", "Bench"),
#         ("bar_stool", "Bar Stool"),
#         ("mattress", "Mattress"),
#         ("outdoor_furniture", "Outdoor Furniture"),
#     ]

#     title = models.CharField(max_length=50)
#     type = models.CharField(max_length=50, choices=FURNITURE_TYPES)  # dropdown
#     price = models.IntegerField()
#     discount_price = models.IntegerField(null=True, blank=True)
#     stock = models.IntegerField(default=0)
#     brand = models.CharField(max_length=50, blank=True)
#     material = models.CharField(max_length=50, blank=True)
#     color = models.CharField(max_length=30, blank=True)
#     width = models.FloatField(null=True, blank=True)
#     height = models.FloatField(null=True, blank=True)
#     depth = models.FloatField(null=True, blank=True)
#     img = models.ImageField(upload_to="furniture_images/")
#     description = models.TextField(max_length=500)
#     is_featured = models.BooleanField(default=False)

#     # other fields...

#     # <-- CHANGE HERE temporarily -->
#     owner = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name="furniture_posts",
#         null=True,      # allow NULL for existing rows
#         blank=True      # allow empty in forms
#     )

#     date = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.title} ({self.get_type_display()})"


# models.py (unchanged, but included for completeness)
from django.db import models
from django.contrib.auth.models import User

class CategorizePost(models.Model):
    FURNITURE_TYPES = [
        ("bed", "Bed"),
        ("sofa", "Sofa"),
        ("chair", "Chair"),
        ("table", "Table"),
        ("dresser", "Dresser"),
        ("wardrobe", "Wardrobe"),
        ("bookshelf", "Bookshelf"),
        ("desk", "Desk"),
        ("cabinet", "Cabinet"),
        ("nightstand", "Nightstand"),
        ("dining_set", "Dining Set"),
        ("coffee_table", "Coffee Table"),
        ("tv_stand", "TV Stand"),
        ("ottoman", "Ottoman"),
        ("recliner", "Recliner"),
        ("shelving_unit", "Shelving Unit"),
        ("bench", "Bench"),
        ("bar_stool", "Bar Stool"),
        ("mattress", "Mattress"),
        ("outdoor_furniture", "Outdoor Furniture"),
    ]

    title = models.CharField(max_length=50)
    type = models.CharField(max_length=50, choices=FURNITURE_TYPES)  # dropdown
    price = models.IntegerField()
    discount_price = models.IntegerField(null=True, blank=True)
    stock = models.IntegerField(default=0)
    brand = models.CharField(max_length=50, blank=True)
    material = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=30, blank=True)
    width = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    depth = models.FloatField(null=True, blank=True)
    img = models.ImageField(upload_to="furniture_images/")
    description = models.TextField(max_length=500)
    is_featured = models.BooleanField(default=False)

    # other fields...

    # <-- CHANGE HERE temporarily -->
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="furniture_posts",
        null=True,      # allow NULL for existing rows
        blank=True      # allow empty in forms
    )

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.get_type_display()})"

    # Add a property to compute dimensions for display (since template references it but model doesn't have it)
    @property
    def dimensions(self):
        dims = []
        if self.width:
            dims.append(f"{self.width}W")
        if self.height:
            dims.append(f"{self.height}H")
        if self.depth:
            dims.append(f"{self.depth}D")
        return " x ".join(dims) if dims else "N/A"