from django.contrib import admin
from .models import Petition, Vote

# Register your models here.
@admin.register(Petition)
class PetitionAdmin(admin.ModelAdmin):
    list_display = ['movie_title', 'title', 'created_by', 'created_at', 'vote_count', 'total_votes']
    list_filter = ['created_at', 'movie_year']
    search_fields = ['movie_title', 'title', 'description', 'created_by__username']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'petition', 'vote_type', 'created_at']
    list_filet = ['vote_type', 'created_at']
    search_fields = ['user__username', 'petition__movie_title']
    ordering = ['-created_at']