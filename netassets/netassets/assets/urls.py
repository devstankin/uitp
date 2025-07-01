from django.urls import path, include
from . import views

app_name = 'assets'

urlpatterns = [
    # Django Views URLs
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard_alias'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('computers/', views.computers_table, name='computers_table'),
    path('printers/', views.printers_table, name='printers_table'),
    path('switches/', views.switches_table, name='switches_table'),
    path('routers/', views.routers_table, name='routers_table'),
    path('network-devices/', views.network_devices_table, name='network_devices_table'),
    
    # Network Devices CRUD
    path('network-devices/create/', views.create_network_device, name='create_network_device'),
    path('network-devices/<int:pk>/edit/', views.edit_network_device, name='edit_network_device'),
    path('network-devices/delete/<int:pk>/', views.delete_network_device, name='delete_network_device'),
    
    # Switches CRUD
    path('switches/create/', views.create_switch, name='create_switch'),
    path('switches/<int:pk>/edit/', views.edit_switch, name='edit_switch'),
    path('switches/<int:pk>/delete/', views.delete_switch, name='delete_switch'),
    
    # Computers CRUD
    path('computers/create/', views.create_computer, name='create_computer'),
    path('computers/<int:pk>/edit/', views.edit_computer, name='edit_computer'),
    path('computers/<int:pk>/delete/', views.delete_computer, name='delete_computer'),
    
    # Printers CRUD
    path('printers/create/', views.create_printer, name='create_printer'),
    path('printers/<int:pk>/edit/', views.edit_printer, name='edit_printer'),
    path('printers/<int:pk>/delete/', views.delete_printer, name='delete_printer'),
    
    # Routers CRUD
    path('routers/create/', views.create_router, name='create_router'),
    path('routers/<int:pk>/edit/', views.edit_router, name='edit_router'),
    path('routers/<int:pk>/delete/', views.delete_router, name='delete_router'),

    # Custom Entity URLs
    path('custom-entities/', views.custom_entity_list, name='custom_entity_list'),
    path('custom-entities/<slug:entity_slug>/', views.custom_entity_detail, name='custom_entity_detail'),
    path('custom-entities/<int:entity_id>/delete/', views.delete_custom_entity, name='delete_custom_entity'),
    path('custom-entities/<slug:entity_slug>/records/', views.entity_record_list, name='entity_record_list'),
    path('e/<slug:entity_slug>/', views.entity_record_list, name='entity_record_list'),
    path('e/<slug:entity_slug>/add/', views.create_entity_record, name='entity_record_create'),
    path('e/<slug:entity_slug>/<int:record_id>/edit/', views.edit_entity_record, name='edit_entity_record'),
    path('e/<slug:entity_slug>/<int:record_id>/delete/', views.delete_entity_record, name='delete_entity_record'),
    
    # Export/Import URLs
    path('export/<str:model_name>/', views.export_csv, name='export_csv'),
    path('import/<str:model_name>/', views.import_csv, name='import_csv'),
    path('e/<slug:entity_slug>/export/', views.export_entity_csv, name='export_entity_csv'),
    path('e/<slug:entity_slug>/import/', views.import_entity_csv, name='import_entity_csv'),

    # API для карточек быстрого доступа
    path('dashboard/cards/', views.dashboard_cards_view, name='dashboard_cards_view'),
    path('dashboard/cards/add/', views.add_dashboard_card, name='add_dashboard_card'),
    path('dashboard/cards/<int:card_id>/update/', views.update_dashboard_card, name='update_dashboard_card'),
    path('dashboard/cards/<int:card_id>/delete/', views.delete_dashboard_card, name='delete_dashboard_card'),

    # User Management
    path('admin/user-management/', views.user_management, name='user_management'),
] 