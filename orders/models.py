import uuid

from django.contrib.auth import get_user_model
from django.db import models


class Order(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="کاربر",
    )

    name = models.CharField(
        max_length=255,
        verbose_name="نام سفارش",
        error_messages={
            "blank": "نام سفارش نمی‌تواند خالی باشد.",
            "max_length": "نام سفارش نباید بیشتر از ۲۵۵ کاراکتر باشد.",
        },
    )

    count = models.PositiveIntegerField(
        verbose_name="تعداد",
        error_messages={
            "blank": "تعداد نمی‌تواند خالی باشد.",
            "invalid": "تعداد باید یک عدد صحیح مثبت باشد.",
        },
    )

    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="قیمت کل",
        error_messages={
            "blank": "قیمت کل نمی‌تواند خالی باشد.",
            "invalid": "قیمت کل باید عددی معتبر باشد.",
        },
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    edited_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ ویرایش")

    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارش‌ها"
        ordering = ["-created_at"]
        permissions = [
            ("view_all_orders", "دسترسی مشاهده همه سفارش‌ها"),
            ("edit_all_orders", "دسترسی ویرایش همه سفارش‌ها"),
            ("delete_all_orders", "دسترسی حذف همه سفارش‌ها"),
            ("filter_all_orders", "دسترسی فیلتر کردن سفارش‌ها"),
        ]

    def __str__(self):
        return f"{self.name} - {self.user.username}"
