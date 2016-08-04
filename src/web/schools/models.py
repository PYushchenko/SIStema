from django.core import urlresolvers
from django.db import models
import django.utils.dateformat


class School(models.Model):
    name = models.CharField(max_length=50, help_text='Например, «ЛКШ 2048»')

    year = models.CharField(max_length=50,
                            blank=True,
                            help_text='Год (календарный или учебный) проведения школы.'
                                      'Для ЛКШ.Зима может отличаться от short_name. Может быть неуникальным')

    full_name = models.TextField(help_text='Полное название, не аббревиатура.'
                                           'По умолчанию совпадает с обычным названием.'
                                           'Например, «Летняя компьютерная школа 2048»')

    short_name = models.CharField(max_length=20,
                                  help_text='Используется в урлах. Например, 2048',
                                  unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.full_name:
            self.full_name = self.name
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return urlresolvers.reverse('school:index', kwargs={'school_name': self.short_name})


class Session(models.Model):
    school = models.ForeignKey(School)

    name = models.CharField(max_length=50, help_text='Например, Август')

    short_name = models.CharField(max_length=20, help_text='Используется в урлах. Лучше обойтись латинскими буквами, цифрами и подчёркиванием. Например, august')

    start_date = models.DateField(help_text='Первый день смены')

    finish_date = models.DateField(help_text='Последний день смены')

    class Meta:
        unique_together = ('school', 'short_name')

    def __str__(self):
        return '%s.%s' % (self.school.name, self.name)

    @property
    def dates_range(self):
        date_format = django.utils.dateformat.format

        # С 27 декабря 2015 года по 7 января 2016 года
        if self.start_date.year != self.finish_date.year:
            return 'С %s по %s' % (date_format(self.start_date, 'd E Y года'),
                                   date_format(self.finish_date, 'd E Y года'))

        # С 28 июля по 20 августа 2016 года
        if self.start_date.month != self.finish_date.month:
            return 'С %s по %s' % (date_format(self.start_date, 'd E'),
                                   date_format(self.finish_date, 'd E Y года'))

        # С 5 по 20 июля 2016 года
        return 'С %s по %s' % (date_format(self.start_date, 'd'),
                               date_format(self.finish_date, 'd E Y года'))


class Parallel(models.Model):
    school = models.ForeignKey(School, related_name='parallels')

    short_name = models.CharField(max_length=100, help_text='Используется в урлах. Лучше обойтись латинскими буквами, цифрами и подчёркиванием. Например, c_prime')

    name = models.CharField(max_length=100, help_text='Например, C\'')

    sessions = models.ManyToManyField(Session)

    class Meta:
        unique_together = ('school', 'short_name')

    def __str__(self):
        return '%s.%s' % (self.school.name, self.name)