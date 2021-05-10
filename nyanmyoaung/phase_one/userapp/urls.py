from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from userapp import views
from django.contrib.auth.decorators import login_required
urlpatterns = [
    # Register
    path('register/', views.RegisterView.as_view(), name="register"),
    # Login
    path('phone_login/', views.PhoneLoginView.as_view(), name="phone_login"),
    path('id_login/', views.IdLoginView.as_view(), name="idlogin"),
    # Verify
    path('verify_phone/', views.PhoneVerifyView.as_view(), name="verify_phone"),
    path('verify_id/', views.IdVerifyView.as_view(), name="verify_id"),
    path('register_verification/', views.RegisterPhoneVerificationView.as_view(),
         name="register_verification"),
    # path('forgot_password/', views.ResetPasswordView.as_view(), name="forgot_password"),
    path('forgot_password_phone/', views.ForgotPasswordPhoneView.as_view(),
         name="forgot_password_phone"),
    path('forgot_password_id/', views.ForgotPasswordIdView.as_view(),
         name="forgot_password_id"),
    path('otp/', views.ValidateSendOTP.as_view(), name="otp"),
    path('logout/', views.Logout.as_view(), name="logout"),
    path('another/', views.AnotherDevice.as_view(), name="another"),
    path('refresh_token/', views.RefreshToken.as_view(), name="refresh_token"),
]
