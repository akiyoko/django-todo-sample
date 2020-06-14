from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import Http404
from django.template.response import TemplateResponse
from django.utils import timezone
from django.views import View

from .forms import TodoForm
from .models import Todo


# No.1: はじめての画面表示
def todo_list(request):
    if request.method == 'GET':
        today = timezone.localdate()
        return HttpResponse('今日は {} です。'.format(today))


# No.2: クラスベースで書き直す
class TodoListView(View):
    def get(self, request, *args, **kwargs):
        today = timezone.localdate()
        return HttpResponse('今日は {} です。'.format(today))


# No.3: HTMLを使ったレスポンスを返す
class TodoListView(View):
    def get(self, request, *args, **kwargs):
        today = timezone.localdate()
        return HttpResponse("""
<html>
<body>
<h1>TODOリスト</h1>
<p>今日は {} です。</p>
</body>
</html>
        """.format(today))


# No.4: テンプレートを使う
class TodoListView(View):
    def get(self, request, *args, **kwargs):
        today = timezone.localdate()
        context = {
            'today': today,
        }
        return TemplateResponse(request, 'todo/todo_list.html', context)


# No.5: モデルを使う
class TodoListView(View):
    def get(self, request, *args, **kwargs):
        today = timezone.localdate()
        todo_list = Todo.objects.order_by('expiration_date')
        context = {
            'today': today,
            'todo_list': todo_list,
        }
        return TemplateResponse(request, 'todo/todo_list.html', context)


class TodoCreateView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'form': TodoForm(),
        }
        return TemplateResponse(request, 'todo/todo_create.html', context)

    def post(self, request, *args, **kwargs):
        # リクエストからフォームを作成
        form = TodoForm(request.POST)
        # バリデーション
        if not form.is_valid():
            # バリデーションNGの場合は追加画面のテンプレートを再表示
            context = {
                'form': form,
            }
            return TemplateResponse(request, 'todo/todo_create.html', context)

        # オブジェクトを保存
        form.save()
        return HttpResponseRedirect('/todo/')


class TodoUpdateView(View):
    def get(self, request, pk, *args, **kwargs):
        try:
            todo = Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            raise Http404

        context = {
            'form': TodoForm(instance=todo),
        }
        return TemplateResponse(request, 'todo/todo_update.html', context)

    def post(self, request, pk, *args, **kwargs):
        try:
            todo = Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            raise Http404

        # リクエストからフォームを作成
        form = TodoForm(request.POST, instance=todo)
        # バリデーション
        if not form.is_valid():
            # バリデーションNGの場合は追加画面のテンプレートを再表示
            context = {
                'form': form,
            }
            return TemplateResponse(request, 'todo/todo_update.html', context)

        # オブジェクトを保存
        form.save()
        return HttpResponseRedirect('/todo/')
