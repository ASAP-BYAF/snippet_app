import io

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from api.models import User
from api.serializers import UserSerializer

# Create a instance of model
user = User(user_id='test_user_cde', password='test_user_cde')
#user.save()
print(f'user = {user}')

# Transform the instance to the serialized data
serializer = UserSerializer(user)
data = serializer.data
print(f'serializer = {serializer}')
print(f'data = {data}')

# Transform the serialized data to the json data
content = JSONRenderer().render(data)
print(f'content = {content}')

# Json to stream
stream = io.BytesIO(content)
print(f'stream = {stream}')

# Stream to serialized data
data2 = JSONParser().parse(stream)
print(f'data2 = {data2}')

# serialized data to serializer
serializer = UserSerializer(data=data2)
print(f'serializer = {serializer}')
# serializer.save()
