from django.shortcuts import render


def note_list(request):
    """List all blog posts/notes"""
    return render(request, 'notes/list.html')


def note_detail(request, note_id):
    """Blog post/note detail view"""
    return render(request, 'notes/detail.html', {'note_id': note_id})
