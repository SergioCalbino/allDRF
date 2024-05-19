
from home.views import index, person, personId, login, PersonAPI, PeopleVieSet, RegisterApi
from django.urls import path, include

# Para la rutas de apiviewset se usa esto

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'people', PeopleVieSet, basename='people')
urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterApi.as_view()),
    path('index/', index ),
    path('person/', person ),
    path('person2/<int:id>/', personId ),
    path('login/', login ),
    # Este ultimo es la url de la class Person en la vista, por eso lo defino asi
    path('persons/', PersonAPI.as_view() ),
]
