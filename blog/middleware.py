# from .models import MyBlog

# def simple_middleware(get_response):
   

#     def middleware(request , id):
#         # Code to be executed for each request before
#         # the view (and later middleware) are called.
#         blog = MyBlog.objects.get(id = id)
#         user = request.user
#         if user.is_special and blog.status == 's'  :
#             return blog
#         else :
#             return request

#         response = get_response(request)

#         # Code to be executed for each request/response after
#         # the view is called.

#         return response

#     return middleware