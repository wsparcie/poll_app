from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Poll, Choice, Vote, Token
from .forms import PollAddForm, ChoiceAddForm
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.urls import reverse

@login_required()
def poll_answer(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    choices = poll.choice_set.all()
    return render(request, 'polls/poll_answer.html', {'poll': poll, 'choices': choices})

@login_required()
def polls_list(request):
    all_polls = Poll.objects.all()
    search_term = ""
    if "search" in request.GET:
        search_term = request.GET["search"]
        all_polls = all_polls.filter(text__icontains=search_term)
    context = {
        "polls": all_polls,
        "search_term": search_term,
    }
    return render(request, "polls/polls_list.html", context)

@login_required()
def polls_add(request):
    if request.user.has_perm("polls.add_poll"):
        if request.method == "POST":
            form = PollAddForm(request.POST)
            if form.is_valid:
                poll = form.save(commit=False)
                poll.owner = request.user
                poll.save()
                Choice(poll=poll, choice_text=form.cleaned_data["choice1"]).save()
                Choice(poll=poll, choice_text=form.cleaned_data["choice2"]).save()
                messages.success(
                    request,
                    "Poll & Choices added successfully.",
                    extra_tags="alert alert-success alert-dismissible fade show",
                )
                return redirect("polls:list")
        else:
            form = PollAddForm()
        context = {
            "form": form,
        }
        return render(request, "polls/add_poll.html", context)
    else:
        return HttpResponse("Sorry but you don't have permission to do that!")

@login_required
def polls_delete(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.user != poll.owner:
        return redirect("home")
    poll.delete()
    messages.success(
        request,
        "Poll Deleted successfully.",
        extra_tags="alert alert-success alert-dismissible fade show",
    )
    return redirect("polls:list")

@login_required
def add_choice(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.user != poll.owner:
        return redirect("home")
    if request.method == "POST":
        form = ChoiceAddForm(request.POST)
        if form.is_valid:
            new_choice = form.save(commit=False)
            new_choice.poll = poll
            new_choice.save()
            messages.success(
                request,
                "Choice added successfully.",
                extra_tags="alert alert-success alert-dismissible fade show",
            )
            return redirect("polls:edit", poll.id)
    else:
        form = ChoiceAddForm()
    context = {
        "form": form,
    }
    return render(request, "polls/add_choice.html", context)

@login_required
def choice_delete(request, choice_id):
    choice = get_object_or_404(Choice, pk=choice_id)
    poll = get_object_or_404(Poll, pk=choice.poll.id)
    if request.user != poll.owner:
        return redirect("home")
    choice.delete()
    messages.success(
        request,
        "Choice Deleted successfully.",
        extra_tags="alert alert-success alert-dismissible fade show",
    )
    return redirect("polls:edit", poll.id)

def poll_detail(request, poll_id):
    token = request.GET.get('token')
    try:
        poll = Poll.objects.get(pk=poll_id)
        token_obj = Token.objects.get(poll=poll, token=token, expires_at__gt=timezone.now())
        if token_obj.used:
            messages.info(
                request,
                "You have already voted in this poll.",
                extra_tags="alert alert-info alert-dismissible fade show",
            )
            return render(request, "polls/post_poll.html")
        return render(request, 'polls/poll.html', {
            'poll': poll,
            'token': token
        })
    except (Poll.DoesNotExist, Token.DoesNotExist):
        return render(request, 'polls/poll.html', {
            'poll': None,
            'token': token
        })
        
def poll_vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    choice_id = request.POST.get("choice")
    token = request.POST.get("token")
    if not poll.user_can_vote(request.user, token):
        messages.error(
            request,
            "You already voted this poll or the token is invalid!",
            extra_tags="alert alert-warning alert-dismissible fade show",
        )
        return redirect("polls:list")
    if not choice_id:
        messages.error(
            request,
            "No choice selected!",
            extra_tags="alert alert-warning alert-dismissible fade show",
        )
        return redirect("polls:detail", poll_id)
    try:
        choice = Choice.objects.get(id=choice_id)
        vote_data = {
            'poll': poll,
            'choice': choice
        }
        if request.user.is_authenticated:
            vote_data['user'] = request.user
        if token:
            vote_data['token'] = token
        Vote.objects.create(**vote_data)
        if token:
            token_obj = Token.objects.get(token=token, poll=poll)
            token_obj.used = True
            token_obj.save()
        messages.success(
            request,
            "Vote recorded successfully!",
            extra_tags="alert alert-success alert-dismissible fade show",
        )
        return render(request, "polls/post_poll.html", {
            'poll': poll,
            'token': token
        })
    except Choice.DoesNotExist:
        messages.error(
            request,
            "Invalid choice selected!",
            extra_tags="alert alert-warning alert-dismissible fade show",
        )
        return redirect("polls:detail", poll_id)

@login_required
def end_poll(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.user != poll.owner:
        return redirect("home")
    if poll.active is True:
        poll.active = False
        poll.save()
        return render(request, "polls/poll_answer.html", {"poll": poll})
    else:
        return render(request, "polls/poll_answer.html", {"poll": poll})

@login_required
def generate_token(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.user != poll.owner:
        return redirect("home")
    token = Token.objects.create(
        poll=poll,
        expires_at=timezone.now() + timezone.timedelta(days=7)
    )
    poll_url = request.build_absolute_uri(
        f"{reverse('polls:detail', args=[poll_id])}?token={token.token}"
    )
    messages.success(
        request,
        f"New share link generated! Share this URL: {poll_url}",
        extra_tags="alert alert-success alert-dismissible fade show",
    )
    return redirect("polls:list")

@login_required
def poll_tokens(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.user != poll.owner:
        return redirect("home")
    tokens = Token.objects.filter(poll=poll).order_by('-created_at')
    context = {
        'poll': poll,
        'tokens': tokens,
    }
    return render(request, "polls/poll_tokens.html", context)