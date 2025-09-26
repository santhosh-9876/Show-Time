from django.urls import reverse
from django.shortcuts import redirect

class RedirectAuthenticatedUserMidleware:
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self,request):
        
        # check the user is athenticated 
        if request.user.is_authenticated:
            # List of the paths to check 
            paths_to_redirect =[reverse('login'),reverse('register')]

            if request.path in paths_to_redirect:
                return redirect(reverse('index'))
            
        response = self.get_response(request)
        return response