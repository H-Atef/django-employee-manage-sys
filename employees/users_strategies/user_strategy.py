from abc import ABC, abstractmethod

class UserStrategy(ABC):
    @abstractmethod
    def post(self, request):
        pass

    @abstractmethod
    def get(self, request, pk=None):
        pass

    @abstractmethod
    def put(self, request, pk):
        pass

    @abstractmethod
    def delete(self, request, pk):
        pass

    @abstractmethod
    def get_profile(self, request, pk):
        pass
