import logging
from django.core.signals import request_finished
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone

from .functions import send_ready_stauts_for_test
from .models import Test

# @receiver(post_save, sender=Test)
# def golab_test_signal(sender, instance, created, **kwargs):
# print(instance.__original_testStatus)
# print(instance.test_status)
# if instance:
#     print(instance.test_status)

test_model_pre_save_signal_dispatch_id = 'test_model_pre_save_signal_dispatch_id'
test_model_post_save_signal_dispatch_id = 'test_model_post_save_signal_dispatch_id'

logger = logging.getLogger(__name__)


# @receiver(pre_save, sender=Test, dispatch_uid=test_model_pre_save_signal_dispatch_id)
# def golab_test_signal(sender, instance, **kwargs):
#     pre_save.disconnect(golab_test_signal, sender=Test, dispatch_uid=test_model_pre_save_signal_dispatch_id)
#
#     # TODO: If notification can only be sent once, add a flag in the test table to check this
#     if instance.test_status == 'ready':
#         send_ready_stauts_for_test(instance)
#     pre_save.connect(golab_test_signal, sender=Test, dispatch_uid=test_model_pre_save_signal_dispatch_id)
#
#
# @receiver(post_save, sender=Test, dispatch_uid=test_model_post_save_signal_dispatch_id)
# def golab_test_post_save_signal(sender, instance, created, **kwargs):
#     post_save.disconnect(golab_test_signal, sender=Test, dispatch_uid=test_model_post_save_signal_dispatch_id)
#     if not created:
#         # update processed field when the model instance is updated
#         instance.processed_date = timezone.now()
#         instance.save()
#     post_save.connect(golab_test_signal, sender=Test, dispatch_uid=test_model_post_save_signal_dispatch_id)


@receiver(post_save, sender=Test)
def golab_test_post_save(sender, created, instance, **kwargs):
    # if not created:
    print(instance)

    if instance.test_status == 'ready':
        # instance.processed_date = timezone.now()
        # instance.save()
        send_ready_stauts_for_test(instance)
