from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import Http404
from django.template.response import TemplateResponse
from django.utils import timezone
from django.views import View

from .forms import TodoForm
from .models import Todo


# Step 1. はじめての画面表示
# def todo_list(request):
#     if request.method == 'GET':
#         today = timezone.localdate()
#         return HttpResponse('今日は {} です。'.format(today))


# Step 2. クラスベースで書き直す
# class TodoListView(View):
#     def get(self, request, *args, **kwargs):
#         today = timezone.localdate()
#         return HttpResponse('今日は {} です。'.format(today))


# Step 3. HTMLを使ったレスポンスを返す
# class TodoListView(View):
#     def get(self, request, *args, **kwargs):
#         today = timezone.localdate()
#         return HttpResponse("""
# <html>
# <body>
# <h1>TODOリスト</h1>
# <p>今日は {} です。</p>
# </body>
# </html>
#         """.format(today))


# Step 4. テンプレートを使う
# class TodoListView(View):
#     def get(self, request, *args, **kwargs):
#         today = timezone.localdate()
#         context = {
#             'today': today,
#         }
#         return TemplateResponse(request, 'todo/todo_list_step4.html', context)


# Step 5. モデルを使う
class TodoListView(View):
    def get(self, request, *args, **kwargs):
        today = timezone.localdate()
        todo_list = Todo.objects.order_by('expiration_date')
        context = {
            'today': today,
            'todo_list': todo_list,
        }
        # return TemplateResponse(request, 'todo/todo_list_step5.html', context)
        return TemplateResponse(request, 'todo/todo_list.html', context)


# Step 6. TODO追加画面を作成する
class TodoCreateView(View):
    def get(self, request, *args, **kwargs):
        # 空のフォームを作成して画面に表示
        context = {
            'form': TodoForm(),
        }
        return TemplateResponse(request, 'todo/todo_create.html', context)

    def post(self, request, *args, **kwargs):
        # リクエストパラメータからフォームを作成
        form = TodoForm(request.POST)
        # フォームを使ってバリデーション
        if not form.is_valid():
            # バリデーションNGの場合はリクエスト元の画面のテンプレートを再表示
            context = {
                'form': form,
            }
            return TemplateResponse(request, 'todo/todo_create.html', context)

        # オブジェクトを保存
        form.save()
        # TODOリスト画面にリダイレクト
        return HttpResponseRedirect('/todo/')


# Step 7. TODO変更画面を作成する
class TodoUpdateView(View):
    def get(self, request, pk, *args, **kwargs):
        # 対象レコードを取得
        try:
            todo = Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            raise Http404

        # 対象レコードからフォームを作成して画面に表示
        context = {
            'form': TodoForm(instance=todo),
        }
        return TemplateResponse(request, 'todo/todo_update.html', context)

    def post(self, request, pk, *args, **kwargs):
        # 対象レコードを取得
        try:
            todo = Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            raise Http404

        # リクエストパラメータと対象レコードからフォームを作成
        form = TodoForm(request.POST, instance=todo)
        # フォームを使ってバリデーション
        if not form.is_valid():
            # バリデーションNGの場合はリクエスト元の画面のテンプレートを再表示
            context = {
                'form': form,
            }
            return TemplateResponse(request, 'todo/todo_update.html', context)

        # オブジェクトを更新
        form.save()
        # TODOリスト画面にリダイレクト
        return HttpResponseRedirect('/todo/')
