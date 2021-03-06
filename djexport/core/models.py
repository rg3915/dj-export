from django.db import models
from django.utils.timezone import now
from django.shortcuts import resolve_url as r
from localflavor.br.br_states import STATE_CHOICES

PHONE_TYPE = (
    ('pri', 'principal'),
    ('com', 'comercial'),
    ('res', 'residencial'),
    ('cel', 'celular'),
    ('cl', 'Claro'),
    ('oi', 'Oi'),
    ('t', 'Tim'),
    ('v', 'Vivo'),
    ('n', 'Nextel'),
    ('fax', 'fax'),
    ('o', 'outros'),
)


class TimeStampedModel(models.Model):
    created = models.DateTimeField(
        'criado em', auto_now_add=True, auto_now=False)
    modified = models.DateTimeField(
        'modificado em', auto_now_add=False, auto_now=True)

    class Meta:
        abstract = True


class Address(models.Model):
    address = models.CharField(u'endereço', max_length=100, blank=True)
    complement = models.CharField('complemento', max_length=100, blank=True)
    district = models.CharField('bairro', max_length=100, blank=True)
    city = models.CharField('cidade', max_length=100, blank=True)
    uf = models.CharField('UF', max_length=2,
                          choices=STATE_CHOICES, blank=True)
    cep = models.CharField('CEP', max_length=9, blank=True)

    class Meta:
        abstract = True


class Person(TimeStampedModel, Address):
    first_name = models.CharField('nome', max_length=50)
    last_name = models.CharField(
        'sobrenome', max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    birthday = models.DateField('nascimento', null=True)
    blocked = models.BooleanField('bloqueado', default=False)

    class Meta:
        ordering = ['first_name']
        verbose_name = 'contato'
        verbose_name_plural = 'contatos'

    def __str__(self):
        return ' '.join(filter(None, [self.first_name, self.last_name]))

    full_name = property(__str__)

    def get_absolute_url(self):
        return r('core:person_detail', pk=self.pk)

    def get_age(self):
        # Retorna a idade da pessoa
        today = now().date()
        bdate = self.birthday

        if not bdate:
            return 0

        age = today.year - bdate.year

        # Verifica se o dia e o mês de aniversário já passaram;
        # se não, tira 1 de `age`.
        if today.month < bdate.month \
           or (today.month == bdate.month and today.day < bdate.day):
            age -= 1

        return age


class Phone(models.Model):
    phone = models.CharField('telefone', max_length=20, blank=True)
    person = models.ForeignKey('Person')
    phone_type = models.CharField(
        'tipo', max_length=3, choices=PHONE_TYPE, default='pri')

    def __str__(self):
        return self.phone
