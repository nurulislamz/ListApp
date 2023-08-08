from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest


from lists.views import home_page
from lists.models import Item, List

class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>To-Do lists</title>', html)
        self.assertTrue(html.endswith('</html>'))

    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(),0)

class ListAndItemModelsTest(TestCase):

    def test_saving_and_retrieving_items(self):
        # creates a list object 
        list_ = List()
        list_.save()

        # creates an item 
        first_item = Item()
        # sets text attribute of item
        first_item.text = 'The first (ever) list item'
        # sets the list attribute of the first item to the current list we're using
        first_item.list = list_
        # saves it
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        
        # list_ used cuz python built-in list function.
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        # gets all items
        saved_items = Item.objects.all()
        # checked if  count of saved items is correct
        self.assertEqual(saved_items.count(),2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        # checks if saved items are saved accurately
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)

        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)

class ListViewTest(TestCase):

    def test_displays_only_items_for_that_list(self):
        # creates an object in one list and objects in another list, compares to see if they overlap
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)
        
        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)
        
        response = self.client.get(f'/lists/{correct_list.id}/')
        
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')


    def test_uses_list_template(self):
        list = List.objects.create()
        response = self.client.get(f'/lists/{list.id}/')
        self.assertTemplateUsed(response, 'list.html')

class NewListTest(TestCase):
    def test_can_save_a_POST_request(self):
        # sends a POST request to lists/new
        # lists/new then goes to the new function which creates a list object witht the text below
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')

class NewItemTest(TestCase):
    def test_can_save_a_POST_request_to_an_existing_list(self):
        # creates two lists
        other_list = List.objects.create()
        correct_list = List.objects.create()
        
        # adds item to first list
        self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'A new item for an existing list'}
        )

        # error - not adding item rn
        # checks all the items in DB
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        # creates two lists
        other_list = List.objects.create()
        correct_list = List.objects.create()

        # new url uses to add item
        response = self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'A new item for an existing list'}
        )
        
        self.assertRedirects(response, f'/lists/{correct_list.id}/')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')   

        # checks the context of the response 
        self.assertEqual(response.context['list'], correct_list)

