from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from rest_framework import generics
from rest_framework import filters
import django_filters

# from accounts.views import MyRegistrationView
from generic.models import Displayable
from models import club, category, contact, address, complexTitle, complexLocation
from forms import clubRegistrationForm
from serializers import clubSerializer, clubItemSerializer

# -----------------------------------------------------------------------
class listAllItems(ListView):
    template_name = "directory/listall.html"
    model = club

    def get_queryset(self):
        return self.model.objects.filter(status = Displayable.CONTENT_STATUS_ACTIVE)
# -----------------------------------------------------------------------
class itemDetail(DetailView):
    template_name = "directory/item.html"
    model = club
# -----------------------------------------------------------------------
# class clubRegistration(MyRegistrationView):
#     template_name = 'directory/club_registration.html'
#     form_class = clubRegistrationForm
# -----------------------------------------------------------------------
#---------------------------------------------------
class getDirectoryCategoryItemList(ListView):
    #model       = complexTitle
    template_name = 'directory/categoryItems.html'
    paginate_by = 20

    def get_queryset(self):
        categoryObject = category.objects.get(title = self.kwargs['slug'])
        categoryObject.visit += 1
        categoryObject.save()
        return club.objects.filter(categoryKeys = categoryObject).select_related()
        #tag = Keyword.objects.get(slug = self.kwargs['slug']) #TODO: keyword instead category
        #return club.objects.filter(keywords__keyword=tag) #TODO: keyword instead category

        #.extra(select={'clubId':'directory_club.id'})

        #select *
        #,directory_complexTitle.id as "locationId"
        #,directory_club.id as "clubId"
        #from directory_complexTitle,directory_club,directory_address
        #where directory_complexTitle.id = directory_club.complexKey_id = directory_address.complexKey_id
        #and directory_club.categoryKey_id = ' + str(self.kwargs['pk'])

        #rawQuery = 'select *,directory_complexTitle.id as "locationId" ,directory_club.id as "clubId" from directory_complexTitle,directory_club,directory_address  where directory_complexTitle.id = directory_club.complexKey_id = directory_address.complexKey_id and directory_club.categoryKey_id = ' + str(self.kwargs['pk'])
        #TODO limit and geospatial sort
        #return complexTitle.objects.raw(rawQuery)

    def get_context_data(self, **kwargs):
        context = super(getDirectoryCategoryItemList, self).get_context_data(**kwargs)

        for item in context['object_list']:
            locationObject = item.locationKey
            item.complex = locationObject.complexKey
            item.location= locationObject
            item.address = address.objects.filter(locationKey = locationObject.pk).values()[0]
            item.contacts = contact.objects.filter(clubKey = item.pk)

        return context
#---------------------------------------------------
class getItemDetail(DetailView):
    model       = complexTitle
    template_name = 'directory/itemDetail.html'

    #def get_queryset(self):
        #return complexTitle.objects.get( slug = self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(getItemDetail, self).get_context_data(**kwargs)

        context['complex'] = self.object
        context['locations'] = self.object.complexlocation_set.all()

        if 'locationId' in self.kwargs:
            locationId = int(self.kwargs['locationId'])
        else:
            locationId = context['locations'][0].id
        context['locationId'] = locationId

        context['contacts'] = contact.objects.filter( locationKey = locationId)

        if 'clubId' in self.kwargs:
            clubId = int(self.kwargs['clubId'])
            clubObject = club.objects.get(pk = self.kwargs['clubId'])
            clubObject.visit += 1
            clubObject.save()
        else:
            clubId = 0
        context['clubId'] = clubId

        return context
#---------------------------------------------------
class getItemList(generics.ListAPIView):
    """
    List Api for Search, filter and order clubs
    title       -- search in title
    category    -- sport category
    genre       -- sport genre
    gender      -- gender
    price_min   -- price minimum
    price_max   -- price maximum
    location    -- athlete location
    distance    -- distance from location
    """
    queryset        = club.objects.all()
    serializer_class= clubSerializer
    paginate_by = 20

    def get_queryset(self):
        queryInst    = super(getItemList, self).get_queryset()

        categoryVal = self.request.query_params.get('category', None)
        titleVal    = self.request.query_params.get('title', None)

        if titleVal is not None:
            try:
                queryInst = queryInst.filter(title__icontains = titleVal)
            except:
                return ''

        if categoryVal is not None:
            try:
                categoryObject = category.objects.get(title = categoryVal)
                categoryObject.visit += 1
                categoryObject.save()
                queryInst = queryInst.filter(categoryKeys = categoryObject)
            except:
                return ''

        queryInst = queryInst.select_related()
        return queryInst
#---------------------------------------------------
class getItem(generics.RetrieveAPIView):
    """
    """
    # model = club
    lookup_field = 'pk'
    queryset = club.objects.all().select_related()
    serializer_class = clubItemSerializer

    # def get_queryset(self):
    #     return club.objects.get(pk = self.request.query_params.get('pk'))
#---------------------------------------------------
class getFav(generics.ListAPIView):
    serializer_class = clubSerializer
    queryset = club.objects.order_by('created')[:3]
#---------------------------------------------------