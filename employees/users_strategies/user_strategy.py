from abc import ABC, abstractmethod

class UserStrategy(ABC):
    @abstractmethod
    def post(self, request):
        pass

    @abstractmethod
    def get(self, request, user_id=None):
        pass

    @abstractmethod
    def put(self, request, user_id):
        pass

    @abstractmethod
    def delete(self, request, user_id):
        pass

    @abstractmethod
    def get_profile(self, request, user_id):
        pass
