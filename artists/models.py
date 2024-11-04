from django.db import models

# Create your models here.
class Expenses(models.Model):
    salary = models.IntegerField("Зарплата");
    artist = models.ForeignKey("Artist",on_delete=models.CASCADE, null=True)
    income = models.ForeignKey("Income",on_delete=models.CASCADE, null=True)
    user = models.ForeignKey("auth.User", verbose_name="Пользователь", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Расход"
        verbose_name_plural = "Расходы"


class Income(models.Model):
    date = models.DateField("Дата")
    place = models.TextField("Место")
    show = models.ForeignKey("Show",on_delete=models.CASCADE, null=True)
    user = models.ForeignKey("auth.User", verbose_name="Пользователь", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Доход"
        verbose_name_plural = "Доходы"


class Type(models.Model):
    show_type = models.TextField("Тип шоу")
    user = models.ForeignKey("auth.User", verbose_name="Пользователь", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Тип шоу"
        verbose_name_plural = "Типы шоу"

    def __str__(self) -> str:
        return self.show_type   

class Show(models.Model):
    name = models.TextField("Название")
    type = models.ForeignKey("Type", on_delete=models.CASCADE, null=True)
    price = models.IntegerField("Стоимость")
    picture = models.ImageField("Изображение", null=True, upload_to="artists")
    user = models.ForeignKey("auth.User", verbose_name="Пользователь", on_delete=models.CASCADE, null=True)
    
    class Meta:
        verbose_name = "Номер"
        verbose_name_plural = "Номера"

    def __str__(self) -> str:
        return self.name   

class Artist(models.Model):
    name = models.TextField("Имя")
    #show_name = models.TextField("Название номера")
    show = models.ForeignKey("Show", on_delete=models.CASCADE, null=True)
    picture = models.ImageField("Изображение", null=True, upload_to="artists")
    user = models.ForeignKey("auth.User", verbose_name="Пользователь", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Артист"
        verbose_name_plural = "Артисты"

    def __str__(self) -> str:
        return self.name    

