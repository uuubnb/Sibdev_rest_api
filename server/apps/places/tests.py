from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth.models import User
from apps.places.models import Place, Meal, Ingredient
from rest_framework.authtoken.models import Token


class UserActionsTest(APITestCase):
    def setUp(self):
        self.test_user = {'username': 'testuser', 'password': 'testpassword'}
        self.users_url = reverse('users-list')
        self.count_before = User.objects.count()

    def test_post_user_success(self):
        """
        Test that user instance created on 'POST' and proper fields returned.
        """
        response = self.client.post(self.users_url, self.test_user)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), self.count_before + 1)

        self.assertTrue('id' in response.data)
        self.assertTrue('username' in response.data)
        self.assertTrue('token' in response.data)

        self.assertEqual(self.test_user['username'], response.data['username'])


class TokenActionsTest(APITestCase):
    def setUp(self):
        self.user = {'username': 'testuser', 'password': 'testpassword'}
        self.wrong_user = {'username': 'wronguser', 'password': 'wrongpassword'}
        self.user_url = reverse('users-list')
        self.token_url = reverse('tokens')

        self.count_before = Token.objects.count()

    def test_create_user_returns_token(self):
        """
        Test that proper token returns on user creation.
        """
        response = self.client.post(self.user_url, self.user, format='json')
        token = User.objects.get(username=self.user['username']).auth_token

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Token.objects.count(), self.count_before + 1)

        self.assertTrue('token' in response.data)

        self.assertEqual(type(response.data['token']), str)
        self.assertEqual(token.key, response.data['token'])

    def test_api_auth_token_returns(self):
        """
        Test that proper token returns given proper username and password on /api/auth/token.
        """
        self.client.post(self.user_url, self.user, format='json')
        response = self.client.post(self.token_url, self.user, format='json')
        token = User.objects.get(username=self.user['username']).auth_token

        self.assertTrue('token' in response.data)

        self.assertEqual(type(response.data['token']), str)
        self.assertEqual(token.key, response.data['token'])

    def test_api_auth_token_fails(self):
        """
        Test that token doesn't return given wrong username and password on /api/auth/token.
        """
        response = self.client.post(self.token_url, self.wrong_user, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PlaceActionsTest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create(username='testowner', password='testownerpassword')
        self.user = User.objects.create(username='testuser', password='testpassword')
        self.owners_token = Token.objects.create(user=self.owner)
        self.users_token = Token.objects.create(user=self.user)

        self.place = Place.objects.create(
            owner=self.owner,
            name='someplace',
            address='Красноярск Дубровинского, 1',
        )
        self.count_before = Place.objects.count()
        self.place_url = reverse('places-detail', args=(self.place.id,))

        self.test_place = {'name': 'testplace', 'address': 'Красноярск Дубровинского, 106'}

    def test_post_place_success(self):
        """
        Test that place instance created on 'POST' and proper fields returned.
        """
        url = reverse('places-list')

        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.owners_token))
        response = self.client.post(url, self.test_place)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Place.objects.count(), self.count_before + 1)

        self.assertTrue('id' in response.data)
        self.assertTrue('name' in response.data)
        self.assertTrue('address' in response.data)
        self.assertTrue('latitude' in response.data)
        self.assertTrue('longitude' in response.data)

        self.assertEqual(self.test_place['name'], response.data['name'])
        self.assertEqual(self.owner.id, response.data['owner'])

    def test_post_places_forbidden(self):
        """
        Test 'POST' for places doesn't work for unauthenticated users
        """
        url = reverse('places-list')

        self.client.credentials()
        response = self.client.post(url, self.test_place)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_place_forbidden(self):
        """
        Test that 'PUT', 'PATCH' not allowed for unauthenticated user.
        """
        self.client.credentials()
        response = self.client.put(self.place_url, self.test_place)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_place_forbidden_notowner(self):
        """
        Test that 'PUT', 'PATCH' not allowed if user is not place owner.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.users_token))
        response = self.client.put(self.place_url, self.test_place)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_place_allowed(self):
        """
        Test that 'PUT', 'PATCH' allowed for place owner.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.owners_token))
        response = self.client.put(self.place_url, self.test_place)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_place_forbidden(self):
        """
        Test that 'DELETE' not allowed for unauthenticated user.
        """
        self.client.credentials()
        response = self.client.delete(self.place_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_place_forbidden_notowner(self):
        """
        Test that 'DELETE' not allowed if user is not place owner.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.users_token))
        response = self.client.delete(self.place_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_place_allowed(self):
        """
        Test that 'DELETE' allowed for place owner.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.owners_token))
        response = self.client.delete(self.place_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_place_allowed(self):
        """
        Test that `list` action allowed for regular user.
        """
        url = reverse('places-list')

        self.client.credentials()
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_place_allowed(self):
        """
        Test that `get` action allowed for regular user.
        """
        response = self.client.get(self.place_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class MealActionsTest(APITestCase):
    def setUp(self):
        # PlaceActionsTest.setUp(self.owners_token)
        self.owner = User.objects.create(username='testowner', password='testownerpassword')
        self.user = User.objects.create(username='testuser', password='testpassword')
        self.owners_token = Token.objects.create(user=self.owner)
        self.users_token = Token.objects.create(user=self.user)

        self.place = Place.objects.create(
            owner=self.owner,
            name='testplace',
            address='Красноярск Дубровинского, 106',
        )
        self.meal = Meal.objects.create(
            name="testmeal",
            place=self.place,
            price="1005.00",
        )
        self.meal.ingredients.add(1, 2, 3)
        self.count_before = Meal.objects.count()

        self.test_meal = {
            "name": "somemeal",
            "place": self.place.id,
            "price": "115.00",
            "ingredients": [5, 6, 7]
        }
        self.meal_url = reverse('meals-detail', args=(self.meal.id,))

    def test_post_meal_success(self):
        """
        Test that meal instance created on 'POST' and proper fields returned.
        """
        url = reverse('meals-list')

        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.owners_token))
        response = self.client.post(url, self.test_meal)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Meal.objects.count(), self.count_before + 1)

        self.assertTrue('id' in response.data)
        self.assertTrue('name' in response.data)
        self.assertTrue('place' in response.data)
        self.assertTrue('price' in response.data)
        self.assertTrue('ingredients' in response.data)
        self.assertTrue('total_calories' in response.data)

        self.assertEqual(self.test_meal['name'], response.data['name'])

    def test_post_meal_forbidden(self):
        """
        Test POST for meals doesn't work for unauthenticated users
        """
        url = reverse('meals-list')

        self.client.credentials()
        response = self.client.post(url, self.test_meal)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_meal_forbidden(self):
        """
        Test that 'PUT', 'PATCH' not allowed for unauthenticated user.
        """
        self.client.credentials()
        response = self.client.put(self.meal_url, self.test_meal)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_meal_forbidden_notowner(self):
        """
        Test that 'PUT', 'PATCH' not allowed if user is not place owner.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.users_token))
        response = self.client.put(self.meal_url, self.test_meal)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_meal_allowed(self):
        """
        Test that 'PUT', 'PATCH' allowed for place owner.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.owners_token))
        response = self.client.put(self.meal_url, self.test_meal)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_meal_forbidden(self):
        """
        Test that 'DELETE' not allowed for unauthenticated user.
        """
        self.client.credentials()
        response = self.client.delete(self.meal_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_meal_forbidden_notowner(self):
        """
        Test that 'DELETE' not allowed if user is not place owner.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.users_token))
        response = self.client.delete(self.meal_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_meal_allowed(self):
        """
        Test that 'DELETE' allowed for place owner.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.owners_token))
        response = self.client.delete(self.meal_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_meal_allowed(self):
        """
        Test that `list` action allowed for regular user.
        """
        url = reverse('places-list')

        self.client.credentials()
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_meal_allowed(self):
        """
        Test that `get` action allowed for regular user.
        """
        response = self.client.get(self.meal_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class IngredientActionsTest(APITestCase):
    def setUp(self):
        # PlaceActionsTest.setUp(self.owners_token)
        self.user = User.objects.create(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        ingredient = Ingredient.objects.create(name='some_ingredient', calories='100')

        self.test_ingredient = {
            "name": "ingredient0",
            "calories": "123"
        }

        self.ingredient_url = reverse('ingredients-detail', args=(ingredient.id,))

    def test_post_ingredients_forbidden_unauth(self):
        """
        Test 'POST' for ingredients doesn't work for unauthenticated user
        """
        url = reverse('ingredients-list')

        self.client.credentials()
        response = self.client.post(url, self.test_ingredient)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_ingredients_forbidden(self):
        """
        Test 'POST' for ingredients doesn't work for authenticated user
        """
        url = reverse('ingredients-list')

        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.token))
        response = self.client.post(url, self.test_ingredient)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_ingredient_forbidden_unauth(self):
        """
        Test 'PUT', 'PATCH' for ingredients doesn't work for unauthenticated user
        """
        self.client.credentials()
        response = self.client.put(self.ingredient_url, self.test_ingredient)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_ingredient_forbidden(self):
        """
        Test 'PUT', 'PATCH' for ingredients doesn't work for authenticated user
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.token))
        response = self.client.put(self.ingredient_url, self.test_ingredient)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_ingredient_forbidden_unauth(self):
        """
        Test 'DELETE' for ingredients doesn't work for unauthenticated user
        """
        self.client.credentials()
        response = self.client.delete(self.ingredient_url, self.test_ingredient)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_ingredient_forbidden(self):
        """
        Test 'DELETE' for ingredients doesn't work for authenticated user
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.token))
        response = self.client.delete(self.ingredient_url, self.test_ingredient)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_list_ingredient_allowed(self):
        """
        Test that `list` action allowed for regular user.
        """
        url = reverse('ingredients-list')

        self.client.credentials()
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_ingredient_allowed(self):
        """
        Test that `get` action allowed for regular user.
        """
        response = self.client.get(self.ingredient_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

