from django.contrib import admin
from django.db.models import Count
# Register your models here.
from.models import Question, Choice, AuthorForm, Author, BookAuthor, Picture, Comment

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
    list_filter = ['pub_date', 'question_text'  ]
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
        return qs

class PictureAdmin(admin.ModelAdmin):
    list_display_fields = ('photo', 'animal_kind', 'author', 'is_promoted', )
    list_filter = [ ProductiveAuthorsFilter]

class AuthorAdmin(admin.ModelAdmin):
    list_display_fields = ('name', 'email', )
    list_filter = ['name']


class CommentAdmin(admin.ModelAdmin):
    list_display_fields = ('picture', 'author', )
    # def queryset (self, request):
    #     qs = Question.objects.order_by('-pub_date')[:1]
    #     ordering = self.get_ordering(request)
    #     print "queryset"
    #     if ordering:
    #         qs = qs.order_by(*ordering)
    #     return qs
# admin.site.register(AuthorForm, QuestionAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Picture, PictureAdmin)
admin.site.register(BookAuthor, AuthorAdmin)
admin.site.register(Comment, CommentAdmin)