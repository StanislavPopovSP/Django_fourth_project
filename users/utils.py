# Реализация поиска
from .models import Profile, Skill
from django.db.models import Q # используется для поиска любых значений

def search_profiles(request):
    """Поиск разработчиков"""
    search_query = '' # Если пользователь ни чего не введет, то будет пустая строка. search_query - значение value в шаблоне.

    if request.GET.get('search_query'): # если пользователь что-то введет search_query, будет True.
        search_query = request.GET.get('search_query') # то что ввёл перезапишем

    # поиск с точным совпадением навыков
    # skill = Skill.objects.filter(name__iexact=search_query)  # name__iexact - точное совпадение, search_query - то что будет написано в поисковой строке.

    # поиск с побуквенным совпадением навыков
    skill = Skill.objects.filter(name__icontains=search_query)

    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) |
        Q(short_info__icontains=search_query) |
        Q(skill__in=skill)
    ) # будем доставать из БД только те элементы которые имеют определенной значение. Q затем один элмент или другой. distinct() - исключить повторяющиеся элементы.
      # skill__in - в переменной skill которая включает в себя точное совпадение с нашим элементом.
      # Нельзя в поиске делать привязку нескольких сразу переменных, поэтому в поиске нужно прописать через skill__in доступ к переменной.

    return profiles, search_query