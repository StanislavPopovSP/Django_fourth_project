from .models import Profile, Skill
from django.db.models import Q # используется для поиска любых значений

def search_profiles(request):
    """Поиск разработчиков"""
    search_query = ''

    if request.GET.get('search_query'): # Будем получать доступ по имени search_query, если пользователь что-то введет, будет True.
        search_query = request.GET.get('search_query')

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

    return profiles, search_query