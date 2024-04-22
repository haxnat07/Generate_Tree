from django.urls import path
from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView
from .views import premium,tree_page,add_people,people_list,add_entry,entry_list,generate_tree

urlpatterns = [
    path('', views.home, name="blog-home"),
    path('about/', views.about, name="blog-about"),
    path('stories/', PostListView.as_view(), name="blog-stories"),
    path('post-new/', PostCreateView.as_view(), name="blog-new"),
    path('post/<int:pk>/', PostDetailView.as_view(), name="blog-detail"),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name="blog-update"),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name="blog-delete"),
    path('free-plan/', PostCreateView.as_view(), name="free-plan"),
    path('premium-plan/', PostCreateView.as_view(), name="premium-plan"),
    path('search-stories/', views.StorySearchView.as_view(), name='search_stories'),
    path('contact_submit/', views.contact_submit, name='contact-submit'),
    path('premium/', views.premium, name='premium'),
    path('tree/', views.tree_page, name='tree'),

    path('add_people/', views.add_people, name='add_people'),
    path('people_list/', views.people_list, name='people_list'),
    path('add_entry/<int:pk>', views.add_entry, name='add_entry'),
    path('entry_list/<int:pk>', views.entry_list, name='entry_list'),
    path('generate_tree/<int:pk>', views.generate_tree, name='generate_tree'),
]
