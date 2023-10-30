menu = [
    # {"title":"Основная информация", "url_name":"about"},
    # {"title":"Новый список", "url_name":"add_list"},

]

class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        user_menu = menu.copy()
        context['menu'] = user_menu
        return context