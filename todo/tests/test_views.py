from datetime import date
from django.test import TestCase

from todo.models import Todo


class TestTodoListView(TestCase):
    """TodoListViewのテスト"""

    def setUp(self):
        self.today = date(2020, 6, 1)
        self.todo = Todo.objects.create(title='test-1', expiration_date=self.today)

    def test_get_success(self):
        """
        /todo/update/<pk>/へのGETリクエスト（正常系）
        """
        # テストクライアントでGETリクエストをシミュレート
        response = self.client.get('/todo/update/{}/'.format(self.todo.id))

        # TODO変更画面に遷移することを検証
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/todo_update.html')
        self.assertContains(response, '<h1>TODO変更</h1>')

    def test_post_success(self):
        """
        /todo/update/<pk>/へのPOSTリクエスト（正常系）
        """
        # テストクライアントでPOSTリクエストをシミュレート
        response = self.client.post('/todo/update/{}/'.format(self.todo.id), {
            'title': 'test-1-updated',
        }, follow=True)

        # TODOリスト画面にリダイレクトされることを検証
        self.assertRedirects(response, '/todo/')
        self.assertTemplateUsed(response, 'todo/todo_list.html')
        self.assertContains(response, '<h1>TODOリスト</h1>')

        # 対象オブジェクトが更新されていることを検証
        todo = Todo.objects.get(pk=self.todo.id)
        self.assertEqual(todo.title, 'test-1-updated')

    def test_post_if_title_is_blank(self):
        """
        /todo/update/<pk>/へのPOSTリクエスト（バリデーションNG）
        """
        # テストクライアントでPOSTリクエストをシミュレート
        response = self.client.post('/todo/update/{}/'.format(self.todo.id), {
            'title': '',
        })

        # TODO変更画面に遷移することを検証
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/todo_update.html')
        self.assertContains(response, '<h1>TODO変更</h1>')

        # エラーメッセージが表示されることを検証
        self.assertEqual(
            response.context_data['form'].errors,
            {'title': ['このフィールドは必須です。']}
        )

        # 対象オブジェクトが更新されていないことを検証
        todo = Todo.objects.get(pk=self.todo.id)
        self.assertEqual(todo.title, 'test-1')
