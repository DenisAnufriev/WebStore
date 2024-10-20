from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from pytils.translit import slugify

from blog.forms import ArticleUpdateForm
from blog.models import Article


class ArticleListView(ListView):
    """
    Представление для отображения списка статей блога.

    Отображает только опубликованные статьи.
    """

    model = Article

    def get_queryset(self, *args, **kwargs):
        """
        Возвращает отфильтрованный список статей, которые опубликованы.
        """
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class ArticleDetailView(DetailView):
    """
    Представление для отображения деталей статьи.

    Увеличивает счетчик просмотров при каждом обращении к статье.
    """

    model = Article

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class ArticleCreateView(CreateView):
    """
    Представление для создания новой статьи.

    После успешного создания статьи устанавливает slug на основе заголовка.
    """

    model = Article
    form_class = ArticleUpdateForm
    success_url = reverse_lazy("blog:article_list")

    def form_valid(self, form):
        if form.is_valid():
            item = form.save()
            item.slug = slugify(item.title)
            item.save()
        return super().form_valid(form)


class ArticleUpdateView(UpdateView):
    """
    Представление для редактирования существующей статьи.

    После успешного редактирования перенаправляет на страницу детали статьи.
    """

    model = Article
    form_class = ArticleUpdateForm

    def get_success_url(self):
        return reverse("blog:article_detail", kwargs={"pk": self.object.pk})


class ArticleDeleteView(DeleteView):
    """
    Представление для удаления статьи.

    После успешного удаления перенаправляет на список статей.
    """

    model = Article
    success_url = reverse_lazy("blog:article_list")
