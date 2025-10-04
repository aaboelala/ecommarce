# from django.dispatch import receiver
# from django.db.models.signals import post_save , post_delete
# from django.db.models import Avg

# from .models import Rating , ProductRating


# @receiver(post_save,sender=Rating)
# def update_product_rating_on_save(sender,instance,**kwargs):
#     product=instance.product
#     rating=product.ratings.all()
#     total_reviews=rating.count()
#     average_rating=rating.aggregate(Avg("score"))['score__avg'] or 0.0

#     product_rating,created=ProductRating.objects.get_or_create(product=product)

#     product_rating.average_rating=average_rating
#     product_rating.total_reviews=total_reviews
#     product_rating.save()


# @receiver(post_delete,sender=Rating)
# def update_product_rating_on_delete(sender,instance,**kwargs):
#     product=instance.product
#     rating=product.ratings.all()
#     total_reviews=rating.count()
#     average_rating=rating.aggregate(Avg("score"))['score__avg'] or 0.0

#     product_rating,created=ProductRating.objects.get_or_create(product=product)

#     product_rating.average_rating=average_rating
#     product_rating.total_reviews=total_reviews
#     product_rating.save()










    

    





