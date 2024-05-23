from functools import wraps

from django.shortcuts import redirect, render

from accounts.templatetags.account_custom_tag import has_access_to_section


class CheckLogin:
    def __call__(class_self, view_func):  # we name self to class_self in favor of not being conflict with warp's self
        @wraps(view_func)
        def wrapper(self, request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('accounts:login')
            return view_func(self, request, *args, **kwargs)

        return wrapper


class RequireMethod:
    def __init__(class_self, allowed_method):
        class_self.allowed_method = allowed_method  # it should be like: GET,POST,PUT,DELETE

    def __call__(class_self, view_func):  # we name self to class_self in favor of not being conflict with warp's self
        @wraps(view_func)
        def wrapper(self, request, *args, **kwargs):
            if str(class_self.allowed_method).find(f'{request.method}') == -1:
                return redirect('panel:panel-dashboard')
            return view_func(self, request, *args, **kwargs)

        return wrapper


class CheckPermissions:
    def __init__(class_self, section, allowed_actions=None):
        class_self.section = section
        class_self.allowed_actions = allowed_actions

    def __call__(class_self, view_func):  # we name self to class_self in favor of not being conflict with warp's self
        @wraps(view_func)
        def wrapper(self, request, *args, **kwargs):
            allowed_actions = str(class_self.allowed_actions)
            if (allowed_actions.find('read') != -1 or allowed_actions.find('create') != -1 or
                    allowed_actions.find('modify') != -1 or allowed_actions.find('delete') != -1):
                if not has_access_to_section(request.user, f'{class_self.allowed_actions},{class_self.section}'):
                    return render(request, 'panel/err/err-not-authorized.html')

            return view_func(self, request, *args, **kwargs)

        return wrapper
