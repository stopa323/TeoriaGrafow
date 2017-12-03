from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Sala(models.Model):
    kod_sali = models.CharField(max_length=30)
    budynek = models.CharField(max_length=30)
    ilosc_miejsc = models.IntegerField()
    rzutnik_tag = models.BooleanField()
    komputer_tag = models.BooleanField()
    tablica_tag = models.BooleanField()


class Kurs(models.Model):
    kod_kursu = models.CharField(max_length=30)
    rok = models.CharField(max_length=30)


class Zajecia(models.Model):
    Kurs = models.ForeignKey(Kurs)
    odpowiedzialny_nauczyciel = models.ForeignKey(User, limit_choices_to={'groups__name': "Prowadzacy Zajecia"})
    nazwa_zajec = models.CharField(max_length=30)
    liczba_minut_w_tygodniu = models.IntegerField()
    mozliwe_sale = models.CharField(max_length=200)


class Matrix(models.Model):
    ...


class Prefernecje_Prowadzacego(models.Model):
    prowadzacy = models.ForeignKey(User, limit_choices_to={'groups__name': "Prowadzacy Zajecia"})
    macierz_preferencji = models.ForeignKey(Matrix)
    maksymalna_ilosc_zajec_pod_rzad = models.IntegerField()
    maksymalna_ilosc_cwiczen_pod_rzad = models.IntegerField()
    minut_przerw_miedzy_zajeciami = models.IntegerField()
    przerwa_obiadowa_tag = models.BooleanField()
    wolny_dzien_tag = models.BooleanField()


class Prefernecje_Studenta(models.Model):
    student = models.ForeignKey(User, limit_choices_to={'groups__name': "Studenci"})
    kurs = models.ForeignKey(Kurs)
    macierz_preferencji = models.ForeignKey(Matrix)


class Cell(models.Model):
    matrix = models.ForeignKey(Matrix)
    row = models.IntegerField()
    col = models.IntegerField()
    val = models.IntegerField()
