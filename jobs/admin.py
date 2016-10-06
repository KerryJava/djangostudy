from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html
from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404 
from django.core.mail import send_mail  
from django.contrib.admin import site
from adminactions import actions
from daterange_filter.filter import DateRangeFilter

# Register your models here.
from.models import Question, Choice, AuthorForm, Author, BookAuthor, Picture, Comment, Person

site_title = "Mjc admin"

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class AuthorInline(admin.StackedInline):
    model = Author
    extra = 3

class AuthorStackedInline(admin.StackedInline):
    model = Author
    extra = 2

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date', 'question_text',  ('pub_date', DateRangeFilter),  ]
    search_fields = ['question_text']

    fieldsets = [
        (None, {
            'fields': ['question_text']
        }), ('Date information', {
            'fields': ['pub_date'],
            'classes': ['collapse']
        }),
    ]
    inlines = [ChoiceInline, AuthorInline, AuthorStackedInline]
    form = AuthorForm

    def get_queryset(self, request):
        qs = super(QuestionAdmin, self).get_queryset(request).filter(question_text='777')
        qs = super(QuestionAdmin, self).get_queryset(request)

        print "get_queryset"
        qsList = (qs)
        print qsList, type(qsList)
        print request

        return qsList


class ProductiveAuthorsFilter(admin.SimpleListFilter):
    parameter_name = 'is_productive'
    title = 'Productive author'
    YES, NO = 1, 0
    # title = _('decade born')


    # Number of comments for an author to be considered a productive one
    THRESHOLD = 2

    def lookups(self, request, model_admin):
        return (
            (self.YES, 'yesssss'),
            (self.NO, 'no'),
        )

    def queryset(self, request, queryset2):

        qs = queryset2.annotate(Count('comments'))

        # Note the syntax. This way we avoid touching the queryset if our
        # filter is not used at all.
        print "-----\n " , self.value(), qs,qs[0], qs[0].comments__count, "next \n",qs[1], qs[1].comments__count
        print qs.filter(comments__count__gte=self.THRESHOLD)
        print "\n"
        print qs.filter(comments__count__lt=self.THRESHOLD)
        print "\nend\n"
        print "-----    " ,  self.YES, self.NO
        # return qs.filter(animal_kind=1)
        if str(self.value()) == str(self.YES):
            print "select yes"
            return qs.filter(animal_kind=1)

            return qs.filter(comments__count__gte=self.THRESHOLD)
        if str(self.value()) == str(self.NO):
            print "select no"

            return qs.filter(comments__count__lt=self.THRESHOLD)

        print "no select "
        return queryset2

class PictureAdmin(admin.ModelAdmin):
    list_display = ('animal_kind', 'author', 'is_promoted', 'object_link', 'mail_link')
    list_display_fields = ( 'animal_kind', 'author', 'is_promoted', 'object_link' )
    list_filter = [ ProductiveAuthorsFilter]
    list_fields = [ 'object_link']
    list_select_related = True

    def object_link(self, item):
        url = item.get_absolute_url()
        return format_html(u'<a href="{url}">open</a>', url=url)
    # object_link.short_description = 'View on site'

    actions = ['promote', ]
    # list_editable = ('editors_note', )


    def promote(self, request, queryset):
        print queryset
        print queryset.query
        print queryset.model
        queryset.update(is_promoted=True)
        self.message_user(request, 'The posts are promoted')
    promote.short_description = 'Promote the pictures'

    def mail_link(self, obj):
        dest = reverse('admin:myapp_pictures_mail_author',
                       kwargs={'pk': obj.pk})
        return format_html('<a href="{url}">{title}</a>',
                           url=dest, title='send mail')
    mail_link.short_description = 'Show some love'
    mail_link.allow_tags = True

    def get_urls(self):
        urls = [
            url('^(?P<pk>\d+)/sendaletter/?$',
                self.admin_site.admin_view(self.mail_view),
                name='myapp_pictures_mail_author'),
        ]
        return urls + super(PictureAdmin, self).get_urls()

    def mail_view(self, request, *args, **kwargs):
        obj = get_object_or_404(Picture, pk=kwargs['pk'])
        send_mail('Feel the granny\'s love', 'Hey, she loves your pet!',
                  'granny@yoursite.com', [obj.author.email])
        self.message_user(request, 'The letter is on its way')
        return redirect(reverse('admin:myapp_picture_changelist'))

class AuthorAdmin(admin.ModelAdmin):
    list_display_fields = ('name', 'email', )
    list_filter = ['name']


class CommentAdmin(admin.ModelAdmin):
    list_display = ('picture', 'author', 'editors_note',)
    list_editable = ("author", "editors_note", )
    # def queryset (self, request):
    #     qs = Question.objects.order_by('-pub_date')[:1]
    #     ordering = self.get_ordering(request)
    #     print "queryset"
    #     if ordering:
    #         qs = qs.order_by(*ordering)
    #     return qs
    pass
# admin.site.register(AuthorForm, QuestionAdmin)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'colored_name')

admin.site.register(Question, QuestionAdmin)
admin.site.register(Picture, PictureAdmin)
admin.site.register(BookAuthor, AuthorAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Person, PersonAdmin)
actions.add_to_site(site)
