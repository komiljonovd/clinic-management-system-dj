# # import logging
# # import time
# # from django.http import JsonResponse

# # # Logger sozlamasini chaqiramiz
# # logger = logging.getLogger('django')

# # class ClinicAppMiddleware:
# #     def __init__(self, get_response):
# #         self.get_response = get_response

# #     def __call__(self, request):
# #         # 1. So'rov vaqtini o'lchash
# #         start_time = time.time()
        
# #         # 2. Response ni olish
# #         response = self.get_response(request)
        
# #         # 3. So'rov ma'lumotlarini logga yozish (INFO)
# #         duration = time.time() - start_time
# #         logger.info(
# #             f"Method: {request.method} | Path: {request.path} | "
# #             f"Status: {response.status_code} | Duration: {duration:.2f}s"
# #         )
        
# #         return response

# #     def process_exception(self, request, exception):
# #         # 4. Xatolik yuz bersa, uni logga yozish (ERROR)
# #         logger.error(f"Xatolik (URL: {request.path}): {str(exception)}", exc_info=True)
        
# #         # 5. Foydalanuvchiga 500 xatosi
# #         return JsonResponse(
# #             {"error": "Serverda kutilmagan xatolik yuz berdi."}, 
# #             status=500
# #         )


# import logging
# import time
# import traceback # Xatolik qayerdaligini ko'rsatish uchun kerak
# from django.http import JsonResponse

# logger = logging.getLogger('clinicapp')

# class ClinicAppMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         start_time = time.time()
#         response = self.get_response(request)
#         duration = time.time() - start_time
        
#         # INFO: To'liq URL va status
#         logger.info(
#             f"Method: {request.method} | Path: {request.build_absolute_uri()} | "
#             f"Status: {response.status_code} | Time: {duration:.2f}s"
#         )
#         return response

#     def process_exception(self, request, exception):
#         # 1. User ma'lumotlari
#         user_info = f"User: {request.user.username} (ID: {request.user.id})" if request.user.is_authenticated else "User: Anonymous"
        
#         # 2. Kirib kelgan ma'lumotlar (POST/JSON data)
#         # request.body ni o'qishda ehtiyot bo'lish kerak
#         try:
#             payload = request.body.decode('utf-8') if request.body else "No body"
#         except:
#             payload = "Could not decode body"

#         # 3. Chiroyli formatdagi xatolik xabari
#         error_msg = f"\n{'='*60}"
#         error_msg += f"\n[XATOLIK VAQTI]: {time.strftime('%Y-%m-%d %H:%M:%S')}"
#         error_msg += f"\n[USER]: {user_info}"
#         error_msg += f"\n[URL]: {request.build_absolute_uri()}"
#         error_msg += f"\n[METHOD]: {request.method}"
#         error_msg += f"\n[PAYLOAD/DATA]: {payload}"
#         error_msg += f"\n[ERROR TYPE]: {type(exception).__name__}"
#         error_msg += f"\n[ERROR MESSAGE]: {str(exception)}"
#         error_msg += f"\n[TRACEBACK]:\n{traceback.format_exc()}"
#         error_msg += f"\n{'='*60}\n" # Ajratuvchi chiziq
        
#         logger.error(error_msg)
        
#         return JsonResponse(
#             {"error": "Serverda xatolik yuz berdi.", "message": str(exception)}, 
#             status=500
#         )

import logging
import time
import traceback
from django.http import JsonResponse

logger = logging.getLogger('clinicapp')

class ClinicAppMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        
        # User ma'lumotlarini olish
        user_info = f"{request.user.email}(ID:{request.user.id})" if request.user.is_authenticated else "Anonymous"
        
        response = self.get_response(request)
        
        # INFO: Har bir so'rovni foydalanuvchi bilan birga yozish
        duration = time.time() - start_time
        logger.info(
            f"User: {user_info} | {request.method} {request.build_absolute_uri()} | "
            f"Status: {response.status_code} | Time: {duration:.2f}s"
        )
        return response

    def process_exception(self, request, exception):
        user_info = f"{request.user.username}(ID:{request.user.id})" if request.user.is_authenticated else "Anonymous"
        
        # Payloaddan ma'lumotlarni xavfsiz olish
        try:
            payload = request.body.decode('utf-8')[:500] if request.body else "No body"
        except:
            payload = "Binary/Decoding error"

        error_msg = (
            f"\n{'='*70}"
            f"\n[TIME]: {time.strftime('%Y-%m-%d %H:%M:%S')}"
            f"\n[USER]: {user_info}"
            f"\n[URL]: {request.build_absolute_uri()}"
            f"\n[DATA]: {payload}"
            f"\n[ERROR]: {type(exception).__name__}: {str(exception)}"
            f"\n[TRACEBACK]:\n{traceback.format_exc()}"
            f"\n{'='*70}"
        )
        
        logger.error(error_msg)
        
        return JsonResponse(
            {"error": "Tizimda xatolik yuz berdi.", "detail": str(exception)}, 
            status=500
        )