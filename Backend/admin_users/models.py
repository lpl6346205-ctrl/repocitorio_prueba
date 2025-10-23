from django.db import models

# ----------------- Asset Types -----------------
class AssetType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class SpecificAssetType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    type = models.ForeignKey(AssetType, on_delete=models.CASCADE, related_name='specific_types')

    def __str__(self):
        return self.name

# ----------------- Locations -----------------
class Location(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
# ----------------- Roles -----------------
class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
# ----------------- Employee roles -----------------
class Role_employee(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# ----------------- Responsible Persons -----------------
class PersonResponsible(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    role = models.ForeignKey(Role_employee, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role.name})" 

# ----------------- System Users -----------------
class SystemUser(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password_hash = models.TextField()
    role = models.ForeignKey(Role, on_delete=models.PROTECT)
    person = models.ForeignKey(PersonResponsible, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.username

# ----------------- Asset Status -----------------
class AssetStatus(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# ----------------- Assets -----------------
class Asset(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    specific_type = models.ForeignKey(SpecificAssetType, on_delete=models.SET_NULL, null=True)
    status = models.ForeignKey(AssetStatus, on_delete=models.PROTECT)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    person = models.ForeignKey(PersonResponsible, on_delete=models.SET_NULL, null=True, blank=True)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# ----------------- Asset Logs -----------------
class AssetLog(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    change_description = models.TextField()
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    person = models.ForeignKey(PersonResponsible, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.ForeignKey(AssetStatus, on_delete=models.PROTECT)

    def __str__(self):
        return f"Log {self.id} - {self.asset.name}"

# ----------------- Asset Costs -----------------
class AssetCost(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.asset.name} - {self.price}"
