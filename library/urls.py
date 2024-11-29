from django.urls import path

from . import views

app_name = 'library'

urlpatterns = [

    # ----------------------------- Dashboard ----------------------------- #
    path('', views.DashboardView.as_view(), name='dashboard'),

    # ------------------------------- Books ------------------------------- #
    path('books', views.BookListView.as_view(), name='book_list'),
    path('book/create/', views.BookCreateView.as_view(), name='book_create'),
    path('book/<int:pk>/update/', views.BookUpdateView.as_view(), name='book_update'),
    path('book/detail/<slug:slug>/',
         views.BookDetailView.as_view(), name='book_detail'),
    path('book/<int:pk>/delete/',
         views.BookDeleteView.as_view(), name='book_delete'),
    path('book/category/<slug:slug>/',
         views.BookListViewCategory.as_view(), name='book_category'),
    path('book/author/<slug:slug>/',
         views.BookListViewAuthor.as_view(), name='book_author'),
    path('book/publisher/<slug:slug>/',
         views.BookListViewPublisher.as_view(), name='book_publisher'),


    # ------------------------------ Authors ------------------------------ #
    path('authors/', views.AuthorListView.as_view(), name='author_list'),
    path('author/create', views.AuthorCreateView.as_view(), name='author_create'),
    path('author/detail/<slug:slug>',
         views.AuthorDetailView.as_view(), name='author_detail'),
    path('author/<int:pk>/update',
         views.AuthorUpdateView.as_view(), name='author_update'),
    path('author/<int:pk>/delete',
         views.AuthorDeleteView.as_view(), name='author_delete'),

    # ----------------------------- Publihsrs ----------------------------- #
    path('publishers/', views.PublisherListView.as_view(), name='publisher_list'),
    path('publisher/create', views.PublisherCreateView.as_view(),
         name='publisher_create'),
    path('publisher/detail/<slug:slug>',
         views.PublisherDetailView.as_view(), name='publisher_detail'),
    path('publisher/<int:pk>/update',
         views.PublisherUpdateView.as_view(), name='publisher_update'),
    path('publisher/<int:pk>/delete',
         views.PublisherDeleteView.as_view(), name='publisher_delete'),

    # ----------------------------- Categories ----------------------------- #
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('category/create', views.CategoryCreateView.as_view(),
         name='category_create'),
    path('category/detail/<slug:slug>',
         views.CategoryDetailView.as_view(), name='category_detail'),
    path('category/<int:pk>/update',
         views.CategoryUpdateView.as_view(), name='category_update'),
    path('category/<int:pk>/delete',
         views.CategoryDeleteView.as_view(), name='category_delete'),

    # ------------------------------ Students ------------------------------ #
    path('students/', views.StudentListView.as_view(), name='student_list'),
    path('student/create',
         views.StudentCreateView.as_view(), name='student_create'),
    path('student/<int:pk>/update/',
         views.StudentUpdateView.as_view(), name='student_update'),
    path('student/detail/<slug:slug>/',
         views.StudentDetailView.as_view(), name='student_detail'),
    path('student/<int:pk>/delete/',
         views.StudentDeleteView.as_view(), name='student_delete'),

    # ------------------------------- Loans  ------------------------------- #
    path('loans/', views.LoanListView.as_view(), name='loan_list'),
    path('loan/create/', views.LoanCreateView.as_view(), name='loan_create'),
    path('loan/<int:pk>/update/', views.LoanUpdateView.as_view(), name='loan_update'),
    path('loan/<int:pk>/return/',
         views.LoanBookReturnView.as_view(), name='loan_return'),
    path('loan/<int:pk>/delete/',
         views.LoanDeleteView.as_view(), name='loan_delete'),

]
