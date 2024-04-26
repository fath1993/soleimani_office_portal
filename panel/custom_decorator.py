from functools import wraps

from django.shortcuts import redirect, render

from panel.templatetags.panel_custom_tag import user_section_is_allowed, permission_section_is_allowed, \
    role_section_is_allowed, resource_section_is_allowed, product_is_allowed, teaser_maker_is_allowed, \
    reseller_network_is_allowed, receiver_is_allowed, advertise_content_is_allowed, forward_to_portal_is_allowed, \
    communication_channel_is_allowed, registrar_is_allowed


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
            if class_self.section == 'user':
                allowed_actions = str(class_self.allowed_actions)
                if (allowed_actions.find('read') != -1 or allowed_actions.find('create') != -1 or
                        allowed_actions.find('modify') != -1 or allowed_actions.find('delete') != -1):
                    if not user_section_is_allowed(request.user, class_self.allowed_actions):
                        return render(request, 'panel/err/err-not-authorized.html')

            if class_self.section == 'permission':
                allowed_actions = str(class_self.allowed_actions)
                if (allowed_actions.find('read') != -1 or allowed_actions.find('create') != -1 or
                        allowed_actions.find('modify') != -1 or allowed_actions.find('delete') != -1):
                    if not permission_section_is_allowed(request.user, class_self.allowed_actions):
                        return render(request, 'panel/err/err-not-authorized.html')

            if class_self.section == 'role':
                allowed_actions = str(class_self.allowed_actions)
                if (allowed_actions.find('read') != -1 or allowed_actions.find('create') != -1 or
                        allowed_actions.find('modify') != -1 or allowed_actions.find('delete') != -1):
                    if not role_section_is_allowed(request.user, class_self.allowed_actions):
                        return render(request, 'panel/err/err-not-authorized.html')

            if class_self.section == 'resource':
                allowed_actions = str(class_self.allowed_actions)
                if (allowed_actions.find('read') != -1 or allowed_actions.find('create') != -1 or
                        allowed_actions.find('modify') != -1 or allowed_actions.find('delete') != -1):
                    if not resource_section_is_allowed(request.user, class_self.allowed_actions):
                        return render(request, 'panel/err/err-not-authorized.html')

            if class_self.section == 'product':
                allowed_actions = str(class_self.allowed_actions)
                if (allowed_actions.find('read') != -1 or allowed_actions.find('create') != -1 or
                        allowed_actions.find('modify') != -1 or allowed_actions.find('delete') != -1):
                    if not product_is_allowed(request.user, class_self.allowed_actions):
                        return render(request, 'panel/err/err-not-authorized.html')

            if class_self.section == 'teaser_maker':
                allowed_actions = str(class_self.allowed_actions)
                if (allowed_actions.find('read') != -1 or allowed_actions.find('create') != -1 or
                        allowed_actions.find('modify') != -1 or allowed_actions.find('delete') != -1):
                    if not teaser_maker_is_allowed(request.user, class_self.allowed_actions):
                        return render(request, 'panel/err/err-not-authorized.html')

            if class_self.section == 'reseller_network':
                allowed_actions = str(class_self.allowed_actions)
                if (allowed_actions.find('read') != -1 or allowed_actions.find('create') != -1 or
                        allowed_actions.find('modify') != -1 or allowed_actions.find('delete') != -1):
                    if not reseller_network_is_allowed(request.user, class_self.allowed_actions):
                        return render(request, 'panel/err/err-not-authorized.html')

            if class_self.section == 'receiver':
                allowed_actions = str(class_self.allowed_actions)
                if (allowed_actions.find('read') != -1 or allowed_actions.find('create') != -1 or
                        allowed_actions.find('modify') != -1 or allowed_actions.find('delete') != -1):
                    if not receiver_is_allowed(request.user, class_self.allowed_actions):
                        return render(request, 'panel/err/err-not-authorized.html')

            if class_self.section == 'advertise_content':
                allowed_actions = str(class_self.allowed_actions)
                if (allowed_actions.find('read') != -1 or allowed_actions.find('create') != -1 or
                        allowed_actions.find('modify') != -1 or allowed_actions.find('delete') != -1):
                    if not advertise_content_is_allowed(request.user, class_self.allowed_actions):
                        return render(request, 'panel/err/err-not-authorized.html')

            if class_self.section == 'forward_to_portal':
                allowed_actions = str(class_self.allowed_actions)
                if (allowed_actions.find('read') != -1 or allowed_actions.find('create') != -1 or
                        allowed_actions.find('modify') != -1 or allowed_actions.find('delete') != -1):
                    if not forward_to_portal_is_allowed(request.user, class_self.allowed_actions):
                        return render(request, 'panel/err/err-not-authorized.html')

            if class_self.section == 'communication_channel':
                allowed_actions = str(class_self.allowed_actions)
                if (allowed_actions.find('read') != -1 or allowed_actions.find('create') != -1 or
                        allowed_actions.find('modify') != -1 or allowed_actions.find('delete') != -1):
                    if not communication_channel_is_allowed(request.user, class_self.allowed_actions):
                        return render(request, 'panel/err/err-not-authorized.html')

            if class_self.section == 'registrar':
                allowed_actions = str(class_self.allowed_actions)
                if (allowed_actions.find('read') != -1 or allowed_actions.find('create') != -1 or
                        allowed_actions.find('modify') != -1 or allowed_actions.find('delete') != -1):
                    if not registrar_is_allowed(request.user, class_self.allowed_actions):
                        return render(request, 'panel/err/err-not-authorized.html')
            return view_func(self, request, *args, **kwargs)

        return wrapper
