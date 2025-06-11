from django.test import TestCase
from api.models import Order, User
from django.urls import reverse
from rest_framework import status

# This class defines tests for the "user-orders" endpoint,
# ensuring it behaves correctly for authenticated and unauthenticated users.
class userOrderTestCase(TestCase):
    
    # The setUp method is called before each test method.
    # It sets up the test data: two users and four orders (2 for each user).
    def setUp(self):
        user1 = User.objects.create_user(username='user1', password='test')
        user2 = User.objects.create_user(username='user2', password='test')
        
        # Create 2 orders for user1
        Order.objects.create(user=user1)
        Order.objects.create(user=user1)
        
        # Create 2 orders for user2
        Order.objects.create(user=user2)
        Order.objects.create(user=user2)
    
    # Test to ensure that only the authenticated user's orders are returned
    def test_user_order_endpoint_retrieves_only_authenticated_user_orders(self):
        # Log in as user1
        user = User.objects.get(username='user1')
        self.client.force_login(user)  # Force login without password auth
        
        # Call the user-orders endpoint (uses the name defined in urls.py)
        response = self.client.get(reverse('user-orders'))
        
        # Assert that the response status is 200 OK
        #assert response.status_code == 200
        assert response.status_code == status.HTTP_200_OK #better readable
        
        # Get the parsed JSON response (a list of order dictionaries)
        orders = response.json()
        print(orders)  # Useful for debugging the output structure
        
        # Check that all returned orders belong to the logged-in user
        self.assertTrue(all(order['user']['id'] == user.id for order in orders))
    
    # Test to ensure that unauthenticated users cannot access the endpoint
    def test_user_order_list_unauthenticated(self):
        # Send request without logging in
        response = self.client.get(reverse('user-orders'))
        
        # Expecting HTTP 403 Forbidden (you may get 401 if using custom permissions)
        #self.assertEqual(response.status_code, 403)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) #much readable
