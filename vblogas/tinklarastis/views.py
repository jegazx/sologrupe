from django.views import View
from django.views.generic import ListView, DetailView, DeleteView, CreateView
from .models import BlogPost, Category, Comment, Video
from django.shortcuts import render, redirect
from .forms import VideoForm, CommentForm, BlogPostForm
from django.shortcuts import render, get_object_or_404, redirect
from .thumbnail_generator import generate_thumbnail
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os, uuid


# Create your views here.
class Index(ListView):
    model = BlogPost
    queryset = BlogPost.objects.all().order_by('-created_at')
    template_name = 'tinklarastis/index.html'
    paginate_by = 4
    

class Featured(ListView):
    model = BlogPost
    queryset = BlogPost.objects.filter(featured=True).order_by('-created_at')
    template_name = 'tinklarastis/featured.html'
    paginate_by = 4


class BlogPostDetail(DetailView):
    model = BlogPost
    template_name = 'tinklarastis/blogpost_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['liked_by_user'] = False

        if self.object.likes.filter(pk=self.request.user.id).exists():
            context['liked_by_user'] = True

        comments_list = self.object.comments.all().order_by('-created_at')  
        paginator = Paginator(comments_list, 5)

        page = self.request.GET.get('page')
        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)

        context['comments'] = comments
        context['total_comments'] = comments_list.count()
        return context


class LikeBlogpost(View):
    def post(self, request, pk):
        blogpost = BlogPost.objects.get(id=pk)
        if blogpost.likes.filter(pk=self.request.user.id).exists():
                blogpost.likes.remove(request.user.id)
        else:
            blogpost.likes.add(request.user.id)

        blogpost.save()
        return redirect('blogpost_detail', pk) 


class DeleteBlogpostView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BlogPost
    template_name = 'tinklarastis/delete_blogpost.html'
    success_url = reverse_lazy('index')

    def test_func(self):
        blogpost = BlogPost.objects.get(id=self.kwargs.get('pk'))
        return self.request.user.id == blogpost.author.id
    
class AddCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'tinklarastis/add_comment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blogpost'] = get_object_or_404(BlogPost, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blogpost_detail', kwargs={'pk': self.object.post_id})





def upload_video(request):
    if request.method == 'POST':
        blogpost_form = BlogPostForm(request.POST)
        video_form = VideoForm(request.POST, request.FILES)
        if blogpost_form.is_valid() and video_form.is_valid():
            blogpost = blogpost_form.save(commit=False)
            blogpost.author = request.user
            blogpost.save()
            video = video_form.save()
            video_path = video.video.path
            thumbnail_filename = f'thumbnail_{uuid.uuid4()}.png'
            thumbnail_path = os.path.join(os.path.dirname(video_path), thumbnail_filename) 
            generate_thumbnail(video_path, thumbnail_path)
            video.thumbnail = thumbnail_path
            video.save()
            blogpost.videos.add(video)
            return redirect(blogpost)
    else:
        blogpost_form = BlogPostForm()
        video_form = VideoForm()
    return render(request, 'tinklarastis/upload.html', {'blogpost_form': blogpost_form, 'video_form': video_form})
def custom_403_view(request, exception):
    return redirect('index')

def create_blog_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            form.save_m2m()
            return redirect('blogpost_detail', pk=blog_post.pk)
    else:
        form = BlogPostForm()
    return render(request, 'tinklarastis/create_blog_post.html', {'form': form})
