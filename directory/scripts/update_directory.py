# -*- coding: utf-8 -*-
from directory.models import complexTitle, complexLocation, club, address, contact, category
from django.contrib.auth.models import User
from django.utils.timezone import now

def run():
    userInst = User.objects.get(email='admin@sportup.ir')
    catInst = category.objects.create(
            title = u"تنیس",
            slug = u"تنیس",
            status = 2,
            publish_date = now(),
            created = now(),
            updated = now(),
            user = userInst
    )

    for object in club.objects.all():

        titleInst = complexTitle.objects.create(
            logo = object.logo,
            summary = object.summary,
            title = object.title,
            slug = object.slug,
            status = object.status,
            publish_date = object.publish_date,
            expiry_date = object.expiry_date,
            created = object.created,
            updated = object.updated,
            user = object.user
            )

        locInst = complexLocation.objects.create(
            complexKey = titleInst,
            title = u"اصلی",
            slug = object.slug,
            status = object.status,
            publish_date = object.publish_date,
            expiry_date = object.expiry_date,
            created = object.created,
            updated = object.updated,
            user = object.user
            )

        adrsInst = address.objects.create(
            locationKey=locInst,
            title = object.title,
            slug = object.slug,
            status = object.status,
            publish_date = object.publish_date,
            expiry_date = object.expiry_date,
            created = object.created,
            updated = object.updated,
            user = object.user,
            address = object.address,
            region = '6',
            city = u"تهران"
            )

        contact.objects.create(
            type = 'TE',
            content = object.phone,
            )

        contact.objects.create(
            type = 'CE',
            content = object.cell,
            )

        contact.objects.create(
            type = 'WB',
            content = object.website,
            )

        object.locationKey = locInst
        object.categoryKeys.add(catInst)
        object.save()
