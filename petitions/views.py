from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from .models import Petition, Vote
from .forms import PetitionForm

# Create your views here.
def index(request):
    petitions = Petition.objects.annotate(
        yes_votes_count=Count('votes', filter=Q(votes__vote_type='yes')),
        total_votes_count=Count('votes')
    ).order_by('-created_at')

    template_data = {
        'title': 'Movie Petitions',
        'petitions': petitions
    }

    return render (request, 'petitions/index.html', {'template_data': template_data})

@login_required
def create(request):
    template_data = {'title': 'Create Petition'}

    if request.method == 'POST':
        form = PetitionForm(request.POST)
        if form.is_valid():
            petition = form.save(commit=False)
            petition.created_by = request.user
            petition.save()
            messages.success(request, 'Petition created successfully!')
            return redirect('petitions.index')
        else:
            template_data['form'] = form
    else:
        template_data['form'] = PetitionForm()
    return render(request, 'petitions/create.html', {'template_data': template_data})
    
@login_required
def vote(request, petition_id):
    petition = get_object_or_404(Petition, id=petition_id)
    vote_type = request.POST.get('vote_type')

    if vote_type not in ['yes', 'no']:
        messages.error(request, 'Invalid vote type.')
        return redirect('petitions.index')
    
    existing_vote = Vote.objects.filter(petition=petition, user=request.user).first()

    if existing_vote:
        existing_vote.vote_type = vote_type
        existing_vote.save()
        messages.success(request, f'Your vote has been update to {vote_type}.')
    else:
        Vote.objects.create(
            petition=petition,
            user = request.user,
            vote_type=vote_type
        )
        messages.success(request, f'Thank you for voting {vote_type}!')

    return redirect('petitions.index')

@login_required
def detail(request, petition_id):
    petition = get_object_or_404(Petition, id=petition_id)

    user_vote = None
    if request.user.is_authenticated:
        try:
            user_vote = Vote.objects.get(petition=petition, user=request.user)
        except Vote.DoesNotExist:
            pass

    votes = Vote.objects.filter(petition=petition).order_by('-created_at')

    template_data = {
        'title': f'Petition: {petition.movie_title}',
        'petition': petition,
        'user_vote': user_vote,
        'votes': votes
    }

    return render(request, 'petitions/detail.html', {'template_data': template_data})