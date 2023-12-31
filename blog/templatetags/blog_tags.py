from django import template
from blog.models import Post, Comment
from blog.models import Category

register = template.Library()


@register.inclusion_tag('blog/Blog_latest_post.html')
def latestposts(arg):
    posts = Post.objects.filter(status=1).order_by('-published_at')[:arg]
    return {'posts': posts}


@register.inclusion_tag('blog/Blog_post_category.html')
def postcategories():
    posts = Post.objects.filter(status=1)
    categories = Category.objects.all()
    cat_dict = {}
    for name in categories:
        cat_dict[name] = posts.filter(category=name).count()

    return {'categories': cat_dict}


@register.simple_tag(name='count_comments')
def function(p_id):
    return Comment.objects.filter(post=p_id, aproved=True).count()
