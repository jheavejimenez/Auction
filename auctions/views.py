from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import CreateListing, CommentForm, NewBidForm


def index(request):
    # list all item in the database
    listing = Listing.objects.all()
    return render(request, "auctions/index.html", {'listing': listing})


def productDetail(request, id):
    # get the id of a product in the database
    cf = CommentForm()
    bf = NewBidForm()
    product_item = Listing.objects.get(pk=id)
    if request.user.is_authenticated:
        if Watchlist.objects.filter(user=request.user, item=id).exists():
            is_added = True
        else:
            is_added = False
        return render(request, "auctions/productDetail.html",
                      {
                          'product': product_item,
                          'is_added': is_added,
                          'comment_form': cf,
                          'NewBidForm': bf
                      })
    else:
        return render(request, "auctions/productDetail.html",
                      {
                          'product': product_item,
                          'comment_form': cf,
                          'NewBidForm': bf
                       })


def getProductCategory(request, item_category):
    # filter the item by its category
    category = Listing.objects.filter(category=item_category)
    return render(request, "auctions/getProductCategory.html", {
        'product_category': category,
        'item_category': item_category
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:

            return render(request, "auctions/register.html", {
                "msgPasswordError": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "msgUsernameError": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url='login')
def createList(request):
    # create a listing post
    if request.method == "POST":
        form = CreateListing(request.POST or None)
        if form.is_valid():  # save if the input data is valid
            context = form.save(commit=False)
            context.Seller = request.user
            context.save()
            return HttpResponseRedirect(reverse("index"))

    else:
        form = CreateListing
        return render(request, "auctions/createList.html", {'form': form})


@login_required(login_url='login')
def watchlist_add(request, product_id):
    item_to_save = get_object_or_404(Listing, pk=product_id)

    # Check if the item already exists in that user watchlist

    if Watchlist.objects.filter(user=request.user, item=product_id).exists():

        messages.add_message(request, messages.ERROR,
                             "You already have it in your watchlist.")
        Watchlist.objects.filter(user=request.user, item=product_id).delete()
        return HttpResponseRedirect(reverse("index"))

    # Get the user watchlist or create it if it doesn't exists
    user_list, created = Watchlist.objects.get_or_create(user=request.user)

    user_list.item.add(item_to_save)
    messages.add_message(request, messages.SUCCESS,
                         "Successfully added to your watchlist")

    return HttpResponseRedirect(reverse("get_watchlist"))


def get_watchlist(request):
    try:
        product_watchlist = Watchlist.objects.get(user=request.user).item.all()
        return render(request, "auctions/watchlist_add.html",
                      {
                          'product_watchlist': product_watchlist
                      })
    except Watchlist.DoesNotExist:
        return render(request, "auctions/watchlist_add.html")


@login_required(login_url='/login')
def add_comment(request, id):
    if request.method == 'POST':
        cf = CommentForm(request.POST or None)
        if cf.is_valid():
            post = get_object_or_404(Listing, pk=id)
            content = request.POST.get('content')
            comment = User_Comment.objects.create(post=post, user=request.user, content=content)
            comment.save()

            return redirect(request.META.get('HTTP_REFERER'))
    else:

        context = {
            'comment_form': CommentForm(),
        }
        return render(request, "auctions/productDetail.html", context)


@login_required(login_url='/logiin')
def take_bid(request, id):
    product_item = Listing.objects.get(pk=id)
    offer = float(request.POST['offer'])
    if is_valid(offer,  product_item):
        product_item.currentBid = offer
        bf = NewBidForm(request.POST)
        newbid = bf.save(commit=False)
        newbid.product = product_item
        newbid.user = request.user
        newbid.save()
        product_item.save()
        return HttpResponseRedirect(reverse("productDetail", args=[id]))
    else:
        context = {
            'comment_form': CommentForm(),
            'product': product_item,
            "NewBidForm": NewBidForm(),
            "error_min_value": True
        }
        return render(request, "auctions/productDetail.html", context)


def is_valid(offer, listing):
    if offer >= listing.startingBid and (listing.currentBid is None or offer > listing.currentBid):
        return True
    else:
        return False


def close_listing(request, id):
    product_item = Listing.objects.get(pk=id)
    if request.user == product_item.Seller:
        product_item.buyer = Bid.objects.filter(product=product_item).last().user
        product_item.save()
        return HttpResponseRedirect(reverse("productDetail", args=[id]))
    else:
        product_item.Watchlist.add(request.user)
    return HttpResponseRedirect(reverse("my_winnings"))
