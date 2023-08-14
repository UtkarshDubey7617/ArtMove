from django.contrib import admin
from django.urls import path
admin.site.site_header='ArtMove'
from django.conf import settings
from django.conf.urls.static import static
from mainApp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('shop/<str:mc>/<str:sc>/<str:br>/', views.shoppage),
    path('singleproduct/<int:num>/', views.singleproduct),
    path('login/', views.login),
    path('logout/', views.logout),
    path('blog/', views.blog),
    path('blogdetails/', views.blogdetails),
    path('history/', views.history),
    path('signup/', views.signup),
    path('profile/', views.profilePage),
    path('updateprofile/', views.updateprofile),
    path('addproduct/', views.addproduct),
    path('editproduct/<int:num>/', views.editproduct),
    path('deleteproduct/<int:num>/', views.deleteproduct),
    path('addtowishlist/<int:num>/', views.addtowishlist),
    path('deletewishlist/<int:num>/', views.deletewishlist),
    path('addtocart/', views.addtocart),
    path('cart/', views.cart),
    path('updatecart/<str:id>/<str:num>/', views.updatecart),
    path('deletecart/<str:id>/', views.deletecart),
    path('checkout/', views.checkout),
    path('confirmation/', views.confirmation),
    path('paymentSuccess/<str:rppid>/<str:rpoid>/<str:rpsid>/',views.paymentSuccess),
    path('paynow/<int:num>/', views.paynow),
    path('contact/', views.contact),
    path('forgetusername/', views.forgetusername),
    path('forgetotp/', views.forgetotp),
    path('forgetpassword/', views.forgetpassword),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
