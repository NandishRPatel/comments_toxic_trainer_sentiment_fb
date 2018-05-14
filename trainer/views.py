from django.shortcuts import render
from django.views.generic import FormView, View
from django.http import JsonResponse
from open_facebook.api import OpenFacebook
import random,re
from textblob import TextBlob
from mtranslate import translate
from comments_toxic_trainer.settings import access_token

from .models import ToxicComments
from .forms import ProfileForm

class ProfilePostView(View):

    def get(self, request, *args, **kwargs):
        post_id = self.kwargs['post_id']
        profile = self.kwargs['profile']

        graph = OpenFacebook(access_token)
        post = graph.get('{0}'.format(post_id))
        comments = graph.get('{0}/comments'.format(post_id))
        context = {}
        measure=[]
        for i in comments['data']:
            measure.append(round(self.get_comment_sentiment(i['message']),2))

        context['comments'] = comments['data']

        for i in range(len(context['comments'])):
            context['comments'][i].update({'measure': measure[i]})

        context['profile'] = profile
        context['post_id'] = post_id

        return render(request, "comments.html", context=context)

    def clean_comment(self,comment): return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", comment).split())

    def get_comment_sentiment(self,comment):
        analysis = TextBlob(translate(self.clean_comment(comment),"en",'auto'))
        return analysis.sentiment.polarity


    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        comment_id = request.POST.get('comment_id')
        comment_text = request.POST.get('comment_text')
        toxic_value = request.POST.get('toxic_value')

        obj, created = ToxicComments.objects.get_or_create(comment_id=comment_id, comment_text=comment_text, toxicity=toxic_value)

        return render(request,"success.html")

class ProfileView(FormView):
    form_class = ProfileForm
    template_name = "profile.html"

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        form = self.get_form()
        if form.is_valid():
            profile_id = form.cleaned_data['profile_id']
            # print profile_id

            graph = OpenFacebook(access_token);
            profile = graph.get('{0}'.format(profile_id))
            posts = graph.get('{0}/posts'.format(profile_id))
            context = self.get_context_data()
            context['profile'] = profile_id
            context['posts'] = posts['data']
            context['next_posts'] = posts['paging']['next']

            return render(request, "posts.html", context=context)
            # return self.form_valid(form)
        else:
            return self.form_invalid(form)

def save_toxic_comment(request):
    msg = "not saved"

    profile_id = request.GET.get('profile_id', None)
    print(profile_id)
    post_id = request.GET.get('post_id', None)
    comment_text = request.GET.get('comment_text', None)
    comment_user_id = request.GET.get('comment_user_id', None)
    comment_time = request.GET.get('comment_time', None)
    toxicity = request.GET.get('toxicity', None)

    obj = {
        'profile_id': profile_id,
        'post_id': post_id,
        'comment_user_id': comment_user_id,
        'comment_text':comment_text,
        'comment_time': comment_time,
        'toxicity': toxicity
    }
    print (obj)

    try:
        obj = ToxicComments.objects.get(post_id=post_id, comment_time=comment_time)
        for key, value in obj.items():
            setattr(obj, key, value)
        obj.save()
        msg = "saved"
    except ToxicComments.DoesNotExist:
        obj = ToxicComments(**obj)
        obj.save()
        msg = "saved"

    data = {
        'message': msg
    }
    return JsonResponse(data)
